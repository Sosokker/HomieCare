import uvicorn

from fastapi import FastAPI
from routers import video, weather

app = FastAPI(
    title="Healthcare-System",
    description="Hello Stranger.",
    root_path="/api/v1",
    docs_url="/docs/swagger",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs"
    )

app.include_router(video.router, prefix="/camera")
app.include_router(weather.router, prefix="/weather")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)