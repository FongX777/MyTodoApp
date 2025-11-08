import React, { useState, useRef, useEffect } from "react";
import TodoList from "../components/TodoList";
import AddTodoForm from "../components/AddTodoForm";
import todoService from "../services/todoService";

const HomePage = () => {
  const todoListRef = useRef();
  const [refreshKey, setRefreshKey] = useState(0);
  // Persist recently created todo IDs so they remain visible in Inbox after page refresh.
  // Rationale: backend /todos endpoint defaults to limit=100; with >100 tasks, newest may be excluded from initial page.
  // We store recent IDs and refetch them individually on mount to ensure visibility.
  const RECENT_KEY = "inboxRecentTodoIds";
  const [recentTodoIds, setRecentTodoIds] = useState(() => {
    try {
      const raw = window.localStorage.getItem(RECENT_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  });

  // After mount (and whenever recentTodoIds changes), fetch any missing recent todos
  // that might not appear in the bulk list due to pagination limit.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      if (!todoListRef.current || recentTodoIds.length === 0) return;
      for (const id of recentTodoIds) {
        try {
          const res = await todoService.getTodo(id);
          if (!cancelled && todoListRef.current?.addTodo) {
            todoListRef.current.addTodo(res.data);
          }
        } catch (e) {
          // Ignore 404 or network errors for missing recent items.
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [recentTodoIds]);

  // Filter for inbox: only show unassigned tasks (project_id === null)
  // Inbox: show unassigned tasks, plus any just-created tasks (even if assigned)
  const inboxFilter = (todo) => {
    // Show todos that are truly unassigned OR were just created here (tracked)
    if (todo.project_id === null || todo.project_id === undefined) return true;
    if (recentTodoIds.includes(todo.id)) return true;
    return false;
  };

  const handleTodoAdded = (newTodo) => {
    setRecentTodoIds((prev) => {
      if (prev.includes(newTodo.id)) return prev;
      const next = [newTodo.id, ...prev].slice(0, 100); // cap size for safety
      try {
        window.localStorage.setItem(RECENT_KEY, JSON.stringify(next));
      } catch {}
      return next;
    });
    if (todoListRef.current) {
      if (todoListRef.current.addTodo) {
        todoListRef.current.addTodo(newTodo);
      } else if (todoListRef.current.refreshTodos) {
        todoListRef.current.refreshTodos();
      }
    }
  };

  // Periodic cleanup: remove IDs that are no longer in data (optional light maintenance)
  useEffect(() => {
    const interval = setInterval(() => {
      // Access current todos via ref if exposed
      const listInstance = todoListRef.current;
      if (!listInstance || !listInstance.refreshTodos) return; // no direct access to todos array here
      // Future improvement: trigger a refresh & prune IDs not found.
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  // Listen for todo moves from inbox to refresh the list
  useEffect(() => {
    const handleTodoMovedFromInbox = () => {
      if (todoListRef.current && todoListRef.current.refreshTodos) {
        todoListRef.current.refreshTodos();
      }
    };

    window.addEventListener("todo-moved-from-inbox", handleTodoMovedFromInbox);
    return () => {
      window.removeEventListener(
        "todo-moved-from-inbox",
        handleTodoMovedFromInbox
      );
    };
  }, []);

  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Inbox</h1>
        <p className="page-subtitle">Unassigned tasks</p>
      </div>
      <div className="content-body">
        <AddTodoForm onTodoAdded={handleTodoAdded} />
        <TodoList
          ref={todoListRef}
          customFilter={inboxFilter}
          key={refreshKey}
        />
      </div>
    </>
  );
};

export default HomePage;
