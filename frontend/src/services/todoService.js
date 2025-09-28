import axios from "axios";

const API_URL = "http://localhost:8000";

const getTodos = () => {
  return axios.get(`${API_URL}/todos`);
};

const createTodo = (todo) => {
  return axios.post(`${API_URL}/todos`, todo);
};

const getTodo = (id) => {
  return axios.get(`${API_URL}/todos/${id}`);
};

const updateTodo = (id, todo) => {
  return axios.put(`${API_URL}/todos/${id}`, todo);
};

const deleteTodo = (id) => {
  return axios.delete(`${API_URL}/todos/${id}`);
};

const todoService = {
  getTodos,
  createTodo,
  getTodo,
  updateTodo,
  deleteTodo,
};

export default todoService;
export { todoService };
