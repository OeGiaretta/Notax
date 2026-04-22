from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.xml_parser import parse_xml_content
from app.services.validator import validate_invoice_data

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/validate-xml")
async def validate_xml(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not file.filename.lower().endswith(".xml"):
        raise HTTPException(status_code=400, detail="Only XML files are allowed.")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="File is empty.")

    parsed = parse_xml_content(content)

    if not parsed["success"]:
        raise HTTPException(status_code=400, detail=parsed["error"])

    validation = validate_invoice_data(parsed["data"])

    return {
        "filename": file.filename,
        "parsed_data": parsed["data"],
        "validation": validation.model_dump()
    }