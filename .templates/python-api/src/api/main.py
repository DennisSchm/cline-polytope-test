from fastapi import FastAPI

app = FastAPI(title="API", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main() -> None:
    import os
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(app, host=host, port=port)
