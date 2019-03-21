import React from "react";
import UserItem from './UserItem';
import { Table } from 'semantic-ui-react'

const UserList = (props) => (
  <Table singleLine>
    <Table.Header>
      <Table.Row>
        <Table.HeaderCell>Name</Table.HeaderCell>
        <Table.HeaderCell>email</Table.HeaderCell>
        <Table.HeaderCell>username</Table.HeaderCell>
        <Table.HeaderCell>active</Table.HeaderCell>
      </Table.Row>
    </Table.Header>

    <Table.Body>
      {
        props.users.map((user) => {
          return (
            <UserItem key={user.id} {...user} />
          )
        })
      }
    </Table.Body>
  </Table>
);

export default UserList