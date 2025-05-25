from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from processor import process_string
from fastapi import FastAPI, Request, Form

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, input_text: str = Form(...)):
    processed = process_string(input_text)
    return templates.TemplateResponse("index.html", {"request": request, "result": processed})
