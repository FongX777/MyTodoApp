# Quickstart

## Prerequisites
- Docker
- Docker Compose

## Running the application
1.  Clone the repository.
2.  Create a `.env` file in the `backend` directory with the following content:
    ```
    DATABASE_URL=postgresql://user:password@db:5432/tododb
    ```
3.  Run `docker-compose up --build` from the root of the repository.
4.  The frontend will be available at `http://localhost:3000`.
5.  The backend API will be available at `http://localhost:8000`.
