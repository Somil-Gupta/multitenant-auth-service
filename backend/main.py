from apis.info.info_endpoints import router as info_router
from apis.members.members_endpoints import router as members_router
from apis.stats.stats_endpoints import router as stats_router
from apis.user.user_endpoints import router as user_router
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(info_router)
app.include_router(members_router)
app.include_router(stats_router)
app.include_router(user_router)