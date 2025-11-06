import React, { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import TodoList from "../components/TodoList";
import AddTodoForm from "../components/AddTodoForm";
import projectService from "../services/projectService";

const ProjectPage = () => {
  const { projectId } = useParams();
  const todoListRef = useRef();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        setLoading(true);
        const response = await projectService.getProject(projectId);
        setProject(response.data);
        setError(null);
      } catch (err) {
        setError("Failed to load project");
        console.error("Error fetching project:", err);
      } finally {
        setLoading(false);
      }
    };

    if (projectId) {
      fetchProject();
    }
  }, [projectId]);

  const handleTodoAdded = (newTodo) => {
    if (todoListRef.current) {
      if (todoListRef.current.addTodo) {
        todoListRef.current.addTodo(newTodo);
      } else if (todoListRef.current.refreshTodos) {
        todoListRef.current.refreshTodos();
      }
    }
  };

  if (loading) {
    return (
      <>
        <div className="content-header">
          <h1 className="page-title">Loading...</h1>
        </div>
        <div className="content-body">
          <div className="loading">Loading project...</div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <div className="content-header">
          <h1 className="page-title">Error</h1>
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
        <h1 className="page-title">{project?.name || "Project"}</h1>
        <p className="page-subtitle">
          {project?.description || "Manage tasks in this project"}
        </p>
      </div>
      <div className="content-body">
        <AddTodoForm
          onTodoAdded={handleTodoAdded}
          defaultProjectId={parseInt(projectId)}
        />
        <TodoList ref={todoListRef} filterByProject={parseInt(projectId)} />
      </div>
    </>
  );
};

export default ProjectPage;
