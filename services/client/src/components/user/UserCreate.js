import React from 'react';
import PropTypes from 'prop-types';
// @material-ui/core components
import {
  withStyles,
  MenuItem,
  TextField,
  Button
} from '@material-ui/core';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    margin: theme.spacing.unit,
  },
  textField: {
    marginBottom: theme.spacing.unit * 2,
  },
  button: {
    marginTop: theme.spacing.unit * 3,
  }
});

const UserCreate = props => {
  const { classes } = props;
  return (
     <form
       onSubmit={(event) => props.addUser(event)}
       className={classes.container}
       noValidate
       autoComplete="off"
     >
        <TextField
          label="email"
          className={classes.textField}
          name="email"
          value={props.email}
          onChange={props.handleChange}
          fullWidth
          required
       />
       <TextField
          label="username"
          className={classes.textField}
          name="username"
          value={props.username}
          onChange={props.handleChange}
          fullWidth
          required
       />
       <TextField
          name="password"
          label="Password"
          className={classes.textField}
          type="password"
          autoComplete="current-password"
          value={props.password}
          onChange={props.handleChange}
          fullWidth
          required
       />
       <Button
         type="submit"
         variant="contained"
         color="primary"
         className={classes.button}
       >
          Submit
       </Button>
     </form>
  )
};

UserCreate.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(UserCreate);