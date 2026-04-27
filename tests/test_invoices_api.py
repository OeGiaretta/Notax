from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_valid_xml():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc>
  <NFe>
    <infNFe>
      <ide>
        <nNF>12345</nNF>
        <dhEmi>2026-04-22T10:00:00-03:00</dhEmi>
      </ide>
      <emit>
        <CNPJ>11222333000181</CNPJ>
        <xNome>Empresa Teste</xNome>
      </emit>
      <dest>
        <CNPJ>11222333000181</CNPJ>
        <xNome>Cliente Teste</xNome>
      </dest>
      <det>
        <prod>
          <cProd>001</cProd>
          <xProd>Produto Teste</xProd>
          <NCM>12345678</NCM>
          <CFOP>5102</CFOP>
          <vProd>100.00</vProd>
        </prod>
      </det>
      <total>
        <ICMSTot>
          <vNF>100.00</vNF>
        </ICMSTot>
      </total>
    </infNFe>
  </NFe>
</nfeProc>
"""

    response = client.post(
        "/invoices/validate-xml",
        files={"file": ("test.xml", xml_content, "text/xml")},
    )

    assert response.status_code == 200


def test_invalid_file_type():
    response = client.post(
        "/invoices/validate-xml",
        files={"file": ("test.txt", "invalid content", "text/plain")},
    )

    assert response.status_code == 400