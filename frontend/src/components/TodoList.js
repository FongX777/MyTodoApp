import React, { useState, useEffect } from "react";
import todoService from "../services/todoService";
import TodoItem from "./TodoItem";

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await todoService.getTodos();
        setTodos(response.data);
      } catch (err) {
        setError("Failed to load todos");
        console.error("Error fetching todos:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, []);

  if (loading) {
    return <div className="loading">Loading todos...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="todo-list">
      <h2 className="section-title">Tasks</h2>
      {todos.length === 0 ? (
        <div className="empty-state">
          <p>No tasks yet. Add your first task above!</p>
        </div>
      ) : (
        todos.map((todo) => <TodoItem key={todo.id} todo={todo} />)
      )}
    </div>
  );
};

export default TodoList;
