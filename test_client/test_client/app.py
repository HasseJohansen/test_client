#!/usr/bin/env python3
"""This is a test api using an upstream api to get either pdf or png.
   If an invalid pdf is returnined from upstream we send a http 204 empty response"""
import os
import logging
import io
from fastapi import FastAPI, Response, HTTPException
from PyPDF2 import PdfReader, errors
import requests

import uvicorn


logging.basicConfig(level=logging.WARN)
log = logging.getLogger()

try:
    SERVICE_HOST = os.environ["DUMMY_SERVICE_HOST"]
except KeyError:
    log.critical("required env variable DUMMY_SERVICE_HOST not set")
    raise

api = FastAPI()


@api.get("/health")
async def health():
    """This is a dummy healtcheck always returning healthy"""
    return {"status": "Healthy"}


@api.get("/{content_id}")
async def get_from_dummy():
    """This makes http requests to the upstream service not returning invalid pdf"""
    up_req = requests.get(f"http://{SERVICE_HOST}/")
    if up_req.ok:
        if up_req.headers["Content-Type"] == "image/png":
            return Response(content=up_req.content, media_type="image/png")
        if up_req.headers["Content-Type"] == "application/pdf" and check_pdf(
            up_req.content
        ):
            return Response(content=up_req.content, media_type="application/pdf")
        log.warning("Upstream returned invalid PDF")
        return Response(status_code=204)
    log.error(
        "Error from upstream service: %s, http status: %s",
        SERVICE_HOST,
        up_req.status_code,
    )
    raise HTTPException(status_code=500, detail="Error reponse status from upstream")


def check_pdf(pdf_data):
    """This checks if the pdf is invalid by reading it"""
    try:
        PdfReader(io.BytesIO(pdf_data), strict=True)
    except errors.PdfReadError:
        return False
    else:
        return True


if __name__ == "__main__":
    print("Starting API...")
    uvicorn.run(
        api,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
    )
