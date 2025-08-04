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

from ayx_python_sdk.core import (
    Anchor,
    PluginV2,
)
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

import pyarrow as pa
import requests
import json
import re
import time
from datetime import datetime

class GoogleAPITool(PluginV2):
    """A Google API Plugin that takes the first column of a CSV file containing search queries and calls the Google API for custom search."""

    def __init__(self, provider: AMPProviderV2):
        """Construct the plugin."""

        self.name = "GoogleAPITool"
        self.provider = provider
        
        self.batches = [] # To collect the input csv data
        self.search_results = [] # To store the search results

        # Get API key and search engine ID from React input boxes
        self.api_key = provider.tool_config.get("apiKey")
        self.search_engine_id = provider.tool_config.get("searchEngineId")

        # Get max number of searches per query (must be between 1 and 10)
        max_num = provider.tool_config.get("maxNum", 10)
        if max_num is not None and 0 < int(max_num) <= 10:
            max_num = int(max_num)
        else:
            max_num = 10
            self.provider.io.warn("Invalid number of searches - setting max searches to 10")
        
        self.max_searches = max_num

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
        self.batches.append(batch) # Append all table inputs

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

    def search_google(self, query: str) -> list:
        """Search Google using Custom Search API"""

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': self.max_searches
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except requests.exceptions.RequestException as e:
            self.provider.io.error(f"Error searching for '{query}': {e}")
            return None

    def collect_data(self, query: str) -> None:
        """Collect search data for a single query"""

        self.provider.io.info(f"  Searching: {query}")

        results = self.search_google(query)

        if not results:
            return None

        for i, result in enumerate(results, 1):
            self.search_results.append({
                'query': query,
                'result_rank': i,
                'title': result.get('title', ''),
                'snippet': result.get('snippet', ''),
                'link': result.get('link', ''),
                'display_link': result.get('displayLink', ''),
                'formatted_url': result.get('formattedUrl', ''),
                'search_timestamp': datetime.now().isoformat()
            })
        time.sleep(1)

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

        if not self.api_key:
            self.provider.io.error("No API key.")
            return
        if not self.search_engine_id:
            self.provider.io.error("No search engine key.")
            return

        if self.batches:
            input_table = pa.concat_tables(self.batches)
            input_rows = input_table.to_pylist() # Convert input csv table to Python list
        else:
            self.provider.io.error("No input data received.")
            return
        
        for item in input_rows:
            query_text = next(iter(item.values())) #item.get('query')  # get the first VALUE from the dict, not the key

            if query_text:
                self.collect_data(query_text) # Append to search results list

        output_table = pa.Table.from_pylist(self.search_results) # Output table from response
        self.provider.write_to_anchor("Output", output_table)
        
        self.provider.io.info(f"Data collection complete. {self.name} tool done.")
