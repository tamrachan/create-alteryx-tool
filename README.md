# Alteryx Custom Tool

Using Python as the backend and React.js as the frontend.
Updated July 2025 version of [Kongson Cheung's Blog](https://kongsoncheung.blogspot.com/2023/08/how-to-develop-alteryx-custom-to.html)

## Set up instructions
### 1. Install [Minicoda3](https://docs.conda.io/en/latest/miniconda.html) (download from the site and install).
### 2. Open Anacoda Prompt and create a virtual environment with the command:
```powershell
conda create -n [ENV_NAME] python=3.10.13
```
### 3. Activate the environment.
```powershell
conda activate [ENV_NAME]
```
### 4. Install the AYX Python SDK.
```powershell
pip install ayx-python-sdk
```
### 5. Install the AYX Plugin CLI
```powershell
pip install ayx-plugin-cli
```
### 6. Create (or initialise) the AYX Plugin Workspace
```powershell
ayx_plugin_cli sdk-workspace-init
```

> Package Name: [The name of the package]  
Tool Category [Python SDK Examples]: [The category of the tools]  
Description []: Description of the package.  
Author []: Who is the author of the package.  
Company []: The company name.  
Backend Language (python): python  

### 7. Install NodeJS. It is required to developer UI for the tool.
```powershell
conda install -c anaconda nodejs=16.13.1
```
### 8. Create the AYX Plugin
```powershell
ayx_plugin_cli create-ayx-plugin
```

> **Tool Name:** [The name of the tool]  
**Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [single-   input-single-output]:** [the type of the tool]  
**Description []:** [description of the tool]  
**Tool Version [1.0]:** [version of the tool]  
**DCM Namespace []:**  [DCM Namespace to be used]

e.g.  
**Tool Name:** Test Input Tool  
**Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [single-   input-single-output]:** input  
**Description []:** A test input tool  
**Tool Version [1.0]:** 1.0  
**DCM Namespace []:**

### 9. Then you have a folder structure of:
- `.ayx_cli.cache`
- `backend`
- `configuration`
- `DcmSchema`
- `ui`
- .gitignore
- ayx_workspace.json
- README.md

### 10. Backend Development (Python)  
`backend/ayx_plugins/<tool_name.py>`  
<br>
Open this using an editor or any IDE to start the tool development. <br>There are four important functions:

>`def __init__(self, provider: AMPProviderV2) -> None:`  
This is to initialise the tools - specifically to initialise the variables to be used in the backend code.

>`def on_record_batch(self, batch: "Table", anchor: namedtuple) -> None:`  
This is to handle the input records provided in batches.  Input tool does not required to manipulate this.

>`def on_incoming_connection_complete(self, anchor: namedtuple) -> None:`  
When an incoming anchor is complete i.e. all input batches are processed, this will be called.  Input tool does not required to handle this.

>`def on_complete(self) -> None:`  
Once everything has been manipulated, this is to free up the resources and also finalise the completion.  Final logic happens here for input tool.  

Ensure pa is installed with these imports:
```bash
import pyarrow as pa
import pyarrow.compute as pc
from typing import TYPE_CHECKING
```
> !!! Once you export this plugin - to edit and update inside Alteryx.   
Edit the python file at: `C:\Users\<user>\AppData\Roaming\Alteryx\Tools\<Tool_Name>_1_0\site-packages\ayx_plugins\<tool_name>.py`


### 11. Frontend Development (React.js)   
`ui/TestInputTool/src/index.tsx`

### 12. Run locally in a test environment (hypothetically) - didn't work
```powershell
ayx_plugin_cli designer-install
```
### 13. Create the YXI and Deploy to Alteryx Designer
Once the frontend, backend, configuration (like icon, description, version, etc) are completed, it can be packaged to YXI file to share and also install into Alteryx Designer.  It is simply running the command:

```powershell
ayx_plugin_cli create-yxi
```

Creates a new folder `build/yxi/<folder_name>.yxi`