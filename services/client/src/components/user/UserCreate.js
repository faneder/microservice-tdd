import React from 'react';
import { Button, Form } from 'semantic-ui-react'

const UserCreate = props => {
  return (
    <Form onSubmit={(event) => props.addUser(event)}>
      <Form.Field>
        <label>email</label>
        <input
          name="email"
          placeholder='email'
          value={props.email}
          onChange={props.handleChange}
          required
        />
      </Form.Field>
      <Form.Field>
        <label>Username</label>
        <input
          name="username"
          placeholder='username'
          value={props.username}
          onChange={props.handleChange}
          required
        />
      </Form.Field>
      <Button type='submit'>Submit</Button>
    </Form>
  )
}

export default UserCreate;