import React, { useState } from "react";
import todoService from "../services/todoService";

const AddTodoForm = ({ onTodoAdded, defaultProjectId }) => {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("low");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    try {
      const todoData = {
        title: title.trim(),
        priority,
        status: "pending",
        description: description.trim(),
      };

      // Add project_id if defaultProjectId is provided
      if (defaultProjectId) {
        todoData.project_id = defaultProjectId;
      }

      const response = await todoService.createTodo(todoData);
      setTitle("");
      setDescription("");
      setPriority("low");
      if (onTodoAdded) {
        onTodoAdded(response.data);
      }
    } catch (error) {
      console.error("Error creating todo:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-todo-form">
      <div className="form-group">
        <label htmlFor="title">Task Title</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title..."
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description (optional)</label>
        <input
          id="description"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add a description..."
        />
      </div>

      <div className="form-group">
        <label htmlFor="priority">Priority</label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
        >
          <option value="low">Low Priority</option>
          <option value="medium">Medium Priority</option>
          <option value="high">High Priority</option>
          <option value="urgent">Urgent Priority</option>
        </select>
      </div>

      <button
        type="submit"
        className="btn"
        disabled={isSubmitting || !title.trim()}
      >
        {isSubmitting ? "Adding..." : "Add Task"}
      </button>
    </form>
  );
};

export default AddTodoForm;
