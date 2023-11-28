import uvicorn

def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "main:get_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()

