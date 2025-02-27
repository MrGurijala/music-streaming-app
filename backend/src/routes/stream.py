from fastapi import APIRouter, HTTPException
from services.s3_service import get_transcoded_file_url

router = APIRouter()

@router.get("/stream/{file_name}")
async def get_stream_url(file_name: str):
    """Returns a signed URL to stream the transcoded file"""
    file_url = get_transcoded_file_url(file_name)
    if not file_url:
        raise HTTPException(status_code=404, detail="File not found")
    return {"stream_url": file_url}
