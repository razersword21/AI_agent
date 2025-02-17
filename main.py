from fastapi import FastAPI
from routers import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Agent API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api.router, prefix='/razer_api')