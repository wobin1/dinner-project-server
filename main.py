from fastapi import FastAPI
from modules.users.router import users_router
from modules.auth.router import auth_router
from modules.guest.router import guests_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://civet-ui.netlify.app/"],  # Allows all 
    allow_credentials=True,  # Allows cookies to be sent
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(guests_router)

@app.get('/')
def root():
    return {"message": "Starters server!"}
