from datetime import datetime
from typing import Optional, List

from ..main import ToDoListApp
from ..core.entities import Project, Task
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
    
    def display_main_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("          ToDoList Application")
        print("="*50)
        print("1. Projects Management")
        print("2. Tasks Management") 
        print("3. Show Validation Limits")
        print("0. Exit")
        print("="*50)
    
    def display_projects_menu(self) -> None:
        """Display projects management menu."""
        print("\n" + "="*50)
        print("          Projects Management")
        print("="*50)
        print("1. Create New Project")
        print("2. List All Projects (View/Edit/Delete)")
        print("3. Back to Main Menu")
        print("="*50)
    
    def display_tasks_menu(self) -> None:
        """Display tasks management menu."""
        print("\n" + "="*50)
        print("          Tasks Management")
        print("="*50)
        print("1. Add New Task")
        print("2. List Tasks by Project (View/Edit/Delete/Change Status)")
        print("3. Back to Main Menu")
        print("="*50)
    
    def get_user_input(self, prompt: str) -> str:
        """Get input from user with proper handling."""
        try:
            return input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            self.running = False
            return ""
    
    def get_int_input(self, prompt: str) -> Optional[int]:
        """Get integer input from user."""
        try:
            return int(self.get_user_input(prompt))
        except ValueError:
            return None
    
    def press_enter_to_continue(self) -> None:
        """Wait for user to press Enter to continue."""
        self.get_user_input("\nPress Enter to continue...")
    
    def create_project(self) -> None:
        """Handle project creation."""
        print("\n--- Create New Project ---")
        name = self.get_user_input("Project name: ")
        description = self.get_user_input("Project description: ")
        
        try:
            project = self.app.create_project(name, description)
            print(f"✅ Project '{project.name}' created successfully!")
        except (ValidationError, DuplicateProjectError, LimitExceededError) as e:
            print(f"❌ Error: {e}")
        
        self.press_enter_to_continue()
    
    def list_projects_with_actions(self) -> None:
        """List all projects with options to edit or delete."""
        while True:
            print("\n--- All Projects ---")
            projects = self.app.list_projects()
            
            if not projects:
                print("No projects found.")
                self.press_enter_to_continue()
                return
            
            print("\nCurrent Projects:")
            print("-" * 60)
            for project in projects:
                task_count = self.app.storage.get_task_count(project.project_id)
                print(f"ID: {project.project_id} - {project.name}")
                print(f"   Description: {project.description}")
                print(f"   Tasks: {task_count} | Created: {project.created_at.strftime('%Y-%m-%d')}")
                print("-" * 60)
            
            print("\nOptions:")
            print("1. Edit a Project")
            print("2. Delete a Project")
            print("3. View Tasks for a Project")
            print("4. Back to Projects Menu")
            
            choice = self.get_user_input("\nChoose an option (1-4): ")
            
            if choice == "1":
                self.edit_project_from_list()
            elif choice == "2":
                self.delete_project_from_list()
            elif choice == "3":
                self.view_tasks_for_project()
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def edit_project_from_list(self) -> None:
        """Edit a project by ID."""
        project_id = self.get_int_input("Enter the PROJECT ID to edit: ")
        
        if project_id is None:
            print("❌ Invalid project ID.")
            return
        
        project = self.app.storage.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        print(f"\nEditing Project: {project.name}")
        print(f"Current description: {project.description}")
        
        new_name = self.get_user_input(f"New name [{project.name}]: ") or project.name
        new_description = self.get_user_input(f"New description [{project.description}]: ") or project.description
        
        if new_name == project.name and new_description == project.description:
            print("No changes made.")
            return
        
        try:
            updated_project = self.app.edit_project(project.project_id, new_name, new_description)
            print(f"✅ Project '{updated_project.name}' updated successfully!")
        except (ProjectNotFoundError, ValidationError, DuplicateProjectError) as e:
            print(f"❌ Error: {e}")
        
        self.press_enter_to_continue()
    
    def delete_project_from_list(self) -> None:
        """Delete a project by ID."""
        project_id = self.get_int_input("Enter the PROJECT ID to delete: ")
        
        if project_id is None:
            print("❌ Invalid project ID.")
            return
        
        project = self.app.storage.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        task_count = self.app.storage.get_task_count(project.project_id)
        
        print(f"\n⚠️  WARNING: You are about to delete project '{project.name}'")
        print(f"This will also delete {task_count} task(s) in this project!")
        
        confirm = self.get_user_input("Are you sure? Type 'DELETE' to confirm: ")
        if confirm.upper() != 'DELETE':
            print("Deletion cancelled.")
            return
        
        try:
            if self.app.delete_project(project.project_id):
                print("✅ Project deleted successfully!")
                return
            else:
                print("❌ Error: Project not found")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.press_enter_to_continue()
    
    def view_tasks_for_project(self) -> None:
        """View tasks for a specific project by ID."""
        project_id = self.get_int_input("Enter the PROJECT ID to view tasks: ")
        
        if project_id is None:
            print("❌ Invalid project ID.")
            return
        
        project = self.app.storage.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        self.list_tasks_with_actions(project.project_id)
    
    def add_task(self) -> None:
        """Handle task creation."""
        print("\n--- Add New Task ---")
        
        projects = self.app.list_projects()
        if not projects:
            print("❌ No projects available. Please create a project first.")
            self.press_enter_to_continue()
            return
        
        print("\nAvailable Projects:")
        for project in projects:
            print(f"ID: {project.project_id} - {project.name}")
        
        project_id = self.get_int_input("\nSelect project ID: ")
        if project_id is None:
            print("❌ Invalid project ID.")
            self.press_enter_to_continue()
            return
        
        project = self.app.storage.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            self.press_enter_to_continue()
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
                self.press_enter_to_continue()
                return
        
        try:
            task = self.app.add_task(project.project_id, title, description, deadline)
            print(f"✅ Task '{task.title}' added to project '{project.name}' successfully!")
        except (ProjectNotFoundError, ValidationError, LimitExceededError) as e:
            print(f"❌ Error: {e}")
        
        self.press_enter_to_continue()
    
    def list_tasks_with_actions(self, project_id: int) -> None:
        """List tasks for a project with options to edit, delete, or change status."""
        try:
            project = self.app.storage.get_project(project_id)
            if not project:
                print("❌ Project not found.")
                return
            
            while True:
                tasks = self.app.list_tasks(project_id)
                
                if not tasks:
                    print(f"\nNo tasks found for project '{project.name}'.")
                    self.press_enter_to_continue()
                    return
                
                print(f"\nTasks for project: {project.name}")
                print("=" * 70)
                for task in tasks:
                    deadline_str = (
                        task.deadline.strftime("%Y-%m-%d") 
                        if task.deadline 
                        else "No deadline"
                    )
                    print(f"ID: {task.task_id} - {task.title}")
                    print(f"   Status: {task.status.value.upper()} | Deadline: {deadline_str}")
                    print(f"   Description: {task.description}")
                    print("-" * 70)
                
                print("\nTask Options:")
                print("1. Edit a Task")
                print("2. Delete a Task")
                print("3. Change Task Status")
                print("4. Back to Previous Menu")
                
                choice = self.get_user_input("\nChoose an option (1-4): ")
                
                if choice == "1":
                    if not self.edit_task_from_list(project_id):
                        continue
                elif choice == "2":
                    if self.delete_task_from_list(project_id):
                        break
                    else:
                        continue
                elif choice == "3":
                    if not self.change_task_status_from_list(project_id):
                        continue
                elif choice == "4":
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                
        except ProjectNotFoundError as e:
            print(f"❌ Error: {e}")
            self.press_enter_to_continue()
    
    def edit_task_from_list(self, project_id: int) -> bool:
        """Edit a task by ID. Returns True if list should refresh."""
        task_id = self.get_int_input("Enter the TASK ID to edit: ")
        
        if task_id is None:
            print("❌ Invalid task ID.")
            return False
        
        task = self.app.storage.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return False

        if task.project_id != project_id:
            print("❌ Task does not belong to this project.")
            return False
        
        print(f"\nEditing Task: {task.title}")
        print(f"Current status: {task.status.value.upper()}")
        print(f"Current description: {task.description}")
        
        new_title = self.get_user_input(f"New title [{task.title}]: ") or task.title
        new_description = self.get_user_input(f"New description [{task.description}]: ") or task.description
        
        print("Available statuses: TODO, DOING, DONE")
        status_str = self.get_user_input(f"New status [{task.status.value.upper()}]: ").upper()
        new_status = task.status
        if status_str:
            try:
                new_status = self.app.get_task_status_from_string(status_str)
            except InvalidStatusError as e:
                print(f"❌ Error: {e}")
                return False
        
        deadline_str = self.get_user_input("New deadline (YYYY-MM-DD, blank to keep current): ")
        new_deadline = task.deadline
        if deadline_str:
            try:
                new_deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("❌ Error: Invalid date format. Use YYYY-MM-DD")
                return False
        
        try:
            updated_task = self.app.edit_task(task.task_id, new_title, new_description, new_status, new_deadline)
            print(f"✅ Task '{updated_task.title}' updated successfully!")
        except (TaskNotFoundError, ValidationError) as e:
            print(f"❌ Error: {e}")
        
        self.press_enter_to_continue()
        return True
    
    def delete_task_from_list(self, project_id: int) -> bool:
        """Delete a task by ID. Returns True if list should refresh."""
        task_id = self.get_int_input("Enter the TASK ID to delete: ")
        
        if task_id is None:
            print("❌ Invalid task ID.")
            return False
        
        task = self.app.storage.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return False

        if task.project_id != project_id:
            print("❌ Task does not belong to this project.")
            return False
        
        confirm = self.get_user_input(f"Are you sure you want to delete task '{task.title}'? (y/N): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return False
        
        try:
            if self.app.delete_task(task.task_id):
                print("✅ Task deleted successfully!")
                return True
            else:
                print("❌ Error: Task not found")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def change_task_status_from_list(self, project_id: int) -> bool:
        """Change status of a task by ID. Returns True if list should refresh."""
        task_id = self.get_int_input("Enter the TASK ID to change status: ")
        
        if task_id is None:
            print("❌ Invalid task ID.")
            return False
        
        task = self.app.storage.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return False

        if task.project_id != project_id:
            print("❌ Task does not belong to this project.")
            return False
        
        print(f"\nCurrent status of '{task.title}': {task.status.value.upper()}")
        print("Available statuses: TODO, DOING, DONE")
        status_str = self.get_user_input("New status: ").upper()
        
        try:
            status = self.app.get_task_status_from_string(status_str)
            updated_task = self.app.change_task_status(task.task_id, status)
            print(f"✅ Task '{updated_task.title}' status changed to {updated_task.status.value.upper()}!")
        except (TaskNotFoundError, InvalidStatusError) as e:
            print(f"❌ Error: {e}")
            return False
        
        self.press_enter_to_continue()
        return True
    
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
        
        self.press_enter_to_continue()
    
    def projects_management(self) -> None:
        """Handle projects management submenu."""
        while True:
            self.display_projects_menu()
            choice = self.get_user_input("\nChoose an option (1-3): ")
            
            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.list_projects_with_actions()
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def tasks_management(self) -> None:
        """Handle tasks management submenu."""
        while True:
            self.display_tasks_menu()
            choice = self.get_user_input("\nChoose an option (1-3): ")
            
            if choice == "1":
                self.add_task()
            elif choice == "2":
                projects = self.app.list_projects()
                if not projects:
                    print("❌ No projects available. Please create a project first.")
                    self.press_enter_to_continue()
                    continue
                
                print("\nSelect a project to view tasks:")
                for project in projects:
                    task_count = self.app.storage.get_task_count(project.project_id)
                    print(f"ID: {project.project_id} - {project.name} ({task_count} tasks)")
                
                project_id = self.get_int_input("\nSelect project ID: ")
                if project_id is None:
                    print("❌ Invalid project ID.")
                    self.press_enter_to_continue()
                    continue
                
                project = self.app.storage.get_project(project_id)
                if not project:
                    print("❌ Project not found.")
                    self.press_enter_to_continue()
                    continue
                
                self.list_tasks_with_actions(project.project_id)
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def run(self) -> None:
        """Run the CLI application."""
        self.running = True
        print("🚀 Welcome to ToDoList Application!")
        
        while self.running:
            self.display_main_menu()
            choice = self.get_user_input("\nChoose an option (0-3): ")
            
            if choice == "1":
                self.projects_management()
            elif choice == "2":
                self.tasks_management()
            elif choice == "3":
                self.show_validation_limits()
            elif choice == "0":
                print("\n👋 Thank you for using ToDoList. Goodbye!")
                self.running = False
            else:
                print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = ToDoListCLI()
    cli.run()
