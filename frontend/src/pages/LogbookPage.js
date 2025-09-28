import React, { useState, useEffect } from "react";
import todoService from "../services/todoService";
import projectService from "../services/projectService";

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
            const dateA = new Date(a.completed_at || a.updated_at);
            const dateB = new Date(b.completed_at || b.updated_at);
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

  const getProjectName = (projectId) => {
    if (!projectId || !projects.length) return null;
    const project = projects.find((p) => p.id === projectId);
    return project ? project.name : null;
  };

  const formatDate = (dateString) => {
    if (!dateString) return "Recently";
    const date = new Date(dateString);
    return (
      date.toLocaleDateString() +
      " at " +
      date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
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
          <div className="logbook-list">
            {completedTodos.map((todo) => (
              <div key={todo.id} className="logbook-item">
                <div className="logbook-item-content">
                  <div className="logbook-item-header">
                    <h3 className="logbook-item-title">
                      {todo.title || "Untitled Task"}
                    </h3>
                    <span className="completion-date">
                      {formatDate(todo.completed_at || todo.updated_at)}
                    </span>
                  </div>
                  {todo.description && (
                    <p className="logbook-item-description">
                      {todo.description}
                    </p>
                  )}
                  <div className="logbook-item-meta">
                    <span
                      className={`priority-badge ${todo.priority || "low"}`}
                    >
                      {(todo.priority || "Low").charAt(0).toUpperCase() +
                        (todo.priority || "low").slice(1)}
                    </span>
                    {getProjectName(todo.project_id) && (
                      <span className="project-badge">
                        {getProjectName(todo.project_id)}
                      </span>
                    )}
                  </div>
                </div>
                <div className="logbook-item-status">
                  <span className="checkmark">✓</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default LogbookPage;
