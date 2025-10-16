from datetime import datetime
from typing import Optional

from ..main import ToDoListApp
from ..core.exceptions import (
    ValidationError, DuplicateProjectError, ProjectNotFoundError,
    TaskNotFoundError, LimitExceededError, InvalidStatusError
)
from ..config import Config


class ToDoListCLI:
    """Command Line Interface for ToDoList application."""
    
    def __init__(self) -> None:
        self.app = ToDoListApp()
        self.running = False
    
    def display_menu(self) -> None:
        print("\n=== ToDoList Application ===")
        print("1. Create Project")
        print("2. List Projects")
        print("3. Edit Project")
        print("4. Delete Project")
        print("5. Add Task")
        print("6. List Tasks")
        print("7. Change Task Status")
        print("8. Edit Task")
        print("9. Delete Task")
        print("L. Show Validation Limits")
        print("0. Exit")
    
    def get_user_input(self, prompt: str) -> str:
        try:
            return input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            self.running = False
            return ""
    
    def get_int_input(self, prompt: str) -> Optional[int]:
        try:
            return int(self.get_user_input(prompt))
        except ValueError:
            return None
    
    def create_project(self) -> None:
        print("\n--- Create New Project ---")
        name = self.get_user_input("Project name: ")
        description = self.get_user_input("Project description: ")
        
        try:
            project = self.app.create_project(name, description)
            print(f"✅ Project '{project.name}' created successfully!")
        except (ValidationError, DuplicateProjectError, LimitExceededError) as e:
            print(f"❌ Error: {e}")
    
    def list_projects(self) -> None:
        print("\n--- All Projects ---")
        projects = self.app.list_projects()
        
        if not projects:
            print("No projects found.")
            return
        
        for project in projects:
            task_count = self.app.storage.get_task_count(project.project_id)
            print(f"ID: {project.project_id} | Name: {project.name} | "
                  f"Tasks: {task_count} | Created: {project.created_at.strftime('%Y-%m-%d')}")
            print(f"   Description: {project.description}")
            print("-" * 50)
    
    def edit_project(self) -> None:
        print("\n--- Edit Project ---")
        project_id = self.get_int_input("Project ID to edit: ")
        
        if project_id is None:
            print("❌ Error: Please enter a valid project ID")
            return
        
        name = self.get_user_input("New project name: ")
        description = self.get_user_input("New project description: ")
        
        try:
            project = self.app.edit_project(project_id, name, description)
            print(f"✅ Project '{project.name}' updated successfully!")
        except (ProjectNotFoundError, ValidationError, DuplicateProjectError) as e:
            print(f"❌ Error: {e}")
    
    def delete_project(self) -> None:
        print("\n--- Delete Project ---")
        project_id = self.get_int_input("Project ID to delete: ")
        
        if project_id is None:
            print("❌ Error: Please enter a valid project ID")
            return
        
        confirm = self.get_user_input(
            "Are you sure? This will delete all tasks in the project! (y/N): "
        )
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        try:
            if self.app.delete_project(project_id):
                print("✅ Project deleted successfully!")
            else:
                print("❌ Error: Project not found")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def add_task(self) -> None:
        print("\n--- Add New Task ---")
        project_id = self.get_int_input("Project ID: ")
        
        if project_id is None:
            print("❌ Error: Please enter a valid project ID")
            return
        
        title = self.get_user_input("Task title: ")
        description = self.get_user_input("Task description: ")
        deadline_str = self.get_user_input("Deadline (YYYY-MM-DD, optional): ")
        
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("❌ Error: Invalid date format. Use YYYY-MM-DD")
                return
        
        try:
            task = self.app.add_task(project_id, title, description, deadline)
            print(f"✅ Task '{task.title}' added successfully!")
        except (ProjectNotFoundError, ValidationError, LimitExceededError) as e:
            print(f"❌ Error: {e}")
    
    def list_tasks(self) -> None:
        print("\n--- List Tasks ---")
        project_id = self.get_int_input("Project ID: ")
        
        if project_id is None:
            print("❌ Error: Please enter a valid project ID")
            return
        
        try:
            tasks = self.app.list_tasks(project_id)
            project = self.app.storage.get_project(project_id)
            
            print(f"\nTasks for project: {project.name}")
            print("=" * 60)
            
            if not tasks:
                print("No tasks found for this project.")
                return
            
            for task in tasks:
                deadline_str = (
                    task.deadline.strftime("%Y-%m-%d") 
                    if task.deadline 
                    else "No deadline"
                )
                print(f"ID: {task.task_id} | Title: {task.title}")
                print(f"   Status: {task.status.value.upper()} | Deadline: {deadline_str}")
                print(f"   Description: {task.description}")
                print("-" * 50)
                
        except ProjectNotFoundError as e:
            print(f"❌ Error: {e}")
    
    def change_task_status(self) -> None:
        print("\n--- Change Task Status ---")
        task_id = self.get_int_input("Task ID: ")
        
        if task_id is None:
            print("❌ Error: Please enter a valid task ID")
            return
        
        print("Available statuses: TODO, DOING, DONE")
        status_str = self.get_user_input("New status: ").upper()
        
        try:
            status = self.app.get_task_status_from_string(status_str)
            task = self.app.change_task_status(task_id, status)
            print(f"✅ Task '{task.title}' status changed to {task.status.value.upper()}!")
        except (TaskNotFoundError, InvalidStatusError) as e:
            print(f"❌ Error: {e}")
    
    def edit_task(self) -> None:
        print("\n--- Edit Task ---")
        task_id = self.get_int_input("Task ID to edit: ")
        
        if task_id is None:
            print("❌ Error: Please enter a valid task ID")
            return
        
        title = self.get_user_input("New task title: ")
        description = self.get_user_input("New task description: ")
        
        print("Available statuses: TODO, DOING, DONE")
        status_str = self.get_user_input("New status: ").upper()
        
        deadline_str = self.get_user_input("New deadline (YYYY-MM-DD, optional): ")
        
        try:
            status = self.app.get_task_status_from_string(status_str)
        except InvalidStatusError as e:
            print(f"❌ Error: {e}")
            return
        
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("❌ Error: Invalid date format. Use YYYY-MM-DD")
                return
        
        try:
            task = self.app.edit_task(task_id, title, description, status, deadline)
            print(f"✅ Task '{task.title}' updated successfully!")
        except (TaskNotFoundError, ValidationError) as e:
            print(f"❌ Error: {e}")
    
    def delete_task(self) -> None:
        print("\n--- Delete Task ---")
        task_id = self.get_int_input("Task ID to delete: ")
        
        if task_id is None:
            print("❌ Error: Please enter a valid task ID")
            return
        
        confirm = self.get_user_input("Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        try:
            if self.app.delete_task(task_id):
                print("✅ Task deleted successfully!")
            else:
                print("❌ Error: Task not found")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_validation_limits(self) -> None:
        """Display current validation limits."""
        limits = Config.get_all_limits()
        print("\n--- Validation Limits ---")
        print(f"Max Projects: {limits['max_projects']}")
        print(f"Max Tasks per Project: {limits['max_tasks_per_project']}")
        print(f"Max Project Name Length: {limits['max_project_name_length']} characters")
        print(f"Max Project Description Length: {limits['max_project_description_length']} characters")
        print(f"Max Task Title Length: {limits['max_task_title_length']} characters")
        print(f"Max Task Description Length: {limits['max_task_description_length']} characters")
    
    def run(self) -> None:
        self.running = True
        print("Welcome to ToDoList Application!")
        
        while self.running:
            self.display_menu()
            choice = self.get_user_input("\nEnter your choice: ")
            
            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.list_projects()
            elif choice == "3":
                self.edit_project()
            elif choice == "4":
                self.delete_project()
            elif choice == "5":
                self.add_task()
            elif choice == "6":
                self.list_tasks()
            elif choice == "7":
                self.change_task_status()
            elif choice == "8":
                self.edit_task()
            elif choice == "9":
                self.delete_task()
            elif choice.lower() == "l":
                self.show_validation_limits()
            elif choice == "0":
                print("Goodbye!")
                self.running = False
            else:
                print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = ToDoListCLI()
    cli.run()
