import React, { useContext } from 'react';
import ReactDOM from 'react-dom';
import { AyxAppWrapper, Box, Typography, TextField, RadioGroup, Radio, FormControlLabel } from '@alteryx/ui';
import { Context as UiSdkContext, DesignerApi } from '@alteryx/react-comms';

const App = () => {
  const [model, handleUpdateModel] = useContext(UiSdkContext);

  const handleAPIKey = (e) => {
    const newModel = { ...model };
    newModel.Configuration.apiKey = e.target.value;
    handleUpdateModel(newModel);
  };

  const searchEngineId = (e) => {
    const newModel = { ...model };
    newModel.Configuration.searchEngineId = e.target.value;
    handleUpdateModel(newModel);
  };

  const handleMaxNum = (e) => {
    const newModel = { ...model };
    newModel.Configuration.maxNum = e.target.value;
    handleUpdateModel(newModel);
  };

  return (
    <Box p={4}>

      <Typography variant="h5" gutterBottom>
        Google API key:
      </Typography>
      <TextField
        fullWidth
        id="api_key"
        value={model.Configuration.apiKey || ''}
        onChange={handleAPIKey}
        label="GoogleAPIKey"
        placeholder="Enter Google API key"
      />

      <Typography variant="h5" gutterBottom>
        Search Engine ID:
      </Typography>
      <TextField
        fullWidth
        id="search_engine_id"
        value={model.Configuration.searchEngineId || ''}
        onChange={searchEngineId}
        label="SearchEngineID"
        placeholder="Enter search engine id"
      />

      <Typography variant="h5" gutterBottom>
        Max number of searches per query:
      </Typography>
      <TextField
        type="number"
        id="max_search_num"
        value={model.Configuration.maxNum}
        onChange={handleMaxNum}
        label="Max search number (must be between 1 and 10)"
      />
      
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