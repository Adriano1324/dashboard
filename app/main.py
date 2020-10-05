import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.token.routes import router as auth_router
from app.user.routes import router as user_router
from app.databases.routes import router as db_router
from app.charts.routes import router as chart_router
from app.dashboards.routes import router as dashboard_router

from app.config import (
    jinja_env,
    origins,
    allow_credentials,
    allow_methods,
    allow_headers
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


#app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)



app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


app.include_router(user_router, prefix="/api/v1", tags=['user'])
app.include_router(auth_router, prefix="/api/v1", tags=['auth'])
app.include_router(db_router, prefix="/api/v1", tags=['db'])
app.include_router(chart_router, prefix="/api/v1", tags=['chart'])
app.include_router(dashboard_router, prefix="/api/v1", tags=['dashboard'])

@app.get('/')
async def welcome():
    file = open('templates/index.html', mode="r")
    return HTMLResponse(content=file.read())

