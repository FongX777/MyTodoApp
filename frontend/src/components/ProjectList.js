import React, { useState, useEffect } from "react";
import projectService from "../services/projectService";

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await projectService.getProjects();
        setProjects(response.data);
      } catch (err) {
        setError("Failed to load projects");
        console.error("Error fetching projects:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (loading) {
    return <div className="loading">Loading projects...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="projects-list">
      {projects.length === 0 ? (
        <div className="empty-state">
          <p>No projects yet. Create your first project!</p>
        </div>
      ) : (
        <div className="project-grid">
          {projects.map((project) => (
            <div key={project.id} className="project-item">
              <h3 className="project-title">
                {project.name || "Untitled Project"}
              </h3>
              {project.description && (
                <p className="project-description">{project.description}</p>
              )}
              <div className="project-meta">
                <span className="project-status">
                  {project.status || "Active"}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProjectList;
