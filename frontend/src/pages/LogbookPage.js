import React, { useState, useEffect } from "react";
import todoService from "../services/todoService";
import projectService from "../services/projectService";
import TodoItem from "../components/TodoItem";

const LogbookPage = () => {
  const [completedTodos, setCompletedTodos] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCompletedTodos = async () => {
      try {
        setLoading(true);
        const [todosResponse, projectsResponse] = await Promise.all([
          todoService.getTodos(),
          projectService.getProjects(),
        ]);

        // Filter only completed todos and sort by completion date
        const completed = todosResponse.data
          .filter((todo) => todo.status === "completed")
          .sort((a, b) => {
            const dateA = new Date(a.completed_at || 0);
            const dateB = new Date(b.completed_at || 0);
            return dateB - dateA; // Most recent first
          });

        setCompletedTodos(completed);
        setProjects(projectsResponse.data);
        setError(null);
      } catch (err) {
        setError("Failed to load completed tasks");
        console.error("Error fetching completed todos:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCompletedTodos();
  }, []);

  const handleTodoUpdated = (updatedTodo) => {
    setCompletedTodos((prevTodos) =>
      prevTodos.map((todo) => (todo.id === updatedTodo.id ? updatedTodo : todo))
    );
  };

  const handleTodoDeleted = (deletedTodoId) => {
    setCompletedTodos((prevTodos) =>
      prevTodos.filter((todo) => todo.id !== deletedTodoId)
    );
  };

  if (loading) {
    return (
      <>
        <div className="content-header">
          <h1 className="page-title">Logbook</h1>
          <p className="page-subtitle">
            Review your completed tasks and achievements
          </p>
        </div>
        <div className="content-body">
          <div className="loading">Loading completed tasks...</div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <div className="content-header">
          <h1 className="page-title">Logbook</h1>
          <p className="page-subtitle">
            Review your completed tasks and achievements
          </p>
        </div>
        <div className="content-body">
          <div className="error">Error: {error}</div>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Logbook</h1>
        <p className="page-subtitle">
          Review your completed tasks and achievements
        </p>
      </div>
      <div className="content-body">
        {completedTodos.length === 0 ? (
          <div className="empty-state">
            <p>No completed tasks yet. Start checking off some todos!</p>
          </div>
        ) : (
          <div className="logbook-container">
            <div className="logbook-header">
              <h2 className="logbook-title">Completed Tasks</h2>
              <p className="logbook-subtitle">
                {completedTodos.length} task{completedTodos.length !== 1 ? 's' : ''} completed
              </p>
            </div>
            <div className="todo-items">
              {completedTodos.map((todo) => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  projects={projects}
                  onTodoUpdated={handleTodoUpdated}
                  onTodoDeleted={handleTodoDeleted}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default LogbookPage;
