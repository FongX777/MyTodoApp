import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
  useLocation,
} from "react-router-dom";
import HomePage from "./pages/HomePage";
import TodayPage from "./pages/TodayPage";
import UpcomingPage from "./pages/UpcomingPage";
import LogbookPage from "./pages/LogbookPage";
import projectService from "./services/projectService";
import AddProjectForm from "./components/AddProjectForm";

function Navigation() {
  const location = useLocation();
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

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">AlertingScout</h1>
      </div>
      <nav>
        <ul>
          <li>
            <Link to="/" className={location.pathname === "/" ? "active" : ""}>
              Home
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
                <li key={project.id} className="sidebar-project-item">
                  <span className="project-name" title={project.description}>
                    {project.name}
                  </span>
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
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
