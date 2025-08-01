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

  const handleSessionToken= (e) => {
    const newModel = { ...model };
    newModel.Configuration.sessionToken = e.target.value;
    handleUpdateModel(newModel);
  };

  const handlePromptChange = (e) => {
    const newModel = { ...model };
    newModel.Configuration.promptText = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleOutputTypeChange = (e) => {
    const newModel = { ...model };
    newModel.Configuration.outputType = e.target.value;
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
        Secret Access Key::
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
        Write a prompt:
      </Typography>
      <TextField
        fullWidth
        id="prompt"
        value={model.Configuration.promptText || ''}
        onChange={handlePromptChange}
        label="Prompt"
        multiline
        rows={4}
        placeholder="Start typing prompt here..."
      />

      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Select Output Type:
        </Typography>
        <RadioGroup
          value={model.Configuration.outputType || 'analysis'}
          onChange={handleOutputTypeChange}
          aria-label="output type"
          name="output-type-group"
        >
          <FormControlLabel value="table" control={<Radio />} label="Output Table" />
          <FormControlLabel value="analysis" control={<Radio />} label="Output Analysis" />
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