import React, { useState, useRef, useEffect } from "react";
import TodoList from "../components/TodoList";
import AddTodoForm from "../components/AddTodoForm";

const HomePage = () => {
  const todoListRef = useRef();
  const [refreshKey, setRefreshKey] = useState(0);

  // Filter for inbox: only show unassigned tasks (project_id === null)
  const inboxFilter = (todo) => todo.project_id === null;

  const handleTodoAdded = (newTodo) => {
    if (todoListRef.current) {
      if (todoListRef.current.addTodo) {
        // Optimistic UI update
        todoListRef.current.addTodo(newTodo);
      } else if (todoListRef.current.refreshTodos) {
        todoListRef.current.refreshTodos();
      }
    }
  };

  // Listen for todo moves from inbox to refresh the list
  useEffect(() => {
    const handleTodoMovedFromInbox = () => {
      if (todoListRef.current && todoListRef.current.refreshTodos) {
        todoListRef.current.refreshTodos();
      }
    };

    window.addEventListener('todo-moved-from-inbox', handleTodoMovedFromInbox);
    return () => {
      window.removeEventListener('todo-moved-from-inbox', handleTodoMovedFromInbox);
    };
  }, []);

  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Inbox</h1>
        <p className="page-subtitle">Unassigned tasks</p>
      </div>
      <div className="content-body">
        <AddTodoForm onTodoAdded={handleTodoAdded} />
        <TodoList 
          ref={todoListRef} 
          customFilter={inboxFilter}
          key={refreshKey}
        />
      </div>
    </>
  );
};

export default HomePage;
