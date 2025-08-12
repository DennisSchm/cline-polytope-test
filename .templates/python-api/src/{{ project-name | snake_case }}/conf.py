from pydantic import BaseModel

from .utils import env, log
from .utils.env import EnvVarSpec

logger = log.get_logger(__name__)

#### Types ####

class HttpServerConf(BaseModel):
    host: str
    port: int
    autoreload: bool

#### Env Vars ####

## Logging ##

LOG_LEVEL = EnvVarSpec(id="LOG_LEVEL", default="INFO")

## HTTP ##

HTTP_HOST = EnvVarSpec(id="HTTP_HOST", default="0.0.0.0")
HTTP_PORT = EnvVarSpec(id="HTTP_PORT", default="8000")
HTTP_AUTORELOAD = EnvVarSpec(
    id="HTTP_AUTORELOAD",
    parse=lambda x: x.lower() == "true",
    default="false",
    type=(bool, ...),
)

#### Validation ####

def validate() -> bool:
    return env.validate(
        [
            LOG_LEVEL,
            HTTP_PORT,
            HTTP_AUTORELOAD,
        ]
    )

#### Getters ####

def get_log_level() -> str:
    return env.parse(LOG_LEVEL)

def get_http_conf() -> HttpServerConf:
    return HttpServerConf(
        host=env.parse(HTTP_HOST),
        port=env.parse(HTTP_PORT),
        autoreload=env.parse(HTTP_AUTORELOAD),
    )
