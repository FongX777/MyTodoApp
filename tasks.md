# Tasks

## Frontend

- [x] f1 - Use '<https://fonts.google.com/icons>' Material icon to replace emojis like calendar, pencil,
- [x] f2 - Remove the "PENDING" "COMPLETED" labels on each task
- [x] f3 - Edit mode: Allow user to click the task to enter edit mode, just like when the click the edit pencil
- [x] f4 - Change name 'Home' to 'Inbox' to put tasks that are not assigned to any project
- [x] f5 - When a pending task is checked to be completed, change wait to 0.3s to disappear the task, so user can see the checkmark animation
- [x] f6 - Bugfix: when drag and drop a todo to different projects, it'll jump to the project, don't do the jump, stay in the current view
- [x] f7 - In 'Upcoming' view, show sections of dates for the next 7 days with weekday names, e.g. 'Monday, June 10', 'Tuesday, June 11', etc. Then put the todos under the corresponding date sections.
- [x] f8 - Change the upper-left app name from 'AlertingScout' to 'TodoApp'
- [x] f9 - For now the browser tab title is always 'React App', change it to 'TodoApp'
- [x] f10 - when I double click anyplace inside a todo item (not just the pencil icon), it should enter edit mode
- [] f11 - Improve the look of the panel 'logbook', instead of a plain list, make it look like a todo card like in other panels
- [] f12 - The inbox should only show tasks that are not assigned to any project, and if i drag and drop a todo item from inbox to a project, it should be removed from inbox view immediately after the drop, and show a toast notification "Moved to [Project Name]" for 1 seconds at bottom-left corner
- [] f13 - When I drag and drop a todo item to change its project (e.g., from project 1 to project 2), after the drop, show a small toast notification at the bottom-left corner that says "Moved to [Project Name]" for 1 seconds, and then disappear, and the task should disappear from the current view (because it's now in a different project). If the user is in 'inbox' view, after the drop, the task should disappear from inbox view immediately.
- [] f14 - In Inbox, Today, project view, when I click 'All', show all tasks including completed ones, but the pending tasks should be on top, and completed tasks should be at the bottom.
- [] f15 - In Project view, users can drag and drop tasks to reorder them within the project. The order should be saved in the backend, and when the user refreshes the page, the order should be preserved. (including backend changes)

## Backend

- [] b1 - Able to use FastAPI's built-in swagger to render `/docs`, and add documentation for each endpoint
- [] b2 - use this grafna dashboard json to create a dashboard for backendfastapi metrics: <https://grafana.com/grafana/dashboards/16110-fastapi-observability/>
  - [] b2.1 - metrics: <https://github.com/prometheus/client_python>
- [] b3 - write a script to periodically (every 24 hours) call apis to test the backend performance and availability, and log the results to a file for monitoring purposes.
