from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    if name:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Hello {name}"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Name is required"}
        )

