import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";
import HomePage from "./pages/HomePage";
import TodayPage from "./pages/TodayPage";
import UpcomingPage from "./pages/UpcomingPage";
import LogbookPage from "./pages/LogbookPage";
import ProjectPage from "./pages/ProjectPage";
import { projectService } from "./services/projectService";
import { todoService } from "./services/todoService";
import AddProjectForm from "./components/AddProjectForm";
import { ToastProvider, useToast } from "./components/ToastProvider";

function Navigation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [projects, setProjects] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await projectService.getProjects();
        setProjects(response.data);
      } catch (error) {
        console.error("Error fetching projects:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const handleProjectAdded = (newProject) => {
    setProjects((prev) => [...prev, newProject]);
    setShowAddForm(false);
  };

  const handleTodoDrop = async (todoId, newProjectId) => {
    try {
      const existing = await todoService.getTodo(todoId);
      const full = existing.data;
      const payload = { ...full, project_id: newProjectId };
      await todoService.updateTodo(todoId, payload);
      
      // Show toast notification
      const projectName = projects.find(p => p.id === newProjectId)?.name || 'Project';
      showToast(`Moved to ${projectName}`);
      
      // Trigger refresh for inbox view if moving from inbox
      if (location.pathname === '/' && full.project_id === null) {
        window.dispatchEvent(new CustomEvent('todo-moved-from-inbox'));
      }
      
      // Stay on current view after drag and drop
    } catch (error) {
      console.error("Error updating todo project:", error);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add("drag-over");
  };

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove("drag-over");
  };

  const handleDrop = (e, projectId) => {
    e.preventDefault();
    e.currentTarget.classList.remove("drag-over");
    const todoId = parseInt(e.dataTransfer.getData("text/plain"));
    if (todoId) {
      handleTodoDrop(todoId, projectId);
    }
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">TodoApp</h1>
      </div>
      <nav>
        <ul>
          <li>
            <Link to="/" className={location.pathname === "/" ? "active" : ""}>
              Inbox
            </Link>
          </li>
          <li>
            <Link
              to="/today"
              className={location.pathname === "/today" ? "active" : ""}
            >
              Today
            </Link>
          </li>
          <li>
            <Link
              to="/upcoming"
              className={location.pathname === "/upcoming" ? "active" : ""}
            >
              Upcoming
            </Link>
          </li>
          <li>
            <Link
              to="/logbook"
              className={location.pathname === "/logbook" ? "active" : ""}
            >
              Logbook
            </Link>
          </li>
        </ul>
      </nav>

      <div className="sidebar-section">
        <div className="sidebar-section-header">
          <h3 className="sidebar-section-title">Projects</h3>
          <button
            className="add-project-btn"
            onClick={() => setShowAddForm(!showAddForm)}
            title="Add new project"
          >
            +
          </button>
        </div>

        {showAddForm && (
          <AddProjectForm
            onProjectAdded={handleProjectAdded}
            onCancel={() => setShowAddForm(false)}
          />
        )}

        <div className="projects-list-sidebar">
          {loading ? (
            <div className="sidebar-loading">Loading...</div>
          ) : projects.length === 0 ? (
            <div className="sidebar-empty">No projects yet</div>
          ) : (
            <ul className="sidebar-projects">
              {projects.map((project) => (
                <li
                  key={project.id}
                  className="sidebar-project-item drop-zone"
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={(e) => handleDrop(e, project.id)}
                >
                  <Link
                    to={`/project/${project.id}`}
                    className="project-name project-link"
                    title={project.description}
                  >
                    {project.name}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/today" element={<TodayPage />} />
            <Route path="/upcoming" element={<UpcomingPage />} />
            <Route path="/logbook" element={<LogbookPage />} />
            <Route path="/project/:projectId" element={<ProjectPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
