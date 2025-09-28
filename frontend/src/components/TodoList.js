import React, {
  useState,
  useEffect,
  forwardRef,
  useImperativeHandle,
} from "react";
import todoService from "../services/todoService";
import projectService from "../services/projectService";
import TodoItem from "./TodoItem";

const TodoList = forwardRef(({ filterByProject }, ref) => {
  const [todos, setTodos] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
  }));

  if (loading) {
    return <div className="loading">Loading todos...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  // Filter todos by project if filterByProject is provided
  // Also filter out completed tasks that are hidden (unless on logbook page)
  const filteredTodos = filterByProject
    ? todos.filter(
        (todo) => todo.project_id === filterByProject && !todo.hidden
      )
    : todos.filter((todo) => !todo.hidden);

  return (
    <div className="todo-list">
      <h2 className="section-title">Tasks</h2>
      {filteredTodos.length === 0 ? (
        <div className="empty-state">
          <p>
            {filterByProject
              ? "No tasks in this project yet."
              : "No tasks yet. Add your first task above!"}
          </p>
        </div>
      ) : (
        filteredTodos.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            projects={projects}
            onTodoUpdated={handleTodoUpdated}
            onTodoDeleted={handleTodoDeleted}
          />
        ))
      )}
    </div>
  );
});

export default TodoList;
