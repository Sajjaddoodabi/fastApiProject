from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/blogs")
def blog(name: str):
    return {"data": 'blogs'}
