from api.routes import router 
from fastapi import FastAPI


app = FastAPI(title="LLM data migration engine")
app.include_router(router)