import React, { useState } from "react";
import todoService from "../services/todoService";

const TodoItem = ({ todo, onTodoUpdated, onTodoDeleted, projects = [] }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title || "");
  const [editDescription, setEditDescription] = useState(
    todo.description || ""
  );
  const [editPriority, setEditPriority] = useState(todo.priority || "low");
  const [editProjectId, setEditProjectId] = useState(todo.project_id || "");
  const [isUpdating, setIsUpdating] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const getPriorityClass = (priority) => {
    if (!priority) return "low";
    return priority.toLowerCase();
  };

  const formatStatus = (status) => {
    if (!status) return "pending";
    return status.replace("_", " ");
  };

  const formatPriority = (priority) => {
    if (!priority) return "Low";
    return priority.charAt(0).toUpperCase() + priority.slice(1);
  };

  const getProjectName = (projectId) => {
    if (!projectId || !projects.length) return null;
    const project = projects.find((p) => p.id === projectId);
    return project ? project.name : null;
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditTitle(todo.title || "");
    setEditDescription(todo.description || "");
    setEditPriority(todo.priority || "low");
    setEditProjectId(todo.project_id || "");
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) return;

    setIsUpdating(true);
    try {
      const response = await todoService.updateTodo(todo.id, {
        ...todo,
        title: editTitle.trim(),
        description: editDescription.trim(),
        priority: editPriority,
        project_id: editProjectId ? parseInt(editProjectId) : null,
      });

      if (onTodoUpdated) {
        onTodoUpdated(response.data);
      }
      setIsEditing(false);
    } catch (error) {
      console.error("Error updating todo:", error);
      alert("Failed to update task. Please try again.");
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await todoService.deleteTodo(todo.id);
      if (onTodoDeleted) {
        onTodoDeleted(todo.id);
      }
    } catch (error) {
      console.error("Error deleting todo:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleToggleComplete = async () => {
    const newStatus = todo.status === "completed" ? "pending" : "completed";
    setIsUpdating(true);
    try {
      const response = await todoService.updateTodo(todo.id, {
        ...todo,
        status: newStatus,
      });
      if (onTodoUpdated) {
        onTodoUpdated(response.data);
      }
    } catch (error) {
      console.error("Error updating todo status:", error);
    } finally {
      setIsUpdating(false);
    }
  };

  if (isEditing) {
    return (
      <div className="todo-item editing">
        <div className="todo-edit-form">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="edit-title-input"
            placeholder="Task title..."
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="edit-description-input"
            placeholder="Description..."
            rows="2"
          />
          <div className="edit-row">
            <div className="edit-field">
              <label>Priority</label>
              <select
                value={editPriority}
                onChange={(e) => setEditPriority(e.target.value)}
                className="edit-select"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div className="edit-field">
              <label>Project</label>
              <select
                value={editProjectId}
                onChange={(e) => setEditProjectId(e.target.value)}
                className="edit-select"
              >
                <option value="">No Project</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="edit-actions">
            <button
              onClick={handleSaveEdit}
              disabled={isUpdating || !editTitle.trim()}
              className="btn-mini btn-primary"
            >
              {isUpdating ? "Saving..." : "Save"}
            </button>
            <button
              onClick={handleCancelEdit}
              className="btn-mini btn-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`todo-item ${todo.status === "completed" ? "completed" : ""}`}
      draggable
      onDragStart={(e) => {
        e.dataTransfer.setData("text/plain", todo.id.toString());
      }}
    >
      <div className="todo-content">
        <div className="todo-header">
          <div className="todo-check-container">
            <input
              type="checkbox"
              checked={todo.status === "completed"}
              onChange={handleToggleComplete}
              className="todo-checkbox"
              disabled={isUpdating}
            />
          </div>
          <div className="todo-main">
            <h3 className="todo-title">{todo.title || "Untitled Task"}</h3>
            {todo.description && (
              <p className="todo-description">{todo.description}</p>
            )}
            <div className="todo-meta">
              {getProjectName(todo.project_id) && (
                <span className="todo-project">
                  📁 {getProjectName(todo.project_id)}
                </span>
              )}
              <span className="todo-status">{formatStatus(todo.status)}</span>
              <span
                className={`todo-priority ${getPriorityClass(todo.priority)}`}
              >
                {formatPriority(todo.priority)}
              </span>
            </div>
          </div>
        </div>
        <div className="todo-actions">
          <button
            onClick={handleEdit}
            className="todo-action-btn edit-btn"
            title="Edit task"
          >
            ✏️
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="todo-action-btn delete-btn"
            title="Delete task"
          >
            {isDeleting ? "..." : "🗑️"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TodoItem;
