# Tasks

## Frontend

- [x] f1 - Use '<https://fonts.google.com/icons>' Material icon to replace emojis like calendar, pencil,
- [x] f2 - Remove the "PENDING" "COMPLETED" labels on each task
- [x] f3 - Edit mode: Allow user to click the task to enter edit mode, just like when the click the edit pencil
- [x] f4 - Change name 'Home' to 'Inbox' to put tasks that are not assigned to any project
- [x] f5 - When a pending task is checked to be completed, change wait to 0.3s to disappear the task, so user can see the checkmark animation
- [] f6 - Bugfix: when drag and drop a todo to different projects, it'll jump to the project, don't do the jump, stay in the current view
- [] f7 - In 'Upcoming' view, show sections of dates for the next 7 days with weekday names, e.g. 'Monday, June 10', 'Tuesday, June 11', etc. Then put the todos under the corresponding date sections.
- [] f8 - Change the upper-left app name from 'AlertingScout' to 'TodoApp'
- [] f9 - For now the browser tab title is always 'React App', change it to 'TodoApp'

## Backend

- [] b1 - Able to use FastAPI's built-in swagger to render `/docs`, and add documentation for each endpoint
- [] b2 - use this grafna dashboard json to create a dashboard for backendfastapi metrics: <https://grafana.com/grafana/dashboards/16110-fastapi-observability/>
  - [] b2.1 - metrics: <https://github.com/prometheus/client_python>
