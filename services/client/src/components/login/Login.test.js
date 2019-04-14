import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Login from './Login';

import {
  Button,
  TextField
} from '@material-ui/core';

const userForm = {
  email: '',
  password: '',
};

test('Login Form renders properly', () => {
  const component = <Login userForm={userForm} />
  const wrapper = shallow(component);
  // * Using dive() because Composition is now wrapped by the withStyles higher order component.
  const element = wrapper.dive().find('form')
  expect(element).toHaveLength(1);
  expect(element.find(TextField).get(0).props.name).toBe('email');
  expect(element.find(TextField).get(0).props.value).toBe(userForm.email);
  expect(element.find(TextField).get(1).props.name).toBe('password');
  expect(element.find(TextField).get(1).props.value).toBe(userForm.password);
  expect(element.find(Button).get(0).props.type).toBe('submit');
});

test('Login Form renders a snapshot properly', () => {
  const component = <Login userForm={userForm} />;
  const tree = renderer.create(component).toJSON();
  expect(tree).toMatchSnapshot();
});