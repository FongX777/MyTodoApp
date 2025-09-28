import React, { useState, useEffect } from 'react';
import todoService from '../services/todoService';
import TodoItem from './TodoItem';

const TodoList = () => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    todoService.getTodos().then((response) => {
      setTodos(response.data);
    });
  }, []);

  return (
    <div>
      <h2>Todo List</h2>
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  );
};

export default TodoList;
