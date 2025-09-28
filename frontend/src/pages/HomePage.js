import React, { useState, useRef } from "react";
import TodoList from "../components/TodoList";
import AddTodoForm from "../components/AddTodoForm";

const HomePage = () => {
  const todoListRef = useRef();

  const handleTodoAdded = (newTodo) => {
    if (todoListRef.current && todoListRef.current.refreshTodos) {
      todoListRef.current.refreshTodos();
    }
  };

  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Home</h1>
        <p className="page-subtitle">Manage your tasks efficiently</p>
      </div>
      <div className="content-body">
        <AddTodoForm onTodoAdded={handleTodoAdded} />
        <TodoList ref={todoListRef} />
      </div>
    </>
  );
};

export default HomePage;
