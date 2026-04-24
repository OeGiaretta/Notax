from app.services.validator import validate_invoice_data


def test_valid_invoice_should_return_ok():
    data = {
        "invoice_number": "12345",
        "issued_at": "2026-04-22T10:00:00-03:00",
        "issuer_cnpj": "11222333000181",
        "recipient_cnpj": "11222333000181",
        "total_value": "100.00",
        "items": [
            {
                "code": "001",
                "name": "Produto Teste",
                "ncm": "12345678",
                "cfop": "5102",
                "value": "100.00",
            }
        ],
    }

    result = validate_invoice_data(data)

    assert result.status == "ok"
    assert result.score == 100
    assert result.summary.total_issues == 0
    assert result.issues == []


def test_invalid_ncm_should_return_error():
    data = {
        "invoice_number": "12345",
        "issued_at": "2026-04-22T10:00:00-03:00",
        "issuer_cnpj": "11222333000181",
        "recipient_cnpj": "11222333000181",
        "total_value": "100.00",
        "items": [
            {
                "code": "001",
                "name": "Produto Teste",
                "ncm": "123",  # inválido
                "cfop": "5102",
                "value": "100.00",
            }
        ],
    }

    result = validate_invoice_data(data)

    assert result.status == "error"
    assert result.summary.errors == 1
    assert result.issues[0].code == "INVALID_NCM_FORMAT"


def test_total_mismatch_should_return_error():
    data = {
        "invoice_number": "12345",
        "issued_at": "2026-04-22T10:00:00-03:00",
        "issuer_cnpj": "11222333000181",
        "recipient_cnpj": "11222333000181",
        "total_value": "150.00",  # errado
        "items": [
            {
                "code": "001",
                "name": "Produto Teste",
                "ncm": "12345678",
                "cfop": "5102",
                "value": "100.00",
            }
        ],
    }

    result = validate_invoice_data(data)

    assert result.status == "error"
    assert any(issue.code == "TOTAL_VALUE_MISMATCH" for issue in result.issues)