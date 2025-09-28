# Feature Specification: Todo List Application

**Feature Branch**: `001-create-a-todolist`
**Created**: 2025-09-28
**Status**: Draft
**Input**: User description: "create a todolist app, with frontend and backend spearated. A todo consists of id, title, notes, scheduled date/time, deadline date/time, tags, priority (low, mid, high, urgent), and projects. A project can contain many todos. A tag is created when a todo specifies one, and is removed when there's no todo having it. A user can list the todo, udpate it, move it between projects. When a todo is created, it by default goes to 'inbox' project. Also, I can list todos by date, projects, and tags."
**Clarifications**:
- "1. User can create todo with empty or duplicate titles 2. Yes, you can create project with duplicate name 3. you cannot move to non-existing projects 4. no need to auth user 5. project is allowed to be empty 6. Projects are created on the webpage, they can click and create project, and call api to create Also, todos and projects have 'status': undone, done, cancelled. And users can filter by status, and on the landing page, done or cancelled todos are considered 'completed', so they should be hidden. Also, when a project is 'done' or 'cancelled', all the remaining undone tasks are marked 'done' or 'cancelled' accordingly. On the sidebar, there are pages: - Today - Upcoming - Logbook (completed), sort by completed day - Projects"
- "- Define "upcoming": list the next 7 days of todos in secitons - Define Soring: by default created time, append the new one at the end, but in the projects, people can move todo's location - Canceling is not a delete, more like a soft delete, yes it can be undone."

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a user, I want to manage my tasks in a todolist application, so that I can organize my work and keep track of what I need to do.

### Acceptance Scenarios
1. **Given** I am on the main page, **When** I create a new todo, **Then** the new todo appears at the end of the 'inbox' project with 'undone' status.
2. **Given** I have a todo in the 'inbox' project, **When** I move it to a new project called 'Work', **Then** the todo is no longer in 'inbox' and appears in 'Work'.
3. **Given** I am viewing the list of todos, **When** I filter by status 'done', **Then** I only see todos with the 'done' status.
4. **Given** a project is marked as 'done', **When** it has undone todos, **Then** all its undone todos are marked as 'done'.
5. **Given** I am on the landing page, **When** there are 'done' or 'cancelled' todos, **Then** they are hidden.
6. **Given** I am on the sidebar, **When** I click on 'Upcoming', **Then** I see all todos for the next 7 days, grouped by day.
7. **Given** a todo is 'cancelled', **When** I go to the 'Logbook', **Then** I can see the cancelled todo and have an option to un-cancel it.

### Edge Cases
- A user can create a todo with an empty or duplicate title.
- A user can create a project with a duplicate name.
- A user cannot move a todo to a non-existing project.
- An empty project can exist.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST allow users to create a new todo.
- **FR-002**: System MUST allow users to update an existing todo.
- **FR-003**: System MUST allow users to list all todos.
- **FR-004**: System MUST allow users to move a todo between projects.
- **FR-005**: System MUST filter todos by date.
- **FR-006**: System MUST filter todos by project.
- **FR-007**: System MUST filter todos by tag.
- **FR-008**: A new todo MUST be placed in the 'inbox' project by default.
- **FR-009**: A tag MUST be created when a todo is created with a new tag.
- **FR-010**: A tag MUST be removed when no todos are associated with it anymore.
- **FR-011**: The application MUST have a separate frontend and backend.
- **FR-012**: System MUST support priorities for todos: low, mid, high, urgent.
- **FR-013**: No user authentication is required.
- **FR-014**: Projects can be empty.
- **FR-015**: Projects are created through the web page.
- **FR-016**: Todos and Projects MUST have a status: 'undone', 'done', 'cancelled'.
- **FR-017**: System MUST allow filtering todos by status.
- **FR-018**: 'Done' or 'cancelled' todos MUST be hidden on the landing page.
- **FR-019**: When a project's status changes to 'done' or 'cancelled', all its undone todos MUST have their status updated accordingly.
- **FR-020**: The sidebar MUST contain links to 'Today', 'Upcoming', 'Logbook', and 'Projects' pages.
- **FR-021**: The 'Logbook' page MUST show completed todos sorted by completion day.
- **FR-022**: The 'Upcoming' page MUST show todos for the next 7 days, sectioned by day.
- **FR-023**: Default sorting of todos MUST be by creation time (newest at the end).
- **FR-024**: Users MUST be able to manually reorder todos within a project.
- **FR-025**: The 'cancelled' status is a soft delete and can be undone.

### Key Entities *(include if feature involves data)*
- **Todo**: Represents a single task.
  - Attributes: id, title, notes, scheduled date/time, deadline date/time, tags, priority, project, status, order.
- **Project**: Represents a container for todos.
  - Attributes: name, status.
  - Relationship: A project can contain many todos.
- **Tag**: Represents a label for a todo.
  - Attributes: name.
  - Relationship: A todo can have many tags.

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Review checklist passed

---