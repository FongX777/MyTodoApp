import axios from "axios";

const API_URL =
  process.env.REACT_APP_API_BASE_URL ||
  `${window.location.protocol}//${window.location.hostname}:8000`;

const client = axios.create({ baseURL: API_URL });

client.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API error", {
      url: err.config && err.config.url,
      method: err.config && err.config.method,
      status: err.response && err.response.status,
      data: err.response && err.response.data,
    });
    return Promise.reject(err);
  }
);

const getProjects = () => {
  return client.get(`/projects`);
};

const createProject = (project) => {
  return client.post(`/projects`, project);
};

const getProject = (id) => {
  return client.get(`/projects/${id}`);
};

const updateProject = (id, project) => {
  return client.put(`/projects/${id}`, project);
};

const projectService = {
  getProjects,
  createProject,
  getProject,
  updateProject,
};

export default projectService;
export { projectService };
