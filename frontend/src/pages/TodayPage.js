import React, { useRef } from "react";
import TodoList from "../components/TodoList";
import AddTodoForm from "../components/AddTodoForm";

const TodayPage = () => {
  const todoListRef = useRef();
  const isToday = (t) => {
    if (!t.deadline_at) return false;
    const d = new Date(t.deadline_at);
    const now = new Date();
    return (
      d.getFullYear() === now.getFullYear() &&
      d.getMonth() === now.getMonth() &&
      d.getDate() === now.getDate()
    );
  };
  const customFilter = (t) => isToday(t);
  const handleTodoAdded = (newTodo) => {
    if (todoListRef.current?.addTodo) todoListRef.current.addTodo(newTodo);
    else if (todoListRef.current?.refreshTodos)
      todoListRef.current.refreshTodos();
  };
  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Today</h1>
        <p className="page-subtitle">Focus on what matters most today</p>
      </div>
      <div className="content-body">
        <AddTodoForm onTodoAdded={handleTodoAdded} />
        <TodoList
          ref={todoListRef}
          initialStatusFilter="active"
          customFilter={customFilter}
        />
      </div>
    </>
  );
};

export default TodayPage;
