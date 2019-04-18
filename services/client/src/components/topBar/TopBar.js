import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import {
  withStyles,
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';

const styles = {
  root: {
    flexGrow: 1,
  },
  grow: {
    flexGrow: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
};

const items = [
  { key: '/', active: true, name: 'Home' },
  { key: '/about', name: 'About' },
  { key: '/user/status', name: 'User Status' },
];

const NavBar = (props) => {
  const { classes, title } = props;
  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <IconButton className={classes.menuButton} color="inherit" aria-label="Menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" color="inherit" className={classes.grow}>
            {title}
            { items.map((obj, key) =>
            <Button
              component={Link}
              name={obj.name}
              to={obj.key}
              key={key}
              color="inherit"
            >
              {obj.name}
            </Button>
            ) }
          </Typography>
          <Button color="inherit" component={Link} to='/login'>Login</Button>
          <Button color="inherit" component={Link} to='/logout'>Log Out</Button>
          <Button color="inherit" component={Link} to='/signup'>Sign Up</Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}

NavBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NavBar);
