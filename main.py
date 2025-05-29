from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from decode_tt import decode_transaction
from constants import tt_options
from fastapi import FastAPI, Request, Form

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, input_text: str = Form(...)):
    decoded_tt_response = decode_transaction(input_text) 
    return templates.TemplateResponse("index.html", {"request": request, "result": decoded_tt_response.split('\n'), "options": tt_options})

@app.post("/submit-tt-type", response_class=HTMLResponse)
async def handle_form(request: Request, input_text: str = Form(...)):
    decoded_tt_response = decode_transaction(input_text) 
    return templates.TemplateResponse("index.html", {"request": request, "result": decoded_tt_response.split('\n'), "options": tt_options})
