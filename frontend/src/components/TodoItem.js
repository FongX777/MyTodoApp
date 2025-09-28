import React from 'react';

const TodoItem = ({ todo }) => {
  return (
    <div>
      <h3>{todo.title}</h3>
      <p>Status: {todo.status}</p>
      <p>Priority: {todo.priority}</p>
    </div>
  );
};

export default TodoItem;
