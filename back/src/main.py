from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth import router as auth_router
from users import router as users_router
from files import router as files_router

from auth.dependencies import check_user_is_admin, get_current_auth_user

import uvicorn


app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(files_router)


@app.get("/")
async def root(is_admin=Depends(get_current_auth_user)):
    return {"message": "MBKS check 1.0"}


if __name__ == "__main__":
    uvicorn.run(app)
