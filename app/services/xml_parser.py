import xmltodict

def parse_xml_content(content: bytes):
    try:
        xml_string = content.decode('utf-8')
        data = xmltodict.parse(xml_string)
        
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }