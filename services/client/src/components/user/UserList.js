import React from 'react';
import PropTypes from 'prop-types';
import UserItem from './UserItem';
// @material-ui/core components
import {
  withStyles,
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
  Paper
} from '@material-ui/core';

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
});

function UserList(props) {
  const { classes } = props;

  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell align="right">Name</TableCell>
            <TableCell align="right">email</TableCell>
            <TableCell align="right">username</TableCell>
            <TableCell align="right">active</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {
            props.users.map((user) => {
              return (
                <UserItem key={user.id} {...user} />
              )
            })
          }
        </TableBody>
      </Table>
    </Paper>
  );
}

UserList.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(UserList);
