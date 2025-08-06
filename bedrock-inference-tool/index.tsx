import React, { useContext } from 'react';
import ReactDOM from 'react-dom';
import { AyxAppWrapper, Box, Typography, TextField, RadioGroup, Radio, FormControlLabel } from '@alteryx/ui';
import { Context as UiSdkContext, DesignerApi } from '@alteryx/react-comms';

const App = () => {
  const [model, handleUpdateModel] = useContext(UiSdkContext);

  const handleAccessKeyID = (e) => {
    const newModel = { ...model };
    newModel.Configuration.accessKeyID = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleSecretAccessKey = (e) => {
    const newModel = { ...model };
    newModel.Configuration.secretAccessKey = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleSessionToken = (e) => {
    const newModel = { ...model };
    newModel.Configuration.sessionToken = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleRegion = (e) => {
    const newModel = { ...model };
    newModel.Configuration.region = e.target.value;
    handleUpdateModel(newModel);
  };

  const handlePromptChange = (e) => {
    const newModel = { ...model };
    newModel.Configuration.promptText = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleInputTypeChange = (e) => {
    const newModel = { ...model };
    newModel.Configuration.inputType = e.target.value;
    handleUpdateModel(newModel);
  };
  
  const handleOutputTypeChange = (e) => {
    const newModel = { ...model };
    newModel.Configuration.outputType = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleTokens = (e) => {
    const newModel = { ...model };
    newModel.Configuration.tokens = e.target.value;
    handleUpdateModel(newModel);
  };

  return (
    <Box p={4}>
      <Typography variant="h5" gutterBottom>
        Access Key ID:
      </Typography>
      <TextField
        fullWidth
        id="access_id"
        value={model.Configuration.accessKeyID || ''}
        onChange={handleAccessKeyID}
        label="AccessKeyID"
        placeholder="Enter Access Key ID"
      />
      <Typography variant="h5" gutterBottom>
        Secret Access Key:
      </Typography>
      <TextField
        fullWidth
        id="secret_key"
        value={model.Configuration.secretAccessKey || ''}
        onChange={handleSecretAccessKey}
        label="SecretAccessKey"
        placeholder="Enter Secret Access Key"
      />
      <Typography variant="h5" gutterBottom>
        Session Token (optional):
      </Typography>
      <TextField
        fullWidth
        id="session_token"
        value={model.Configuration.sessionToken || ''}
        onChange={handleSessionToken}
        label="SessionToken"
        placeholder="Enter Session Token"
      />
      <Typography variant="h5" gutterBottom>
        Maximum output tokens (default: 512):
      </Typography>
      <TextField
        fullWidth
        id="tokens"
        value={model.Configuration.tokens || 512}
        type="number"
        onChange={handleTokens}
        label="Enter max number of output tokens, e.g. 512"
      />
      <Typography variant="h5" gutterBottom>
        Region (default: us-east-1):
      </Typography>
      <TextField
        fullWidth
        id="region"
        value={model.Configuration.region || 'us-east-1'}
        onChange={handleRegion}
        label="Region"
        placeholder="Enter AWS region"
      />
      <Typography variant="h5" gutterBottom>
        Write a prompt:
      </Typography>
      <TextField
        fullWidth
        id="prompt"
        value={model.Configuration.promptText || ''}
        onChange={handlePromptChange}
        label="Prompt"
        multiline
        rows={12}
        placeholder="Start typing prompt here..."
      />

      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Select Input Type:
        </Typography>
        <RadioGroup
          value={model.Configuration.inputType || 'table'}
          onChange={handleInputTypeChange}
          aria-label="input type"
          name="input-type-group"
        >
          <FormControlLabel value="json" control={<Radio />} label="Grouped JSON" />
          <FormControlLabel value="table" control={<Radio />} label="Table" />
        </RadioGroup>
      </Box>

      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Select Output Type:
        </Typography>
        <RadioGroup
          value={model.Configuration.outputType || 'table'}
          onChange={handleOutputTypeChange}
          aria-label="output type"
          name="output-type-group"
        >
          <FormControlLabel value="table" control={<Radio />} label="Output Table" />
        </RadioGroup>
      </Box>
    </Box>
  );
};

const Tool = () => {
  return (
    <DesignerApi messages={{}}>
      <AyxAppWrapper>
        <App />
      </AyxAppWrapper>
    </DesignerApi>
  );
};

ReactDOM.render(
  <Tool />,
  document.getElementById('app')
);
