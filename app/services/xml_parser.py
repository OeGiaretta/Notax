import xmltodict

def parse_xml_content(content: bytes):
    try:
        xml_string = content.decode('utf-8')
        data = xmltodict.parse(xml_string)
        
        inf_nfe = (
            data.get('nfeProc', {})
                .get('NFe', {})
                .get('infNFe', {})
        )

        ide = inf_nfe.get('ide', {})
        emit = inf_nfe.get('emit', {})
        dest = inf_nfe.get('dest', {})
        total = inf_nfe.get('total', {}).get("ICMSTot", {})

        det = inf_nfe.get("det", [])
        if isinstance(det, dict):
            det = [det]
        
        items = []
        for item in det:
            prod = item.get("prod", {})
            
            items.append({
                "code": prod.get('cProd'),
                "name": prod.get('xProd'),
                "ncm": prod.get('NCM'),
                "cfop": prod.get('CFOP'),
                "value": prod.get('vProd')
            })

        return {
            "success": True,
            "data": {
                "invoice_number": ide.get('nNF'),
                "issued_at": ide.get('dhEmi'),
                "issuer_cnpj": emit.get('CNPJ'),
                "issuer_name": emit.get('xNome'),
                "recipient_cnpj": dest.get('CNPJ'),
                "recipient_name": dest.get('xNome'),
                "total_value": total.get('vNF'),
                "items": items
            }
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": {str(e)}
        }