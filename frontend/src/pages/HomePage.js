import React from 'react';
import TodoList from '../components/TodoList';
import AddTodoForm from '../components/AddTodoForm';
import ProjectList from '../components/ProjectList';

const HomePage = () => {
  return (
    <div>
      <h1>Todo List</h1>
      <AddTodoForm />
      <TodoList />
      <ProjectList />
    </div>
  );
};

export default HomePage;
