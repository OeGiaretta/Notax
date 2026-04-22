from  fastapi import APIRouter, File, HTTPException ,UploadFile

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"]
)

@router.post("/validate-xml")
async def validate_xml(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    if not file.filename.lower().endswith(".xml"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only XML files are allowed.")
        
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    return{
         "filename": file.filename,
         "content_type": file.content_type,
         "size_bytes": len(content),
         "message": "File received successfully"
    }