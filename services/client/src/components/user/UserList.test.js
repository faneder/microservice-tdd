import React from 'react';
import renderer from 'react-test-renderer';
import { shallow } from 'enzyme';
import { Table } from 'semantic-ui-react'
import UserList from "./UserList";
import UserItem from "./UserItem";

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
  const wrapper = shallow(<UserList users={users} />);

  expect(wrapper.find(Table)).toHaveLength(1);
  expect(wrapper.find(Table.Header)).toHaveLength(1);
  expect(wrapper.find(Table.Body)).toHaveLength(1);
});

test('It renders 2 UserItems when 2 users ', () => {
  const wrapper = shallow(<UserList users={users} />);

  expect(wrapper.find(UserItem)).toHaveLength(2);
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UserList users={users}/>).toJSON();

  expect(tree).toMatchSnapshot();
});
