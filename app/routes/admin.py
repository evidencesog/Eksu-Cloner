from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.database import fetch_all_credentials
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

ADMIN_PASSWORD = os.getenv("ADMIN_PASS", "letmein")

@router.get("/admin", response_class=HTMLResponse)
async def view_admin_dashboard(request: Request, auth: str = ""):
    if auth != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    credentials = fetch_all_credentials()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "credentials": credentials
    })

