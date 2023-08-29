from fastapi import FastAPI
from routers import database, user, security, item

app = FastAPI()

app.include_router(router=database.router)
app.include_router(router=user.router)
app.include_router(router=security.router)
app.include_router(router=item.router)