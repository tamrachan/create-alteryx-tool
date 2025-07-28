import React, { useContext, useEffect} from 'react';
import ReactDOM from 'react-dom';
import { AyxAppWrapper, Box, Grid, Typography, makeStyles, Theme, TextField } from '@alteryx/ui';
// import { Alteryx } from '@alteryx/icons';
import { Context as UiSdkContext, DesignerApi } from '@alteryx/react-comms';



// const useStyles = makeStyles((theme: Theme) => ({
//   alteryx: {
//     color: theme.palette.brand.corporateBlue,
//     height: '125px',
//     width: '125px'
//   }
// }));

const App = () => {
  // const classes = useStyles();
  const [model, handleUpdateModel] = useContext(UiSdkContext);

  const handleChange = (e) => {
    const newModel = { ...model };
    newModel.Configuration.addValue = e.target.value;
    handleUpdateModel(newModel);
  };

  return (
    <Box p={4}>
      <Typography variant="h5" gutterBottom>
        Add value to numeric columns:
      </Typography>
      <TextField
        type="number"
        id="value_to_add"
        value={model.Configuration.addValue}
        onChange={handleChange}
        label="Value to add"
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
  )
}

ReactDOM.render(
  <Tool />,
  document.getElementById('app')
);
