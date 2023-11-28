from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Words translation API",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # app.include_router(api_router)

    add_pagination(app)

    return app
