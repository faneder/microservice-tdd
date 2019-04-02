import React from "react";

import {
  TableCell,
  TableRow
} from '@material-ui/core';

const UserItem = (user) => {
  return (
    <TableRow key={user.id}>
      <TableCell align="right">{user.id}</TableCell>
      <TableCell align="right">{user.email}</TableCell>
      <TableCell align="right">{user.username}</TableCell>
      <TableCell align="right">{user.active ? 'o' : 'x'}</TableCell>
    </TableRow>
  )
};

export default UserItem;