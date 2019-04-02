import React from 'react';
import { shallow, mount } from 'enzyme';

import UserCreate from './UserCreate';

import {
  Button,
  TextField
} from '@material-ui/core';

test('UserCreate renders properly', () => {
  const wrapper = shallow(<UserCreate />);
  // * Using dive() because Composition is now wrapped by the withStyles higher order component.
  const element = wrapper.dive().find('form')
  expect(element).toHaveLength(1);
  expect(element.find(TextField).get(0).props.name).toBe('email');
  expect(element.find(TextField).get(1).props.name).toBe('username');
  expect(element.find(TextField).get(2).props.name).toBe('password');
  expect(element.find(Button).get(0).props.type).toBe('submit');
});