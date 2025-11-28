import warnings

from todo_list.cli.console import cli
from todo_list.db.session import db





if __name__ == '__main__':
    warnings.warn(
        "CLI interface is deprecated and will be removed soon"
        "Please use the FastAPI interface instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
    print("⚠️  WARNING: CLI interface is deprecated and will be removed soon.")
    print("   Please use the FastAPI interface instead.")
    print("   Start API server: poetry run python -m todo_list.api_server")
    print("   API Docs: https://example.com/docs\n")

    db.create_tables()
    cli()
