# Tasks: Todo List Application

**Input**: Design documents from `/specs/001-create-a-todolist/`

## Backend Tasks

### Phase 3.1: Setup
- [X] T001: Set up FastAPI project structure in `backend/app`.
- [X] T002: Configure database connection in `backend/app/main.py`.

### Phase 3.2: Models
- [X] T003 [P]: Create `Todo` SQLAlchemy model in `backend/app/models/todo.py`.
- [X] T004 [P]: Create `Project` SQLAlchemy model in `backend/app/models/project.py`.
- [X] T005 [P]: Create `Tag` SQLAlchemy model in `backend/app/models/tag.py`.

### Phase 3.3: Tests First (TDD)
- [X] T006 [P]: Write failing contract test for `POST /todos` in `backend/tests/test_todos.py` (not run).
- [X] T007 [P]: Write failing contract test for `GET /todos` in `backend/tests/test_todos.py` (not run).
- [X] T008 [P]: Write failing contract test for `GET /todos/{todo_id}` in `backend/tests/test_todos.py` (not run).
- [X] T009 [P]: Write failing contract test for `PUT /todos/{todo_id}` in `backend/tests/test_todos.py` (not run).
- [X] T010 [P]: Write failing contract test for `POST /projects` in `backend/tests/test_projects.py` (not run).
- [X] T011 [P]: Write failing contract test for `GET /projects` in `backend/tests/test_projects.py` (not run).
- [X] T012 [P]: Write failing contract test for `GET /projects/{project_id}` in `backend/tests/test_projects.py` (not run).
- [X] T013 [P]: Write failing contract test for `PUT /projects/{project_id}` in `backend/tests/test_projects.py` (not run).

### Phase 3.4: Core Implementation
- [X] T014: Implement repository for `Todo` in `backend/app/repository/todo_repo.py`.
- [X] T015: Implement repository for `Project` in `backend/app/repository/project_repo.py`.
- [X] T016: Implement `POST /todos` endpoint in `backend/app/routes/todos.py`.
- [X] T017: Implement `GET /todos` endpoint in `backend/app/routes/todos.py`.
- [X] T018: Implement `GET /todos/{todo_id}` endpoint in `backend/app/routes/todos.py`.
- [X] T019: Implement `PUT /todos/{todo_id}` endpoint in `backend/app/routes/todos.py`.
- [X] T020: Implement `POST /projects` endpoint in `backend/app/routes/projects.py`.
- [X] T021: Implement `GET /projects` endpoint in `backend/app/routes/projects.py`.
- [X] T022: Implement `GET /projects/{project_id}` endpoint in `backend/app/routes/projects.py`.
- [X] T023: Implement `PUT /projects/{project_id}` endpoint in `backend/app/routes/projects.py`.
- [X] T024: Include todo and project routers in `backend/app/main.py`.

## Frontend Tasks

### Phase 3.5: Setup
- [X] T025: Install `axios` for API communication in `frontend` (user needs to run `npm install`).

### Phase 3.6: Services
- [X] T026: Create `todoService.js` in `frontend/src/services` to interact with the backend todo endpoints.
- [X] T027: Create `projectService.js` in `frontend/src/services` to interact with the backend project endpoints.

### Phase 3.7: Components
- [X] T028 [P]: Create `TodoList` component in `frontend/src/components/TodoList.js`.
- [X] T029 [P]: Create `TodoItem` component in `frontend/src/components/TodoItem.js`.
- [X] T030 [P]: Create `ProjectList` component in `frontend/src/components/ProjectList.js`.
- [X] T031 [P]: Create `AddTodoForm` component in `frontend/src/components/AddTodoForm.js`.

### Phase 3.8: Pages
- [X] T032: Create `HomePage` in `frontend/src/pages/HomePage.js`.
- [X] T033: Create `TodayPage` in `frontend/src/pages/TodayPage.js`.
- [X] T034: Create `UpcomingPage` in `frontend/src/pages/UpcomingPage.js`.
- [X] T035: Create `LogbookPage` in `frontend/src/pages/LogbookPage.js`.

### Phase 3.9: Routing
- [X] T036: Set up routing for the pages in `frontend/src/App.js`.

## Dependencies
- Backend models (T003-T005) should be created before repositories and tests.
- Backend tests (T006-T013) must be written and failing before core implementation (T014-T024).
- Backend repositories (T014-T015) should be created before the endpoints that use them.
- Frontend services (T026-T027) should be created before the components that use them.
- Frontend components (T028-T031) should be created before the pages that use them.

## Parallel Example
```
# Launch backend model creation tasks together:
Task: "Create Todo SQLAlchemy model in backend/app/models/todo.py"
Task: "Create Project SQLAlchemy model in backend/app/models/project.py"
Task: "Create Tag SQLAlchemy model in backend/app/models/tag.py"

# Launch backend contract test tasks together:
Task: "Write failing contract test for POST /todos in backend/tests/test_todos.py"
Task: "Write failing contract test for GET /todos in backend/tests/test_todos.py"
...

# Launch frontend component creation tasks together:
Task: "Create TodoList component in frontend/src/components/TodoList.js"
Task: "Create TodoItem component in frontend/src/components/TodoItem.js"
...
```
