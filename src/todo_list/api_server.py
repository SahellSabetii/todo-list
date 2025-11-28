import uvicorn

from todo_list.api.main import create_application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "todo_list.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
