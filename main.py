from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hdhub_down import get_download_link  # This function should return final download link

app = FastAPI()

# Allow all origins (Flutter app can access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expected structure of POST body
class MovieRequest(BaseModel):
    movie: str
    quality: str

@app.post("/get_link")
async def get_link(data: MovieRequest):
    try:
        print(f"🔍 Scraping for {data.movie} [{data.quality}]")
        link = get_download_link(data.movie, data.quality)
        return {"status": "ok", "link": link}
    except Exception as e:
        return {"status": "error", "message": str(e)}

