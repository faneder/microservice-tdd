import React, { Component } from 'react';
import PropTypes from 'prop-types';
import usersApi from './apis/usersApi';
import UserList from './components/user/UserList';
import UserCreate from './components/user/UserCreate';

import withRootTheme from './withRootTheme';
// @material-ui/core components
import {
  withStyles,
  Grid,
  Paper,
  Typography
} from '@material-ui/core';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    padding: theme.spacing.unit * 3

  },
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing.unit * 2,
    marginTop: theme.spacing.unit * 2,
    textAlign: 'center',
  },
});

class App extends Component {
  static users;

  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: ''
    };
  }

  async componentDidMount() {
    this.getUsers();
  }

  handleChange = event => {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }

  getUsers = async () => {
    try {
        const response = await usersApi.get('/users');
        this.setState({
          users: response.data.data.users
        });
    } catch (err) {
        console.log(err)
    }
  }

  addUser = async event => {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password,
    }

    try {
      await usersApi.post('/users', data);
      this.getUsers();
      this.setState({ username: '', email: ''});
      console.log(this.state)
    } catch (err) {
      console.log(err)
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.container}>
         <Grid container spacing={24}>
           <Grid item xs={12}>
             <Typography variant="h5" component="h3">
               Create User
             </Typography>
             <Paper className={classes.paper}>
                <UserCreate
                  username={this.state.username}
                  email={this.state.email}
                  addUser={this.addUser}
                  handleChange={this.handleChange}
                />
             </Paper>
           </Grid>
           <Grid item xs={12}>
             <Typography variant="h5" component="h3">
               All Users
             </Typography>
             <UserList users={this.state.users} />
           </Grid>
        </Grid>
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRootTheme(withStyles(styles)(App));