import React from "react";
import TodoList from "../components/TodoList";
import AddTodoForm from "../components/AddTodoForm";

const HomePage = () => {
  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Manage your tasks efficiently</p>
      </div>
      <div className="content-body">
        <AddTodoForm />
        <TodoList />
      </div>
    </>
  );
};

export default HomePage;
