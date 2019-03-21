import React from 'react';
import { shallow } from 'enzyme';
import { Table } from 'semantic-ui-react'

import UserItem from "./UserItem";

const users = {
  'id': 1,
  'active': true,
  'email': 'eder@gmail.com',
  'username': 'eder'
};

it('it renders one line per UserItem', () => {
  const wrapper = shallow(<UserItem {...users} />);

  expect(wrapper.find(Table.Row).length).toEqual(1);
});

it('it renders 4 columns per UserItem', () => {
  const wrapper = shallow(<UserItem {...users} />);

  expect(wrapper.find(Table.Cell).length).toEqual(4);
});

it('shows the text for each UserItem', () => {
  const wrapper = shallow(<UserItem {...users} />);

  expect(wrapper.render().text()).toContain('eder@gmail.com');
  expect(wrapper.render().text()).toContain('eder');
  expect(wrapper.render().text()).toContain('1');
  expect(wrapper.render().text()).toContain('o');
});

it('shows inactive when user not active', () => {
  const user = {
    'active': false
  };
  const wrapper = shallow(<UserItem {...user} />);

  expect(wrapper.render().text()).toContain('x');
});
