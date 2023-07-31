from fastapi import FastAPI
from routers import root, user, security, item

app = FastAPI()

app.include_router(router=root.router)
app.include_router(router=user.router)
app.include_router(router=security.router)
app.include_router(router=item.router)


