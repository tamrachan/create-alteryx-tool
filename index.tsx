import React, { useContext, useEffect} from 'react';
import ReactDOM from 'react-dom';
import { AyxAppWrapper, Box, Grid, Typography, makeStyles, Theme, TextField } from '@alteryx/ui';
import { Alteryx } from '@alteryx/icons';
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


  

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = Number(event.target.value);
    handleUpdateModel({ addValue: isNaN(value) ? 2 : value });
  };


  // Dev Harness Specific Code ---------- Start
  // The following code is specifically a dev harness functionality.
  // If you're developing a tool for Designer, you'll want to remove this
  // and check out our docs for guidance 
  useEffect(() => {
    handleUpdateModel(model)
  }, []);
  // Dev Harness Specific Code ---------- End

  return (
    <Box p={4}>
      <Typography variant="h5" gutterBottom>
        Add value to numeric columns:
      </Typography>
      <TextField
        type="number"
        value={model.addValue ?? 2}
        onChange={handleChange}
        label="Value to add"
      />
    </Box>
  );
};

//   return (
//     <Box p={4}>
//      <Grid container spacing={4} direction="column" alignItems="center">
//         <Grid item>
//           <Alteryx className={classes.alteryx} />
//         </Grid>
//         <Grid item>
//           <Typography variant="h3">
//             To get started, edit src/index.tsx
//           </Typography>
//         </Grid>
//       </Grid>
//     </Box>
//   )
// }

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
