from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.utils.security import verify_password
from app.db.database import get_admin_user
from starlette.middleware.sessions import SessionMiddleware

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin-login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse(request, "admin_login.html", {"request": request})

@router.post("/admin-login")
async def handle_admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_admin_user(username)
    if user and verify_password(password, user[2]):
        request.session["admin"] = username
        return RedirectResponse("/admin", status_code=302)
    return templates.TemplateResponse(request, "admin_login.html", {"request": request, "error": "Invalid credentials"})
