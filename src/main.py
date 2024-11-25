from src.secret import Config
from fastapi import FastAPI, status
from src.routers import health_check
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.exceptions import ImageSearchEngineApiError, NotFoundError
from utils.helper import create_exception_handler
from src.routers.encoders import encoder_init, encoder_status

app = FastAPI(
    root_path="/api/v1",
    title="Image Search Engine",
    description="Backend service for Image Search Engine project.",
    version="1.0.0",
)

config = Config()

# @app.on_event("startup")
# async def startup():
#     await database_migration()


# @app.on_event("shutdown")
# async def shutdown():
#     await database_connection().dispose()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    middleware_class=SessionMiddleware, secret_key=config.MIDDLEWARE_SECRET_KEY
)

app.include_router(health_check.router)
app.include_router(encoder_init.router)
app.include_router(encoder_status.router)

app.add_exception_handler(
    exc_class_or_status_code=ImageSearchEngineApiError,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail_message="A service seems to be down, try again later.",
    ),
)


app.add_exception_handler(
    exc_class_or_status_code=NotFoundError,
    handler=create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        detail_message="File/data not found.",
    ),
)
