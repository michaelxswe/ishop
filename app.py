from fastapi import FastAPI
from routers import data_router, users_router, auth_router, items_router, orders_router, cart_router

app = FastAPI()

app.include_router(router=data_router.router)
app.include_router(router=users_router.router)
app.include_router(router=auth_router.router)
app.include_router(router=items_router.router)
app.include_router(router=orders_router.router)
app.include_router(router=cart_router.router)