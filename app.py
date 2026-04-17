import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Team Resource Board")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Supabase configuration
url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")
supabase: Client = create_client(url, key)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Mock data for now, will replace with Supabase call
    boards = [
        {"id": 1, "name": "Hackathon 2026", "description": "Resource sharing for upcoming hackathon.", "owner": "Aditya"},
        {"id": 2, "name": "CCL Mini Project", "description": "Cloud Computing Lab resources.", "owner": "Team Alpha"}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "boards": boards})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/board/{board_id}", response_class=HTMLResponse)
async def board_view(request: Request, board_id: int):
    # Mock data
    board = {"id": board_id, "name": "Hackathon 2026", "description": "Resource sharing for upcoming hackathon."}
    resources = [
        {"id": 1, "title": "Supabase Docs", "url": "https://supabase.com/docs", "type": "link", "description": "Main documentation"},
        {"id": 2, "title": "Project Proposal.pdf", "url": "#", "type": "file", "description": "Initial proposal draft"}
    ]
    return templates.TemplateResponse("board.html", {"request": request, "board": board, "resources": resources})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
