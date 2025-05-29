from fastapi import FastAPI
from feeds import get_all_data
import uvicorn

app = FastAPI()

@app.get("/api/feeds")
def read_feeds():
    return get_all_data()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
