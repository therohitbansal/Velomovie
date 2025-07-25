from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
async def download(movie_name: str = Form(...), quality: str = Form(...)):
    try:
        subprocess.Popen(["python", "hdhub_down.py", movie_name, quality])
        return {"message": "Download started"}
    except Exception as e:
        return {"error": str(e)}
