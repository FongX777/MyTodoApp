import React, { useState, useEffect, useRef } from "react";
import todoService from "../services/todoService";
import projectService from "../services/projectService";

const AddTodoForm = ({ onTodoAdded, defaultProjectId }) => {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("low");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [deadlineDate, setDeadlineDate] = useState("");
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(
    defaultProjectId || null
  );
  const [showPriority, setShowPriority] = useState(false);
  const [showProject, setShowProject] = useState(false);
  const [showCalendar, setShowCalendar] = useState(false);
  const popoverRef = useRef(null);
  const priorityListRef = useRef(null);

  useEffect(() => {
    if (!defaultProjectId) {
      (async () => {
        try {
          const res = await projectService.getProjects();
          setProjects(res.data);
        } catch (err) {
          console.error("Error loading projects", err);
        }
      })();
    }
  }, [defaultProjectId]);

  // Listen for external project creation
  useEffect(() => {
    const handler = (e) => {
      setProjects((prev) => {
        if (prev.find((p) => p.id === e.detail.id)) return prev;
        return [...prev, e.detail];
      });
    };
    window.addEventListener("project:created", handler);
    return () => window.removeEventListener("project:created", handler);
  }, []);

  useEffect(() => {
    const handler = (e) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target)) {
        setShowPriority(false);
        setShowProject(false);
        setShowCalendar(false);
      }
    };
    document.addEventListener("mousedown", handler);
    const keyHandler = (e) => {
      if (e.key === "Escape") {
        setShowPriority(false);
        setShowProject(false);
        setShowCalendar(false);
      }
      if (showPriority && (e.key === "ArrowDown" || e.key === "ArrowUp")) {
        e.preventDefault();
        const items = priorityListRef.current?.querySelectorAll(
          ".things-popover-item"
        );
        if (!items || items.length === 0) return;
        let index = Array.from(items).findIndex((el) =>
          el.classList.contains("selected")
        );
        if (index === -1) index = 0;
        if (e.key === "ArrowDown") index = (index + 1) % items.length;
        if (e.key === "ArrowUp")
          index = (index - 1 + items.length) % items.length;
        items.forEach((el) => el.classList.remove("kbd-focus"));
        items[index].classList.add("kbd-focus");
        items[index].focus();
      }
    };
    document.addEventListener("keydown", keyHandler);
    return () => document.removeEventListener("mousedown", handler);
  }, [showPriority]);

  // Remove key handler cleanup separately
  useEffect(() => {
    const keyHandler = (e) => {
      if (e.key === "Escape") {
        setShowPriority(false);
        setShowProject(false);
        setShowCalendar(false);
      }
    };
    document.addEventListener("keydown", keyHandler);
    return () => document.removeEventListener("keydown", keyHandler);
  }, []);

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
        deadline_at: deadlineDate ? new Date(deadlineDate).toISOString() : null,
      };

      if (selectedProjectId) {
        todoData.project_id = selectedProjectId;
      }

      const response = await todoService.createTodo(todoData);
      setTitle("");
      setDescription("");
      setPriority("low");
      setDeadlineDate("");
      if (onTodoAdded) {
        onTodoAdded(response.data);
      }
    } catch (error) {
      console.error("Error creating todo:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const todayStr = new Date().toISOString().substring(0, 10);

  return (
    <form onSubmit={handleSubmit} className="things-add-todo" ref={popoverRef}>
      <input
        className="things-input things-title-input"
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New To-Do"
        required
        aria-label="New to-do title"
      />
      <textarea
        className="things-textarea"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Notes"
        rows={3}
        aria-label="To-do notes"
      />
      <div className="things-action-row">
        <button
          type="submit"
          className="things-primary-btn"
          disabled={isSubmitting || !title.trim()}
        >
          {isSubmitting ? "Adding..." : "Add Task"}
        </button>
        <div className="things-selected-chips">
          {selectedProjectId && (
            <span className="things-chip" title="Project selected">
              <span className="material-icons">folder</span>{" "}
              {projects.find((p) => p.id === selectedProjectId)?.name ||
                "Project"}
            </span>
          )}
          <span className={`things-chip priority-${priority}`} title="Priority">
            <span className="material-icons">flag</span>{" "}
            {priority.charAt(0).toUpperCase() + priority.slice(1)}
          </span>
          {deadlineDate && (
            <span className="things-chip" title="Deadline">
              <span className="material-icons">event</span> {deadlineDate}
            </span>
          )}
        </div>
        <div className="things-icon-group">
          {!defaultProjectId && (
            <button
              type="button"
              className={`things-icon-btn ${showProject ? "active" : ""}`}
              onClick={() => {
                setShowProject((s) => !s);
                setShowPriority(false);
                setShowCalendar(false);
              }}
              title="Select Project"
              aria-label="Select project"
            >
              <span className="material-icons">folder</span>
            </button>
          )}
          <button
            type="button"
            className={`things-icon-btn ${showPriority ? "active" : ""}`}
            onClick={() => {
              setShowPriority((s) => !s);
              setShowProject(false);
              setShowCalendar(false);
            }}
            title="Set Priority"
            aria-label="Set priority"
          >
            <span className="material-icons">flag</span>
          </button>
          <button
            type="button"
            className={`things-icon-btn ${showCalendar ? "active" : ""}`}
            onClick={() => {
              setShowCalendar((s) => !s);
              setShowProject(false);
              setShowPriority(false);
            }}
            title="Set Deadline"
            aria-label="Set deadline"
          >
            <span className="material-icons">event</span>
          </button>
        </div>
      </div>
      {(showPriority || showProject || showCalendar) && (
        <>
          <div
            className="things-overlay"
            onClick={() => {
              setShowPriority(false);
              setShowProject(false);
              setShowCalendar(false);
            }}
          />
          <div className="things-popovers">
            {showProject && !defaultProjectId && (
              <div className="things-popover">
                <div className="things-popover-title">Project</div>
                {projects.length === 0 ? (
                  <div className="things-popover-empty">No projects</div>
                ) : (
                  <ul className="things-popover-list" role="listbox">
                    {projects.map((p) => (
                      <li key={p.id}>
                        <button
                          type="button"
                          className={`things-popover-item ${
                            selectedProjectId === p.id ? "selected" : ""
                          }`}
                          onClick={() => {
                            setSelectedProjectId(p.id);
                            setShowProject(false);
                          }}
                          tabIndex={0}
                        >
                          {p.name}
                        </button>
                      </li>
                    ))}
                    <li>
                      <button
                        type="button"
                        className={`things-popover-item ${
                          selectedProjectId === null ? "selected" : ""
                        }`}
                        onClick={() => {
                          setSelectedProjectId(null);
                          setShowProject(false);
                        }}
                        tabIndex={0}
                      >
                        No Project
                      </button>
                    </li>
                  </ul>
                )}
              </div>
            )}
            {showPriority && (
              <div className="things-popover">
                <div className="things-popover-title">Priority</div>
                <ul
                  className="things-popover-list"
                  role="listbox"
                  ref={priorityListRef}
                >
                  {[
                    { id: "low", label: "Low" },
                    { id: "medium", label: "Medium" },
                    { id: "high", label: "High" },
                    { id: "urgent", label: "Urgent" },
                  ].map((opt) => (
                    <li key={opt.id}>
                      <button
                        type="button"
                        className={`things-popover-item ${
                          priority === opt.id ? "selected" : ""
                        }`}
                        onClick={() => {
                          setPriority(opt.id);
                          setShowPriority(false);
                        }}
                        tabIndex={0}
                      >
                        {opt.label}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {showCalendar && (
              <div className="things-popover">
                <div className="things-popover-title">Deadline</div>
                <div className="things-popover-calendar">
                  <input
                    type="date"
                    value={deadlineDate}
                    onChange={(e) => setDeadlineDate(e.target.value)}
                    className="things-inline-date"
                  />
                  <div className="things-date-shortcuts">
                    <button
                      type="button"
                      onClick={() => setDeadlineDate(todayStr)}
                    >
                      Today
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        const d = new Date();
                        d.setDate(d.getDate() + 1);
                        setDeadlineDate(d.toISOString().substring(0, 10));
                      }}
                    >
                      Tomorrow
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        const d = new Date();
                        const day = d.getDay();
                        const offset = (1 - day + 7) % 7 || 7; // Next Monday
                        d.setDate(d.getDate() + offset);
                        setDeadlineDate(d.toISOString().substring(0, 10));
                      }}
                    >
                      Next Mon
                    </button>
                  </div>
                  {deadlineDate && (
                    <button
                      type="button"
                      className="things-clear-date"
                      onClick={() => setDeadlineDate("")}
                    >
                      Clear
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </form>
  );
};

export default AddTodoForm;
