# Copyright (C) 2022 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING
import pyarrow as pa

import boto3 # For AWS Bedrock

import re # For cleaning AWS Bedrock response
import traceback # For debugging
import json

from ayx_python_sdk.core import (
    Anchor,
    PluginV2,
)

from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

class BedrockInferenceTool(PluginV2):
    """A sample Plugin that passes data from an input connection to an output connection."""

    def __init__(self, provider: AMPProviderV2):
        """Construct the plugin."""
        self.name = "BedrockInferenceTool"
        self.provider = provider
        self.batches = []

        self.access_key = provider.tool_config.get("accessKeyID")
        self.secret_key = provider.tool_config.get("secretAccessKey")
        self.session_token = provider.tool_config.get("sessionToken", None)
        self.max_tokens = provider.tool_config.get("tokens", 512)
        if not self.max_tokens:
            self.max_tokens = int(512)
            self.provider.io.warn("Defaulting to 512 max output tokens as no number was provided.")
        else:
            self.max_tokens = int(self.max_tokens)
        self.region = provider.tool_config.get("region", "us-east-1")

        self.prompt_template = provider.tool_config.get("promptText") # Get prompt template from text box
        self.input_type = provider.tool_config.get("inputType", "table")
        self.output_type = "table" # provider.tool_config.get("outputType", "table")

        # Setup boto3 Bedrock client
        if self.session_token:
            # With session token
            self.bedrock_client = boto3.client( 
                service_name="bedrock-runtime",
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                aws_session_token=self.session_token
            )
        else:
            # Without session token
            self.bedrock_client = boto3.client(
                service_name="bedrock-runtime",
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )

        self.provider.io.info(f"{self.name} tool started")

    def on_record_batch(self, batch: "pa.Table", anchor: Anchor) -> None:
        """
        Process the passed record batch.

        The method that gets called whenever the plugin receives a record batch on an input.

        This method IS NOT called during update-only mode.

        Parameters
        ----------
        batch
            A pyarrow Table containing the received batch.
        anchor
            A namedtuple('Anchor', ['name', 'connection']) containing input connection identifiers.
        """

        self.batches.append(batch) # For AI table input

    def on_incoming_connection_complete(self, anchor: Anchor) -> None:
        """
        Call when an incoming connection is done sending data including when no data is sent on an optional input anchor.

        This method IS NOT called during update-only mode.

        Parameters
        ----------
        anchor
            NamedTuple containing anchor.name and anchor.connection.
        """
        self.provider.io.info(
            f"Received complete update from {anchor.name}:{anchor.connection}."
        )

    def analyse_with_bedrock(self, prompt: str) -> None:
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.2
        }

        # Set up client and response
        bedrock = self.bedrock_client
        request = json.dumps(native_request).encode('utf-8')

        try:
            # Invoke Bedrock model (Claude Sonnet 3.5 v2)
            response = bedrock.invoke_model(
                modelId="us.anthropic.claude-3-5-sonnet-20241022-v2:0", # CHANGE MODEL HERE
                body=request,
                accept="application/json",
                contentType="application/json"
            )
        except Exception as e:
            self.provider.io.error(f"Error invoking model: {e}")
            self.provider.io.error(traceback.format_exc())
            return
        
        self.provider.io.info(f"Success response: {response}")

        try:
            result = json.loads(response['body'].read().decode('utf-8'))
            self.provider.io.info(f"Bedrock response received: {result}")
            
            content = result.get("content", "")

            if isinstance(content, list) and content and isinstance(content[0], dict) and 'text' in content[0]:
                text = content[0]['text']
            else:
                text = content

            json_objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', str(text), re.DOTALL)

            for obj_str in json_objects:
                try:
                    # Clean up the JSON string
                    cleaned_str = obj_str.strip()
                    # Remove any trailing commas before closing braces
                    cleaned_str = re.sub(r',\s*}', '}', cleaned_str)
                    cleaned_str = re.sub(r',\s*]', ']', cleaned_str)
                    
                    parsed_obj = json.loads(cleaned_str)
                    self.provider.io.info(f"Parsed: {parsed_obj}")
                    self.parsed_data.append(parsed_obj)
                except Exception as e:
                    print(f"Error parsing JSON object: {e}")
                    print(f"Problematic JSON string: {obj_str}")
                    continue

        except Exception as e:
            self.provider.io.error(f"Error parsing model response: {e}")
            return

    def create_prompt(self, input_data) -> str:
        prompt = (
            f"The following JSON array represents tabular data:\n{input_data}\n\n"
            f"{self.prompt_template}\n\n"
            "Please return a modified version of this data as a JSON array of objects. "
            "Do not include explanations or formatting, ONLY the JSON array."
        )

        return prompt


    def write_output(self) -> None:
        self.provider.io.info(f"Parsed data: {self.parsed_data}")
        if isinstance(self.parsed_data, list) and all(isinstance(row, dict) for row in self.parsed_data):
            output_table = pa.Table.from_pylist(self.parsed_data) # Output table from response
            self.provider.write_to_anchor("Output", output_table)
            self.provider.io.info("Output table written successfully.")
        else:
            raise ValueError("Unexpected format: AI output is not as expected.")

    def on_complete(self) -> None:
        """
        Clean up any plugin resources, or push records for an input tool.

        This method gets called when all other plugin processing is complete.

        In this method, a Plugin designer should perform any cleanup for their plugin.
        However, if the plugin is an input-type tool (it has no incoming connections),
        processing (record generation) should occur here.

        Note: A tool with an optional input anchor and no incoming connections should
        also write any records to output anchors here.
        """
        # Return errors if mandatory fields are not completed
        if not self.prompt_template:
            self.provider.io.error("No prompt was provided.")
            return
        elif not self.access_key or not self.secret_key:
            self.provider.io.error("Missing AWS credentials.")
            return
            
        # Combine all input batches into one table
        if self.batches:
            input_table = pa.concat_tables(self.batches)
            input_rows = input_table.to_pylist()
        else:
            self.provider.io.error("No input data received.")
            return

        self.parsed_data = []
        if self.input_type == "json": # Writes output for every group by
            for json_object in input_rows:
                json_string = next(iter(json_object.values()))

                prompt = self.create_prompt(json_string)

                self.provider.io.info("Sending prompt to AWS Bedrock..." + prompt)
                
                self.analyse_with_bedrock(prompt)
            
        else: # ungrouped data
            prompt = self.create_prompt(input_rows)

            self.provider.io.info("Sending prompt to AWS Bedrock..." + prompt)
            self.analyse_with_bedrock(prompt)
            
        self.write_output()
        
        self.provider.io.info(f"{self.name} tool complete. Freeing resources.")