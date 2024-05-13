import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import video, weather, prediction, camera, recommend, action


app = FastAPI(
    title="Healthcare-System",
    description="Hello Stranger.",
    root_path="/api/v1",
    docs_url="/docs/swagger",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
    lifespan=video.lifespan
    )

origins = [
    "http://localhost",
    "http://localhost:5173",
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/camera")
app.include_router(weather.router, prefix="/weather")
app.include_router(prediction.router, prefix="/weather")
app.include_router(camera.router, prefix="/camera")
app.include_router(recommend.router, prefix="/recommend")
app.include_router(action.router, prefix="/action")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)