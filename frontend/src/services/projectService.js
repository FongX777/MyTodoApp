import axios from "axios";

const API_URL = "http://localhost:8000";

const getProjects = () => {
  return axios.get(`${API_URL}/projects`);
};

const createProject = (project) => {
  return axios.post(`${API_URL}/projects`, project);
};

const getProject = (id) => {
  return axios.get(`${API_URL}/projects/${id}`);
};

const updateProject = (id, project) => {
  return axios.put(`${API_URL}/projects/${id}`, project);
};

const projectService = {
  getProjects,
  createProject,
  getProject,
  updateProject,
};

export default projectService;
export { projectService };
