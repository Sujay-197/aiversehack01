#!/bin/bash
# Render startup script for FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
