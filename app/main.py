import uvicorn

from app.core.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.core.asgi:app",
        host=settings.server.HOST,
        port=settings.server.PORT,
        reload=True,
    )
