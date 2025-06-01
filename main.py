from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from decode_tt import decode_tt
from constants import tt_options
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "options": None, "input_text": ""})

@app.post("/get-decoded-tt", response_class=HTMLResponse)
async def handle_form(request: Request, input_text: str = Form(...)):
    decoded_tt_response = decode_tt(input_text)
    print("Decoded TT Response:", decoded_tt_response)
    return templates.TemplateResponse("index.html", {"request": request, "result": decoded_tt_response.split('\n'), "options": tt_options, "input_text": input_text})

@app.post("/get-decoded-tt-by-type", response_class=HTMLResponse)
async def handle_form(request: Request, input_text: str = Form(...), selected_option: str = Form(...)):
    print("input_text:", input_text)
    print("selected_option:", selected_option)
    decoded_tt_response = decode_tt(input_text, selected_option)
    return templates.TemplateResponse("index.html", {"request": request, "result": decoded_tt_response.split('\n'), "options": tt_options, "input_text": input_text})
