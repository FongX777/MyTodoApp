import React, { useState } from "react";
import projectService from "../services/projectService";

const AddProjectForm = ({ onProjectAdded, onCancel }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;

    setIsSubmitting(true);
    try {
      const newProject = await projectService.createProject({
        name: name.trim(),
        description: description.trim(),
        status: "active",
      });
      setName("");
      setDescription("");
      if (onProjectAdded) {
        onProjectAdded(newProject.data);
      }
    } catch (error) {
      console.error("Error creating project:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-project-form">
      <div className="form-group">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Project name..."
          required
          className="project-name-input"
        />
      </div>

      <div className="form-group">
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)..."
          className="project-description-input"
        />
      </div>

      <div className="form-actions">
        <button
          type="submit"
          className="btn-mini btn-primary"
          disabled={isSubmitting || !name.trim()}
        >
          {isSubmitting ? "Adding..." : "Add"}
        </button>
        <button
          type="button"
          className="btn-mini btn-secondary"
          onClick={onCancel}
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default AddProjectForm;
