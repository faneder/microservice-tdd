import React from "react";
import { Table } from 'semantic-ui-react'

const UserItem = (user) => {
  return (
    <Table.Row>
      <Table.Cell>{user.id}</Table.Cell>
      <Table.Cell>{user.email}</Table.Cell>
      <Table.Cell>{user.username}</Table.Cell>
      <Table.Cell>{user.active ? 'o' : 'x'}</Table.Cell>
    </Table.Row>
  )
}

export default UserItem;