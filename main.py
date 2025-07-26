from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hdhub_down import get_download_link  # Your scraping function
import traceback

app = FastAPI()

# Allow all origins for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⛔️ Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class MovieRequest(BaseModel):
    movie: str
    quality: str

@app.post("/get_link")
async def get_link(data: MovieRequest):
    try:
        print(f"🔍 Scraping for {data.movie} [{data.quality}]")
        link = get_download_link(data.movie, data.quality)

        if link:
            return {"status": "ok", "link": link}
        else:
            return {"status": "error", "message": "Could not extract link. Please check movie/quality name."}

    except Exception as e:
        # Logs full error to console/logs (especially useful on Railway)
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Internal error: {str(e)}"
        }
