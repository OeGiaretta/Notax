from  fastapi import APIRouter, File, HTTPException ,UploadFile
from app.services.xml_parser import parse_xml_content

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
    
    parsed = parse_xml_content(content)

    if not parsed["success"]:
        raise HTTPException(status_code=400, detail=parsed["error"])

    return {
        "filename": file.filename,
        "parsed_data": parsed["data"]
    }