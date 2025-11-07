import React, { useState, useEffect } from "react";
import todoService from "../services/todoService";
import projectService from "../services/projectService";
import TodoItem from "../components/TodoItem";

const UpcomingPage = () => {
  const [todos, setTodos] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [todosResponse, projectsResponse] = await Promise.all([
          todoService.getTodos(),
          projectService.getProjects(),
        ]);
        setTodos(todosResponse.data);
        setProjects(projectsResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleTodoUpdated = (updatedTodo) => {
    setTodos((prevTodos) =>
      prevTodos.map((todo) => (todo.id === updatedTodo.id ? updatedTodo : todo))
    );
  };

  const handleTodoDeleted = (deletedTodoId) => {
    setTodos((prevTodos) =>
      prevTodos.filter((todo) => todo.id !== deletedTodoId)
    );
  };

  if (loading) {
    return (
      <div className="content-body">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  // Filter for upcoming tasks (tomorrow to next 7 days)
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  const nextWeek = new Date(today);
  nextWeek.setDate(nextWeek.getDate() + 7);

  const upcomingTodos = todos.filter((todo) => {
    if (!todo.deadline_at || todo.status === "completed") return false;
    const deadline = new Date(todo.deadline_at);
    deadline.setHours(0, 0, 0, 0);
    return deadline >= tomorrow && deadline <= nextWeek;
  });

  // Group todos by date
  const groupedTodos = {};
  for (let i = 1; i <= 7; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() + i);
    const dateKey = date.toISOString().split("T")[0];
    groupedTodos[dateKey] = {
      date: date,
      todos: [],
    };
  }

  upcomingTodos.forEach((todo) => {
    const deadline = new Date(todo.deadline_at);
    const dateKey = deadline.toISOString().split("T")[0];
    if (groupedTodos[dateKey]) {
      groupedTodos[dateKey].todos.push(todo);
    }
  });

  const weekdayNames = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Upcoming</h1>
        <p className="page-subtitle">Plan ahead and stay organized</p>
      </div>
      <div className="content-body">
        {upcomingTodos.length === 0 ? (
          <div className="empty-state">
            <p>No upcoming tasks in the next 7 days.</p>
          </div>
        ) : (
          <div className="upcoming-sections">
            {Object.keys(groupedTodos).map((dateKey) => {
              const section = groupedTodos[dateKey];
              if (section.todos.length === 0) return null;

              const weekday = weekdayNames[section.date.getDay()];
              const month = monthNames[section.date.getMonth()];
              const day = section.date.getDate();

              return (
                <div key={dateKey} className="upcoming-date-section">
                  <h3 className="upcoming-date-header">
                    {weekday}, {month} {day}
                  </h3>
                  <div className="todo-items">
                    {section.todos.map((todo) => (
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
              );
            })}
          </div>
        )}
      </div>
    </>
  );
};

export default UpcomingPage;
