import axios from "axios";

// Prefer environment variable, fallback to same host :8000 (backend) for dev
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

const getTodos = () => {
  return client.get(`/todos`);
};

const createTodo = (todo) => {
  return client.post(`/todos`, todo);
};

const getTodo = (id) => {
  return client.get(`/todos/${id}`);
};

const updateTodo = (id, todo) => {
  return client.put(`/todos/${id}`, todo);
};

const deleteTodo = (id) => {
  return client.delete(`/todos/${id}`);
};

const reorderTodos = (todoOrders) => {
  return client.put(`/todos/reorder`, { todo_orders: todoOrders });
};

const todoService = {
  getTodos,
  createTodo,
  getTodo,
  updateTodo,
  deleteTodo,
  reorderTodos,
};

export default todoService;
export { todoService };
