import React from 'react';
import renderer from 'react-test-renderer';
import { mount } from 'enzyme';

import UserList from "./UserList";
import UserItem from "./UserItem";

import {
  Table,
  TableHead,
  TableBody,
} from '@material-ui/core';

const users = [
  {
    'id': 1,
    'active': true,
    'email': 'eder@gmail.com',
    'username': 'eder'
  },
  {
    'id': 2,
    'active': true,
    'email': 'ping@ping.org',
    'username': 'ping'
  }
];

test('UserList renders properly', () => {
  const wrapper = mount(<UserList users={users} />);

  expect(wrapper.find(Table)).toHaveLength(1);
  expect(wrapper.find(TableHead)).toHaveLength(1);
  expect(wrapper.find(TableBody)).toHaveLength(1);
});

test('It renders 2 UserItems when 2 users ', () => {
  const wrapper = mount(<UserList users={users} />);

  expect(wrapper.find(UserItem)).toHaveLength(2);
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UserList users={users}/>).toJSON();

  expect(tree).toMatchSnapshot();
});
