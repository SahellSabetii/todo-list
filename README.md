# ToDoList - Python OOP

A ToDoList application built with Python OOP principles, now with PostgreSQL database integration.

### 🗄️ Database & Persistence
- ✅ **PostgreSQL Integration** - Professional-grade relational database
- ✅ **SQLAlchemy ORM** - Object-Relational Mapping for type-safe database operations
- ✅ **Alembic Migrations** - Version-controlled database schema management
- ✅ **Data Persistence** - Your data survives application restarts

### 🏗️ Architecture Improvements
- ✅ **Layered Architecture** - Clear separation of concerns
- ✅ **Repository Pattern** - Abstracted data access layer
- ✅ **Dependency Injection** - Loose coupling between components

### 🔧 Enhanced Features
- ✅ **Enum-based Task Status** - Type-safe status management
- ✅ **Optional Deadlines** - Flexible task scheduling
- ✅ **Auto-close Overdue Tasks** - Scheduled background processing
- ✅ **Cascade Deletes** - Automatic cleanup with foreign key constraints
- ✅ **Edit Operations** - Update projects and tasks

## 🛠️ Technology Stack

- **Python** - Core programming language
- **PostgreSQL** - Professional relational database
- **SQLAlchemy** - Modern ORM with type safety
- **Alembic** - Database migration framework
- **Poetry** - Dependency management and packaging
- **Python-dotenv** - Environment configuration
- **Click** - Command-line interface framework

## 📦 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Poetry (package manager)
- PostgreSQL (installed and running)

### Quick Start

1. **Clone and setup**
   ```bash
   git clone https://github.com/sahellsabetii/todo-list
   cd todo-list
   poetry install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

3. **Setup PostgreSQL Database**
   ```bash
   # Create database (run in psql or pgAdmin)
   CREATE DATABASE todolist;
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Run the application**
   ```bash
   ./main.py --help
   ```

## 🎯 Usage Examples

### Project Management
```bash
# Create a project
./main.py project create --name "Work Tasks" --description "Professional tasks and deadlines"

# List all projects
./main.py project list

# Edit a project
./main.py project edit --id 1 --name "Updated Project" --description "New description"

# Delete a project (automatically deletes all tasks)
./main.py project delete 1
```

### Task Management
```bash
# Create a task without deadline
./main.py task create --title "Write documentation" --project-id 1

# Create a task with deadline
./main.py task create --title "Submit report" --project-id 1 --deadline "2024-01-20 17:00"

# List all tasks
./main.py task list

# List tasks for a specific project
./main.py task list-by-project --project-id 1

# Edit a task
./main.py task edit --id 1 --title "Updated task title" --description "New description" --status in_progress

# Close a task
./main.py task close 1

# List overdue tasks
./main.py task overdue
```

### Edit Command Examples
```bash
# Edit project name and description
./main.py project edit --id 1 --name "New Project Name" --description "Updated description"

# Edit task title and status
./main.py task edit --id 5 --title "Revised Task Title" --status in_progress

# Edit task deadline
./main.py task edit --id 5 --deadline "2024-02-01 14:30"

# Remove task deadline
./main.py task edit --id 5 --deadline ""

# Edit multiple task properties
./main.py task edit --id 5 --title "Final Version" --description "Complete all items" --status done
```

### Automated Features
```bash
# Manually close all overdue tasks
./main.py autoclose-overdue

# Schedule auto-close (add to crontab)
*/15 * * * * cd /path/to/todolist && ./main.py autoclose-overdue
```

## 🔄 Available Commands

### Project Commands
- `project create` - Create new project
- `project list` - List all projects
- `project edit` - Edit project details
- `project delete` - Delete project and its tasks

### Task Commands
- `task create` - Create new task
- `task list` - List all tasks
- `task edit` - Edit task details
- `task close` - Mark task as done
- `task overdue` - List overdue tasks

### System Commands
- `autoclose-overdue` - Close all overdue tasks

## 📊 Code Quality & Standards

### Architecture Patterns
- **Repository Pattern** - Clean data access abstraction
- **Dependency Injection** - Testable and maintainable code
- **Layered Architecture** - Separation of concerns
- **ORM Best Practices** - Type-safe database operations

## 🧪 Development

### Creating Migrations
```bash
# After model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Database Management
```bash
# Check migration history
alembic history

# Create specific migration
alembic revision -m "add_new_feature"

# Check current migration
alembic current
```

## 🔄 Git Workflow

### Branch Strategy
- `main` - Stable production releases
- `develop` - Main development branch
- `feature/*` - Feature development

### Commit Convention
```
<type>: <short description>

[optional body]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Sahel Sabeti - sabetisahel@gmail.com

## 🙏 Acknowledgments

- Python Software Foundation
- SQLAlchemy ORM team
- PostgreSQL community

---
