import React, {
  useState,
  useEffect,
  forwardRef,
  useImperativeHandle,
} from "react";
import todoService from "../services/todoService";
import projectService from "../services/projectService";
import TodoItem from "./TodoItem";

const FILTERS = [
  { id: "all", label: "All" },
  { id: "active", label: "Active" },
  { id: "completed", label: "Completed" },
];

const TodoList = forwardRef(({ filterByProject }, ref) => {
  const [todos, setTodos] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusFilter, setStatusFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const [todosResponse, projectsResponse] = await Promise.all([
        todoService.getTodos(),
        projectService.getProjects(),
      ]);
      setTodos(todosResponse.data);
      setProjects(projectsResponse.data);
      setError(null);
    } catch (err) {
      setError("Failed to load todos");
      console.error("Error fetching todos:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleTodoUpdated = (updatedTodo) => {
    setTodos((prevTodos) =>
      prevTodos.map((todo) =>
        todo.id === updatedTodo.id
          ? updatedTodo.hidden
            ? { ...updatedTodo, hidden: true } // Mark as hidden but keep in state temporarily
            : updatedTodo
          : todo
      )
    );

    // If todo is marked as hidden, remove it after a short delay
    if (updatedTodo.hidden) {
      setTimeout(() => {
        setTodos((prevTodos) =>
          prevTodos.filter((todo) => todo.id !== updatedTodo.id)
        );
      }, 100);
    }
  };

  const handleTodoDeleted = (deletedTodoId) => {
    setTodos((prevTodos) =>
      prevTodos.filter((todo) => todo.id !== deletedTodoId)
    );
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  useImperativeHandle(ref, () => ({
    refreshTodos: fetchTodos,
    addTodo: (todo) => {
      // Prevent duplicates if already loaded
      setTodos((prev) => {
        if (prev.find((t) => t.id === todo.id)) return prev;
        return [todo, ...prev];
      });
    },
  }));

  if (loading) {
    return <div className="loading">Loading todos...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  // Filter todos by project if filterByProject is provided
  // Also filter out completed tasks that are hidden (unless on logbook page)
  const baseTodos = filterByProject
    ? todos.filter(
        (todo) => todo.project_id === filterByProject && !todo.hidden
      )
    : todos.filter((todo) => !todo.hidden);

  const filteredByStatus = baseTodos.filter((todo) => {
    if (statusFilter === "completed") {
      return todo.status === "completed";
    }
    if (statusFilter === "active") {
      return todo.status !== "completed";
    }
    return true;
  });

  const filteredTodos = filteredByStatus.filter((todo) => {
    if (!searchTerm.trim()) {
      return true;
    }
    const term = searchTerm.toLowerCase();
    return (
      (todo.title || "").toLowerCase().includes(term) ||
      (todo.description || "").toLowerCase().includes(term)
    );
  });

  const completedCount = baseTodos.filter(
    (todo) => todo.status === "completed"
  ).length;
  const totalCount = baseTodos.length;
  const completionRate = totalCount
    ? Math.round((completedCount / totalCount) * 100)
    : 0;

  return (
    <div className="todo-list">
      <div className="todo-list-header">
        <div className="todo-list-heading">
          <h2 className="todo-list-title">Tasks</h2>
          <p className="todo-list-subtitle">
            {totalCount
              ? `${
                  totalCount - completedCount
                } open • ${completionRate}% complete`
              : "You're all caught up"}
          </p>
        </div>
        <div className="todo-list-controls">
          <div
            className="todo-filter-group"
            role="group"
            aria-label="Filter tasks by status"
          >
            {FILTERS.map((filter) => (
              <button
                key={filter.id}
                type="button"
                className={`todo-filter-btn ${
                  statusFilter === filter.id ? "active" : ""
                }`}
                onClick={() => setStatusFilter(filter.id)}
              >
                {filter.label}
              </button>
            ))}
          </div>
          <label className="todo-search" htmlFor="todo-search-input">
            <span className="todo-search-icon" aria-hidden="true">
              🔍
            </span>
            <input
              id="todo-search-input"
              type="search"
              placeholder="Search tasks"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              className="todo-search-input"
            />
          </label>
        </div>
        {totalCount > 0 && (
          <div className="todo-progress" aria-label="Task completion progress">
            <div
              className="todo-progress-bar"
              style={{ width: `${completionRate}%` }}
            />
          </div>
        )}
      </div>
      {filteredTodos.length === 0 ? (
        <div className="empty-state">
          <p>
            {filterByProject
              ? "No tasks in this project yet."
              : "No tasks yet. Add your first task above!"}
          </p>
        </div>
      ) : (
        <div className="todo-items">
          {filteredTodos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              projects={projects}
              onTodoUpdated={handleTodoUpdated}
              onTodoDeleted={handleTodoDeleted}
            />
          ))}
        </div>
      )}
    </div>
  );
});

export default TodoList;
