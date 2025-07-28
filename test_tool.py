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

"""Example pass through tool."""
import pyarrow as pa
import pyarrow.compute as pc
from typing import TYPE_CHECKING

from ayx_python_sdk.core import (
    Anchor,
    PluginV2,
)
from ayx_python_sdk.providers.amp_provider.amp_provider_v2 import AMPProviderV2

class TestTool(PluginV2):
    """A sample Plugin that passes data from an input connection to an output connection."""

    '''This is to initialize the tools.  Usually, to initialize the variable to be used in the backend code.'''
    def __init__(self, provider: AMPProviderV2):
        """Construct the plugin."""
        self.name = "TestInputTool"
        self.provider = provider # Main API object
        
        self.total_rows = 0
        # Read value from frontend config
        self.add_value = provider.tool_config.get("addValue", 2)

        self.provider.io.info(f"{self.name} tool started. Will add {self.add_value} to numeric columns!!.")

    '''This is to handle the record provided in batches.  Input tool does not required to manipulate this.'''
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

        # Count the number of rows in this batch and add to total
        batch_count = batch.num_rows
        self.total_rows += batch_count
        self.provider.io.info(f"Received {batch_count} rows in this batch")
        
        # Add 2 to any numerical data
        updated_columns = []
        column_names = []

        for i, column in enumerate(batch.columns):
            field = batch.schema.field(i)
            col_name = field.name
            col_type = field.type

            if pa.types.is_integer(col_type) or pa.types.is_floating(col_type):
                # Add 2 to numeric column
                updated_col = pc.add(column, 2)
                updated_columns.append(updated_col)
            else:
                # Keep non-numeric columns unchanged
                updated_columns.append(column)

            column_names.append(col_name)

        # Create new batch with modified columns
        new_batch = pa.Table.from_arrays(updated_columns, names=column_names)

        # Output the modified data
        self.provider.write_to_anchor("Output", new_batch)

    '''When there is an incoming anchor complete, this will be called.  Input tool does not required to handle this.'''
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

    '''Once the batches have been manipulated, this is to free up the resources and also finalize the completion.  All logics happen here for input tool.'''
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
        self.provider.io.info(f"Total rows received: {self.total_rows}")
        self.provider.io.info(f"{self.name} tool complete. Freeing resources.")
