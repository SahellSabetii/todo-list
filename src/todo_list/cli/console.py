import click
from datetime import datetime

from todo_list.db.session import db
from todo_list.repositories.project_repository import ProjectRepository
from todo_list.repositories.task_repository import TaskRepository
from todo_list.services.project_service import ProjectService
from todo_list.services.task_service import TaskService
from todo_list.commands.autoclose_overdue import autoclose_overdue_cmd


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
    """Todo List Application with PostgreSQL"""
    pass

@cli.group()
def project():
    """Project management commands"""
    pass

@cli.group()
def task():
    """Task management commands"""
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
            task_count = len(project.tasks)
            click.echo(f"📁 {project.id}: {project.name} ({task_count} tasks)")
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
            status_icon = "✅" if task.status == 'done' else "⏳"
            click.echo(f"{status_icon} {task.id}: {task.title} [Project: {task.project.name}]")
            if task.description:
                click.echo(f"   Description: {task.description}")
            if task.deadline:
                overdue = " (OVERDUE!)" if task.deadline < datetime.now() and task.status != 'done' else ""
                click.echo(f"   Deadline: {task.deadline}{overdue}")
            click.echo(f"   Status: {task.status}")
            click.echo()
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

cli.add_command(autoclose_overdue_cmd, name="autoclose-overdue")


if __name__ == '__main__':
    cli()
