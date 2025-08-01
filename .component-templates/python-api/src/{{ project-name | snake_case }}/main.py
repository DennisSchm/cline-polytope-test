import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .utils import log
from .routes import router
from . import conf

logger = log.get_logger(__name__)
app = FastAPI(title="API", version="0.1.0")

def init():
    """Initializes the application."""
    log.init(conf.get_log_level())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init logic goes here
    yield
    # clean-up logic goes here


app = FastAPI(
    title="{{ project-name }}",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan
)
app.include_router(router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main() -> None:
    init()

    if not conf.validate():
        raise ValueError("Invalid configuration.")

    http_conf = conf.get_http_conf()
    logger.info(f"Starting API on port {http_conf.port}")
    uvicorn.run(
        "{{ project-name | snake_case }}.main:app",
        host=http_conf.host,
        port=http_conf.port,
        reload=http_conf.autoreload,
        log_level="debug" if http_conf.debug else "info",
        log_config=None
    )
