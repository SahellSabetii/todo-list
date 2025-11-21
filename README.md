# ToDoList - Python OOP

A ToDoList application built with Python OOP principles, following clean architecture and best practices.

## 🚀 Features

### Project Management
- ✅ Create new projects with name and description
- ✅ Edit existing projects
- ✅ Delete projects with cascade delete (all tasks are automatically deleted)
- ✅ List all projects with task counts

### Task Management
- ✅ Add tasks to projects with title, description, and optional deadline
- ✅ Edit task details (title, description, status, deadline)
- ✅ Delete tasks
- ✅ Change task status (TODO → DOING → DONE)
- ✅ List tasks by project

### User Experience
- ✅ Clean, intuitive CLI interface
- ✅ Combined list/edit/delete views
- ✅ Persistent project and task IDs
- ✅ Input validation and error handling
- ✅ "Press Enter to continue" for better navigation

## 🛠️ Technology Stack

- **Python 3.10+** - Core programming language
- **Poetry** - Dependency management and packaging
- **Python-dotenv** - Environment configuration

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Poetry (package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/sahellsabetii/todo-list
   cd todo-list
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment configuration**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file to customize limits if needed.

4. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

## 🎯 Usage

### Running the Application
```bash
poetry run python -m src.todo_list.cli.console
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS_PER_PROJECT=50
MAX_PROJECT_NAME_LENGTH=30
MAX_PROJECT_DESCRIPTION_LENGTH=150
MAX_TASK_TITLE_LENGTH=30
MAX_TASK_DESCRIPTION_LENGTH=150
```

### Default Limits
- **Projects**: Maximum 10 projects
- **Tasks**: Maximum 50 tasks per project
- **Project Name**: 30 characters max
- **Project Description**: 150 characters max  
- **Task Title**: 30 characters max
- **Task Description**: 150 characters max


## 📋 Code Quality

This project follows strict code quality standards:

- **PEP 8 Compliance** - Python style guide
- **Type Hints** - Full type annotation coverage
- **Docstrings** - Comprehensive documentation
- **Single Responsibility** - Clean separation of concerns
- **Dependency Injection** - Loose coupling between components

### Coding Conventions

- **Imports**: Standard library → Third-party → Local modules
- **Naming**: 
  - Classes: `PascalCase` (e.g., `Project`, `Task`)
  - Functions/Variables: `snake_case` (e.g., `create_project`, `task_title`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_PROJECT_NAME_LENGTH`)
- **Line Length**: 88 characters (Black formatted)
- **Indentation**: 4 spaces

## 🔄 Development Workflow

### Git Branch Strategy
- `main` - Stable production releases
- `develop` - Main development branch
- `feature/*` - Feature development
- `fix/*` - Bug fixes
- `release/*` - Release preparation

### Commit Message Convention
```
<type>: <short description>

[optional body]
[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `chore`

**Examples**:
- `feat: add project creation with validation`
- `fix: resolve task status None issue`
- `docs: update README with installation instructions`

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
- Poetry for dependency management

---

**Happy Coding!** 🎉
