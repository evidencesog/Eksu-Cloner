#/routes/admin.py
# app/routes/admin.py
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from pathlib import Path
from app.db.database import fetch_all_credentials
import os

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

HASHED_PASSWORD = b"$2b$12$wXFflsHrWcRBfLEQhyV9PO1VQAMKrAcRbEphA99lWulQXBg5y5zwK"

@router.get("/admin", response_class=HTMLResponse)
async def show_admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@router.post("/admin/login")
async def admin_login(request: Request, password: str = Form(...)):
    if bcrypt.verify(password, HASHED_PASSWORD.decode()):
        request.session["admin"] = "letmein"
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    else:
        return templates.TemplateResponse(request, "admin_login.html", {"request": request, "error": "Invalid password"})

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def view_admin_dashboard(request: Request):
    if request.session.get("admin") != "letmein":
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    credentials = fetch_all_credentials()
    return templates.TemplateResponse(request, "admin_dashboard.html", {"request": request, "credentials": credentials})

