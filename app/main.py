#Main.py 


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import login
from app.db.database import init_db  # <--- Add this
from fastapi.responses import RedirectResponse
import uvicorn
from pyngrok import ngrok

# Set up a tunnel to the app on port 8000
public_url = ngrok.connect(8000)
print("Public URL:", public_url)

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


app = FastAPI()

# Mount static and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize the database
init_db()  # <--- Run this when the app starts

# Include the router
app.include_router(login.router)

@app.get("/")
async def root_redirect():
   return RedirectResponse(url="/login")
