import click
from datetime import datetime

from todo_list.db.session import db
from todo_list.repositories.project_repository import ProjectRepository
from todo_list.repositories.task_repository import TaskRepository
from todo_list.services.project_service import ProjectService
from todo_list.services.task_service import TaskService
from todo_list.commands.autoclose_overdue import autoclose_overdue_cmd
from todo_list.models.task import TaskStatus


class TodoCLI:
    def __init__(self):
        self.session = db.get_session()
        project_repo = ProjectRepository(self.session)
        task_repo = TaskRepository(self.session)
        self.project_service = ProjectService(project_repo)
        self.task_service = TaskService(task_repo)
    
    def close_session(self):
        self.session.close()

@click.group()
def cli():
    pass

@cli.group()
def project():
    pass

@cli.group()
def task():
    pass

# Project Commands
@project.command()
@click.option('--name', required=True, help='Project name')
@click.option('--description', help='Project description')
def create(name, description):
    """Create a new project"""
    todo = TodoCLI()
    try:
        project = todo.project_service.create_project(name, description)
        click.echo(f"✅ Project '{project.name}' created with ID: {project.id}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

@project.command()
def list():
    """List all projects"""
    todo = TodoCLI()
    try:
        projects = todo.project_service.get_all_projects()
        if not projects:
            click.echo("No projects found")
            return
        
        for project in projects:
            tasks = todo.task_service.get_tasks_by_project(project.id)
            task_count = len(tasks)
            
            pending_tasks = len([t for t in tasks if t.status != 'done'])
            done_tasks = len([t for t in tasks if t.status == 'done'])
            
            click.echo(f"📁 {project.id}: {project.name}")
            click.echo(f"   Tasks: {task_count} total ({pending_tasks} pending, {done_tasks} done)")
            
            if project.description:
                click.echo(f"   Description: {project.description}")
            click.echo(f"   Created: {project.created_at}")
            click.echo()
    finally:
        todo.close_session()

@project.command()
@click.argument('project_id', type=int)
def delete(project_id):
    """Delete a project"""
    todo = TodoCLI()
    try:
        todo.project_service.delete_project(project_id)
        click.echo(f"✅ Project {project_id} deleted")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

@project.command()
@click.argument('project_id', type=int)
@click.option('--name', help='New project name')
@click.option('--description', help='New project description')
def edit(project_id, name, description):
    """Edit an existing project"""
    todo = TodoCLI()
    try:
        if not name and not description:
            click.echo("❌ Error: At least one of --name or --description must be provided")
            return
        
        project = todo.project_service.update_project(project_id, name, description)
        click.echo(f"✅ Project {project_id} updated successfully")
        click.echo(f"   Name: {project.name}")
        if project.description:
            click.echo(f"   Description: {project.description}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

# Task Commands
@task.command()
@click.option('--title', required=True, help='Task title')
@click.option('--project-id', required=True, type=int, help='Project ID')
@click.option('--description', help='Task description')
@click.option('--deadline', help='Deadline (YYYY-MM-DD HH:MM)')
def create(title, project_id, description, deadline):
    """Create a new task"""
    todo = TodoCLI()
    try:
        deadline_dt = None
        if deadline:
            deadline_dt = datetime.strptime(deadline, '%Y-%m-%d %H:%M')
        
        task = todo.task_service.create_task(title, project_id, description, deadline_dt)
        click.echo(f"✅ Task '{task.title}' created with ID: {task.id}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

@task.command()
def list():
    """List all tasks"""
    todo = TodoCLI()
    try:
        tasks = todo.task_service.get_all_tasks()
        if not tasks:
            click.echo("No tasks found")
            return
        
        for task in tasks:
            status_icon = "✅" if task.status == TaskStatus.DONE.value else "⏳"
            click.echo(f"{status_icon} {task.id}: {task.title} [Project: {task.project.name}]")
            if task.description:
                click.echo(f"   Description: {task.description}")
            if task.deadline:
                overdue = " (OVERDUE!)" if task.deadline < datetime.now() and task.status != TaskStatus.DONE.value else ""
                click.echo(f"   Deadline: {task.deadline}{overdue}")
            click.echo(f"   Status: {task.status}")
            click.echo()
    finally:
        todo.close_session()

@task.command()
@click.option('--project-id', required=True, type=int, help='Project ID to list tasks for')
def list_by_project(project_id):
    """List all tasks for a specific project"""
    todo = TodoCLI()
    try:
        project = todo.project_service.get_project(project_id)
        if not project:
            click.echo(f"❌ Project with ID {project_id} not found")
            return
        tasks = todo.task_service.get_tasks_by_project(project_id)
        if not tasks:
            click.echo(f"📭 No tasks found for project '{project.name}'")
            return
        click.echo(f"📋 Tasks for project '{project.name}':")
        click.echo("=" * 50)

        for task in tasks:
            status_icon = "✅" if task.status == 'done' else "⏳"
            overdue_indicator = ""
            if task.deadline and task.deadline < datetime.now() and task.status != 'done':
                overdue_indicator = " 🚨 OVERDUE!"
            click.echo(f"{status_icon} {task.id}: {task.title}{overdue_indicator}")
            if task.description:
                click.echo(f"   Description: {task.description}")
            click.echo(f"   Status: {task.status}")
            if task.deadline:
                click.echo(f"   Deadline: {task.deadline}")
            if task.closed_at:
                click.echo(f"   Closed: {task.closed_at}")
            click.echo()
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

@task.command()
@click.argument('task_id', type=int)
def close(task_id):
    """Close a task"""
    todo = TodoCLI()
    try:
        task = todo.task_service.close_task(task_id)
        click.echo(f"✅ Task '{task.title}' closed")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

@task.command()
def overdue():
    """List overdue tasks"""
    todo = TodoCLI()
    try:
        tasks = todo.task_service.get_overdue_tasks()
        if not tasks:
            click.echo("No overdue tasks found")
            return
        
        click.echo("🚨 OVERDUE TASKS:")
        for task in tasks:
            click.echo(f"   ⚠️  {task.id}: {task.title} [Project: {task.project.name}]")
            click.echo(f"      Deadline: {task.deadline}")
            click.echo()
    finally:
        todo.close_session()

@task.command()
@click.argument('task_id', type=int)
@click.option('--title', help='New task title')
@click.option('--description', help='New task description')
@click.option('--deadline', help='New deadline (YYYY-MM-DD HH:MM)')
@click.option('--status', type=click.Choice(['todo', 'doing', 'done']), help='New status')
def edit(task_id, title, description, deadline, status):
    """Edit an existing task"""
    todo = TodoCLI()
    try:
        if not any([title, description, deadline, status]):
            click.echo("❌ Error: At least one option must be provided (--title, --description, --deadline, or --status)")
            return
        
        update_data = {}
        
        if title:
            update_data['title'] = title
        
        if description is not None:  # Allow empty description
            update_data['description'] = description
        
        if deadline:
            update_data['deadline'] = datetime.strptime(deadline, '%Y-%m-%d %H:%M')
        
        if status:
            status_enum = TaskStatus[status.upper()]
            update_data['status'] = status_enum
        
        task = todo.task_service.update_task(task_id, **update_data)
        click.echo(f"✅ Task {task_id} updated successfully")
        click.echo(f"   Title: {task.title}")
        click.echo(f"   Status: {task.status}")
        if task.description:
            click.echo(f"   Description: {task.description}")
        if task.deadline:
            click.echo(f"   Deadline: {task.deadline}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
    finally:
        todo.close_session()

cli.add_command(autoclose_overdue_cmd, name="autoclose-overdue")


if __name__ == '__main__':
    cli()
