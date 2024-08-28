# app/main.py
from fastapi import FastAPI

app = FastAPI()

# Import routers từ các module
from crawling.app import crawl_api

# Gán các router vào ứng dụng
app.include_router(crawl_api.router)