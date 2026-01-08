
from fastapi import FastAPI
from src.router.router_user import router_user
from src.router.router_file import router_file
from src.router.router_estate import router_estate
from src.router.router_auth import router_auth
from fastapi.middleware.cors import CORSMiddleware
from src.router.router_estate import router_estate
from src.router.router_lots import router_lots
from fastapi.staticfiles import StaticFiles
from src.router.router_comennt import router_coment
from src.router.router_coffe  import router_coffe
from src.router.router_analysis import router_analysis
app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_file)
app.include_router(router_estate)
app.include_router(router_lots)
app.include_router(router_coffe)
app.include_router(router_analysis)
app.include_router(router_coment)
app.mount("/img", StaticFiles(directory="public/img"), name="img")
app.mount("/docs",StaticFiles(directory="public/docs"), name="docs")
@app.get("/")
def root():
    return {"message": "welcome to World the our FastAPI application backend of la tribuna del café"}