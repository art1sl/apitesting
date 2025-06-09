from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from postgreDB import fetchrow
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/{country}/{service}/{link_id}", response_class=HTMLResponse)
async def render_dynamic_page(request: Request, country: str, service: str, link_id: str):
    data = await fetchrow("SELECT data FROM generated_links WHERE link_id = $1", link_id)
    if not data:
        return HTMLResponse("Ссылка не найдена", status_code=404)

    context = json.loads(data["data"]) if isinstance(data["data"], str) else data["data"]
    context["request"] = request  # Jinja требует

    template_path = f"pages/{country}/{service}.html"
    if not os.path.exists(f"templates/{template_path}"):
        return HTMLResponse("Шаблон не найден", status_code=404)

    return templates.TemplateResponse(template_path, context)



