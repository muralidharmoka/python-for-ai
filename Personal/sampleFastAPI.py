from fastapi import FastAPI

app = FastAPI(title="Sample FastAPI App")

@app.get("/ask")
def ask(q: str):
    return {"response": f"You asked: {q}"}
