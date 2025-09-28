# Todo List Application

This is a simple todo list application with a React frontend and a Python FastAPI backend.

## How to get started in local

### Prerequisites
- Docker
- Docker Compose
- Node.js and npm

### Running the application
1.  **Start Docker:** Make sure your Docker daemon is running.
2.  **Install frontend dependencies:**
    ```bash
    cd frontend
    npm install
    cd ..
    ```
3.  **Run the application:**
    ```bash
    docker-compose up --build
    ```
4.  The frontend will be available at `http://localhost:3000`.
5.  The backend API will be available at `http://localhost:8000`.

### Testing
The backend tests are located in the `backend/tests` directory. You can run them with `pytest`.
Due to an issue with the Docker daemon, the tests were not run during the implementation. You can run them with the following command:
```bash
docker-compose exec backend pytest
```

The frontend is a simple prototype and does not have any tests yet.
