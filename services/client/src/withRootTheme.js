import React from 'react';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { blue, indigo } from '@material-ui/core/colors'

// A theme with custom primary and secondary color.
const theme = createMuiTheme({
  palette: {
    primary: {
      // main: indigo[700],
      main: blue[500],
      light: blue[100],
      dark: blue[700],
      contrastText: '#fff',
    },
    typography: {
      // Use the system font instead of the default Roboto font.
      fontFamily: [
        '"Lato"',
        'sans-serif'
      ].join(',')
    },
  },
});

const withRoot = (Component) => {
  const WithRoot = (props) => {
    // MuiThemeProvider makes the theme available down the React tree
    return (
      <MuiThemeProvider theme={theme}>
        {/* CssBaseline kick start an elegant, consistent, and simple baseline to build upon. */}
        <CssBaseline />
        <Component {...props} />
      </MuiThemeProvider>
    );
  };
  return WithRoot;
};

export default withRoot;
