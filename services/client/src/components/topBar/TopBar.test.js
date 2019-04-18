import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';

import TopBar from './TopBar';

import {
  AppBar,
  Typography
} from '@material-ui/core';

const title = 'Title';

test('TopBar renders properly', () => {
  const wrapper = shallow(<TopBar title={title}/>);
  const element = wrapper.dive().find(AppBar)
  expect(element.length).toBe(1);
  expect(element.find(Typography).get(0).props.children[0]).toBe(title);
});

test('TopBar renders a snapshot properly', () => {
  const tree = renderer.create(
    <Router location="/">
      <TopBar title={title}/>
    </Router>
  ).toJSON();
  expect(tree).toMatchSnapshot();
});
