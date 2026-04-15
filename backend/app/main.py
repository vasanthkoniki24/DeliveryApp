from fastapi import FastAPI
from app.api.v1.routes.auth import router as auth_router 
from app.api.v1.routes.admin import router as admin_router
from app.api.v1.routes.product import router as product_router
from app.api.v1.routes.order import router as order_router
from app.api.v1.routes.ws import router as ws_router
from app.api.v1.routes.notification import router as notification_router
from app.db.base import Base
from app.db.session import engine

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(ws_router)
app.include_router(notification_router)