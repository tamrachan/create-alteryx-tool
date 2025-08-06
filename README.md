# Alteryx Custom Tool

This README contains:
1. How to create an Alteryx Plugin
2. How to develop/edit the plugin
3. Problems + solution

## How to create an Alteryx Plugin
Based on [Kongson Cheung's Blog](https://kongsoncheung.blogspot.com/2023/08/how-to-develop-alteryx-custom-to.html) - updated for July 2025 and onwards.  
These instructions were created using `Alteryx 2024.2`, `Python 3.10.13` as the backend and `Node.js 16.13.1` as the frontend.

If you have followed these steps before and already have a virtual environment with the dependencies, skip to Step 7.

### 1. Install [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) (download from the site and install).
### 2. Open Anacoda Prompt and create a virtual environment with the command:
> For example, my [ENV_NAME] was `alteryx_env` but name it whatever you like.
```powershell
conda create -n [ENV_NAME] python=3.10.13
```
### 3. Activate the environment.
```powershell
conda activate [ENV_NAME]
```
Now your terminal should say (ENV_NAME) C:\Users\...
### 4. Install the AYX Python SDK.
```powershell
pip install ayx-python-sdk
```
### 5. Install the AYX Plugin CLI
```powershell
pip install ayx-plugin-cli
```

### 6. Install NodeJS. It is required to developer UI for the tool.
```powershell
conda install -c anaconda nodejs=16.13.1
```

### 7. Create (or initialise) the AYX Plugin Workspace
Create a folder for your plugin and cd into it. Then run the following command to initiate the plugin workspace.
```powershell
ayx_plugin_cli sdk-workspace-init
```

> **Package Name:** [The name of the package]  
**Tool Category [Python SDK Examples]:** [The category of the tool - will show in Alteryx's tool bar]  
**Description []:** Description of the package.  
**Author []:** Author of the package.  
**Company []:** The company name.  
**Backend Language (python):** python  

<br>
Your folder should contain these paths now:

```text
C:.  
│   .gitignore  
│   ayx_workspace.json  
│   README.md  
│  
├───.ayx_cli.cache  
│       .doit.db.bak  
│       .doit.db.dat  
│       .doit.db.dir  
│  
├───backend  
│   │   requirements-local.txt  
│   │   requirements-thirdparty.txt  
│   │   setup.py  
│   │  
│   ├───ayx_plugins   
│   │       __init__.py  
│   │
│   └───tests  
├───configuration  
│       Config.xml  
│       default_package_icon.png  
│  
└───DcmSchemas  
```

### 8. Create the AYX Plugin

```powershell
ayx_plugin_cli create-ayx-plugin
```

> **Tool Name:** [The name of the tool]  
**Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [single-   input-single-output]:** [the type of the tool]  
**Will this tool write output data? [y/N]** [y/N]  
**Description []:** [description of the tool]  
**Tool Version [1.0]:** [version of the tool]  
**DCM Namespace []:**  [DCM Namespace to be used]  
**Do you want to skip generating UI component? [Default: No] [y/N]:** N  


e.g. Bedrock Inference Tool uses these settings:  
**Tool Name:** Bedrock Inference Tool  
**Tool Type (input, multiple-inputs, multiple-outputs, optional, output, single-input-single-output, multi-connection-input-anchor) [single-   input-single-output]:** single-input-single-output  
**Will this tool write output data? [y/N]** N  
**Description []:** An AI tool which calls the AWS Bedrock API. 
**Tool Version [1.0]:** 1.0  
**DCM Namespace []:**  

<br>
Congrats - now you have successfully initiated an Alteryx plugin! :)

## How to develop/edit the plugin
This is complicated due to the updated ayx_plugin_cli and lack of updated documentation for it.  
I briefly mention solutions for the problems I faced in steps 9 to 11. More detail can be found in the 'Problems + solutions' section.

### 9. Backend Development (Python)  
The backend Python script can be found at `backend/ayx_plugins/<tool_name.py>`. Open this using any IDE to start the tool development. 
<br><br>There are FOUR important functions:    <br>
`def __init__(self, provider: AMPProviderV2) -> None:`  
This is to initialise the tools - specifically to initialise the variables to be used in the backend code.

`def on_record_batch(self, batch: "Table", anchor: namedtuple) -> None:`  
This is to handle the input records provided in batches - Alteryx sends the input table rows in batches. 

`def on_incoming_connection_complete(self, anchor: namedtuple) -> None:`  
When an incoming anchor is complete i.e. all input batches are processed, this will be called.  This function sends a signal to Alteryx that all batches have been received. Nothing needs to be changed in this function.

`def on_complete(self) -> None:`  
This is where the main processing of your tool will be if using AWS Bedrock. If you are using the complete input csv, you can send all the data to bedrock in this function. Once everything has been manipulated, this function is also used to free up the resources and also finalise the completion.

<br>

>**WARNING**: Default template code gives import error

By default, the Python script contains:
```python
from typing import TYPE_CHECKING
...
if TYPE_CHECKING:
    import pyarrow as pa
```
However, this leads to an import error in Alteryx - "pa is not imported". Solve this by removing the if statement and indentation like below:

```python
from typing import TYPE_CHECKING
import pyarrow as pa
```


### 10. Frontend Development (React.js)   
Edit the file at `ui/TestInputTool/src/index.tsx` for the frontend (what you see in the Alteryx tool). There are code examples in the `tool-templates` folder.

### 11. Create the YXI and Deploy to Alteryx Designer
Once the frontend, backend, configuration (like icon, description, version, etc) are completed, it can be packaged to YXI file to share and install into Alteryx Designer. 

This can be done in two ways:
1. `create-yxi` - only creating the .yxi and drag/drop in Alteryx Designer
2. `designer-install` - automatically create and install the .yxi in Alteryx Designer so the tool is already there when you open Alteryx.

I would recommend using `designer-install` when developing. Both methods take a few minutes to export the .yxi so get a snack and relax.

#### Method 1: create-yxi
Simply run the command:

```powershell
ayx_plugin_cli create-yxi
```

This creates a new folder `build/yxi/<folder_name>.yxi` in your current directory. You can then drag/drop the .yxi into Alteryx and start using the tool.

#### Method 2: designer-install
Use the following command to update the YXI file:
```powershell
ayx_plugin_cli designer-install
```

> NOTE: The backend Python file does not update when running `ayx_plugin_cli designer-install`  
To fix: After creating the YXI, edit the Python file at `C:\Users\<user>\AppData\Roaming\Alteryx\Tools\<Tool_Name>_1_0\site-packages\ayx_plugins\<tool_name>.py`. The next section contains more detail on this.
<br>

## Problems + solutions
### Python script not updating after first export
```powershell
ayx_plugin_cli designer-install
```
The first use of the above command successfully exports your plugin to Alteryx. However, if you update your code after this and use the command again, the backend Python script does not update for some reason. To work around this, I worked directly in Alteryx's AppData where the tool was exported and modified the python script there. This way, once you save the script, changes are made directly in Alteryx and you do not need to export anything. 

Alteryx's AppData Python script file path: <br> `C:\Users\<user>\AppData\Roaming\Alteryx\Tools\<Tool_Name>_1_0\site-packages\ayx_plugins\<tool_name>.py`

> **WARNING**: Although the Python script does not update when running `ayx_plugin_cli designer-install`, the front-end `index.tsx` does update. If you need to update `index.tsx`, use `ayx_plugin_cli designer-install` but note <u>YOUR PYTHON SCRIPT IN APPDATA DIRECTORY WILL BE OVERWRITTEN!</u> <br>**To do:** Copy and paste your Python script back to your original plugin folder Python script. Then, when designer-install is completed, copy and paste it back into the APPDATA directory.

### Adding external Python libraries (Internal Error - Deadlock detected)
If you are using external Python libraries, e.g. boto3, they need to be added in `Your_Tool_Folder/backend/requirements-thirdparty.txt`, otherwise, Alteryx will flag "Internal Error - Deadlock detected".

I added the following to the `bedrock-inference-tool/backend/requirements-thirdparty.txt`.
```powershell
boto3==1.39.15
```

### DCM Connection

Ensure you put a DCM Namespace when creating the Alteryx plugin.

I did not completely figure this one out. I looked at [Alteryx's Example Tool](https://community.alteryx.com/t5/SDK-Resources/DCM-Input-Example-Tool/ta-p/1127605) to help.  

Credentials can be put in Alteryx: `File > Manage Connections > Credentials`  <br><br>
**This is what I did figure out:**  
Adding the third connection in `Your_Tool_Folder/configuration/Your_Tool_1_0/Your_Tool_1_0Config.xml` tells Alteryx to look for a DCM Connection. Make sure the `<DCM_Namespace>` is the same as the one in the Python code.
```xml
<InputConnections>
<Connection AllowMultiple="False" Label="" Name="Input" Optional="False" Type="Connection"/>
</InputConnections>
<OutputConnections>
<Connection AllowMultiple="False" Label="" Name="Output" Optional="False" Type="Connection"/>
</OutputConnections>
<Connections>
	<Connection name="<DCM_Namespace>" type="Credential" />
</Connections>
```
Here is some code I wrote that kind of worked - just kept receiving that "username" could not be found. But this is on the right track...
```python
def on_connection_loaded(self, conn):
        self.provider.io.info(f"DCM connection loaded: {conn}")

        # Safely get credentials
        self.access_key = conn.get("username")
        self.secret_key = conn.get("password")
        self.session_token = conn.get("extra", {}).get("sessionToken", None)

        if not self.access_key or not self.secret_key:
            self.provider.io.error("DCM connection is missing required fields (username/password).")
            self.dcm_valid = False
        else:
            self.dcm_valid = True


    def __init__(self, provider: AMPProviderV2):
        ...
        self.dcm_valid = False

        # Correctly call get_connection() method to get connection data
        provider.dcm.get_connection("<DCM_Namespace>", self.on_connection_loaded)

        if not self.dcm_valid:
            self.provider.io.error("Skipping execution due to invalid DCM credentials.")
            return

        self.provider.io.info("DCM connection complete")
```