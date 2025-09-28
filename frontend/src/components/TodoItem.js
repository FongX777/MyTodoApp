import React from "react";

const TodoItem = ({ todo }) => {
  const getPriorityClass = (priority) => {
    if (!priority) return "low";
    return priority.toLowerCase();
  };

  const formatStatus = (status) => {
    if (!status) return "pending";
    return status.replace("_", " ");
  };

  return (
    <div
      className={`todo-item ${todo.status === "completed" ? "completed" : ""}`}
    >
      <h3 className="todo-title">{todo.title || "Untitled Task"}</h3>
      <div className="todo-meta">
        <span className="todo-status">{formatStatus(todo.status)}</span>
        <span className={`todo-priority ${getPriorityClass(todo.priority)}`}>
          {todo.priority || "Low"} Priority
        </span>
      </div>
      {todo.description && (
        <p className="todo-description">{todo.description}</p>
      )}
    </div>
  );
};

export default TodoItem;
