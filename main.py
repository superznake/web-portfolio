import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import uvicorn

app = FastAPI(title="Портфолио")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/works", StaticFiles(directory="works"), name="works")

templates = Jinja2Templates(directory="templates")
templates.env.cache = None

WORKS_DIR = Path("works")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    projects = []

    if WORKS_DIR.exists():
        for project_dir in sorted(WORKS_DIR.iterdir()):
            if project_dir.is_dir():
                json_path = project_dir / "data.json"
                image_path = project_dir / "image.png"

                if json_path.exists() and image_path.exists():
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        projects.append({
                            "title": data.get("title", "Без названия"),
                            "description": data.get("description", ""),
                            "image": f"/works/{project_dir.name}/image.png",
                            "links": data.get("links", [])
                        })

                    except Exception as e:
                        logging.error(f"✗ Ошибка в проекте {project_dir.name}: {e}")

    template = templates.get_template("index.html")
    html_content = template.render(request=request, projects=projects)
    return HTMLResponse(content=html_content)


def runserver():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=63000,
        log_level="info"
    )


if __name__ == "__main__":
    runserver()
