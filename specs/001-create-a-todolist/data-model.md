# Data Model

## Entities

### Todo
-   `id`: integer, primary key
-   `title`: string
-   `notes`: text
-   `scheduled_at`: datetime
-   `deadline_at`: datetime
-   `priority`: string (low, mid, high, urgent)
-   `status`: string (undone, done, cancelled)
-   `order`: integer
-   `project_id`: integer, foreign key to Project
-   `tags`: relationship to Tag

### Project
-   `id`: integer, primary key
-   `name`: string
-   `status`: string (undone, done, cancelled)
-   `todos`: relationship to Todo

### Tag
-   `id`: integer, primary key
-   `name`: string, unique
-   `todos`: relationship to Todo
