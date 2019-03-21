import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css'
import { Container, Header, Menu } from 'semantic-ui-react'
import usersApi from './apis/usersApi';
import UserList from './components/user/UserList';
import UserCreate from './components/user/UserCreate';
import logo from './logo.svg'; // Tell Webpack this JS file uses this image

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
      email: this.state.email
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
    return (
    <Container>
      <Menu stackable>
        <Menu.Item>
          <img src={logo} alt='Logo' />
        </Menu.Item>
        <Menu.Item name='features'>
          Features
        </Menu.Item>
      </Menu>
      <Header as='h2'>
        All Users
      </Header>
      <UserCreate
        username={this.state.username}
        email={this.state.email}
        addUser={this.addUser}
        handleChange={this.handleChange}
      />
      <UserList users={this.state.users} />
    </Container>
    );
  }
}

export default App;
