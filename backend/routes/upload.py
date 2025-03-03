# Music files upload to AWS s3
from fastapi import APIRouter, File, UploadFile, HTTPException
from services.s3_service import upload_file_to_s3

router = APIRouter()

@router.post("/upload")
async def upload_song(file: UploadFile):
    """Handles music upload to the raw S3 bucket"""
    file_url = upload_file_to_s3(file.filename, file.file)
    if not file_url:
        raise HTTPException(status_code=500, detail="File upload failed")
    return {"message": "File uploaded successfully", "url": file_url}
