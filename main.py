from src.settings import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=settings.host, port=settings.port, reload=True)
