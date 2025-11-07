import React, { useRef } from "react";
import TodoList from "../components/TodoList";

const UpcomingPage = () => {
  const todoListRef = useRef();
  const customFilter = (t) => {
    if (!t.deadline_at) return false;
    const deadline = new Date(t.deadline_at);
    const today = new Date();
    const start = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate() + 1
    ); // tomorrow
    const end = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate() + 7
    ); // next 7 days
    return deadline >= start && deadline <= end;
  };
  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Upcoming</h1>
        <p className="page-subtitle">Plan ahead and stay organized</p>
      </div>
      <div className="content-body">
        <TodoList
          ref={todoListRef}
          initialStatusFilter="active"
          customFilter={customFilter}
        />
      </div>
    </>
  );
};

export default UpcomingPage;
