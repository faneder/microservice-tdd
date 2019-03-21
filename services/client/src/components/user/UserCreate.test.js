import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UserCreate from './UserCreate';
import { Button, Form } from 'semantic-ui-react'

test('UserCreate renders properly', () => {
  const wrapper = shallow(<UserCreate />);
  const element = wrapper.find(Form);

  expect(element.find('input').length).toBe(2);
  expect(element.find('input').get(0).props.name).toBe('email');
  expect(element.find('input').get(1).props.name).toBe('username');
  expect(element.find(Button).get(0).props.type).toBe('submit');
});