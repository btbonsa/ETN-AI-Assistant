from fastapi import FastAPI

app = FastAPI()

@app.get("/master")
async def read_root():
    return {"Hello": "World"}
