import click

from todo_list.db.session import db
from todo_list.repositories.task_repository import TaskRepository
from todo_list.services.task_service import TaskService


def auto_close_overdue_tasks():
    session = db.get_session()
    try:
        task_repo = TaskRepository(session)
        task_service = TaskService(task_repo)
        
        closed_count = task_service.auto_close_overdue_tasks()
        
        if closed_count > 0:
            click.echo(f"✅ Auto-closed {closed_count} overdue task(s)")
        else:
            click.echo("ℹ️  No overdue tasks found to close")
        
        return closed_count
    finally:
        session.close()

@click.command()
def autoclose_overdue_cmd():
    auto_close_overdue_tasks()


if __name__ == "__main__":
    autoclose_overdue_cmd()
