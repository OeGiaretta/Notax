# Notax

Automated invoice validation API for Brazilian NF-e (Nota Fiscal Eletrônica) documents.

Notax processes XML files, extracts structured data, and evaluates invoice quality using rule-based validation and scoring.

---

## 🚀 Features

- Upload and parse NF-e XML files
- Extract structured invoice data
- Validate required fields and item consistency
- Apply rule-based validation with severity levels
- Generate a quality score for each invoice
- Modular validation engine (scalable architecture)

---

## 📦 Example Response

```json
{
  "filename": "invoice.xml",
  "parsed_data": {
    "invoice_number": "12345",
    "issued_at": "2026-04-22T10:00:00-03:00",
    "issuer_cnpj": "12345678000199",
    "issuer_name": "Empresa Emitente LTDA",
    "recipient_cnpj": "98765432000188",
    "recipient_name": "Cliente Teste",
    "total_value": "100.00",
    "items": [
      {
        "code": "001",
        "name": "Produto Teste",
        "ncm": "12345678",
        "cfop": "5102",
        "value": "100.00"
      }
    ]
  },
  "validation": {
    "status": "ok",
    "score": 100,
    "summary": {
      "total_issues": 0,
      "errors": 0,
      "warnings": 0,
      "info": 0
    },
    "issues": []
  }
}
```

---

## 🧠 Architecture

```
app/
├── api/            # API routes (FastAPI)
├── services/       # Business logic (parser, validator)
├── core/rules/     # Validation rules (modularized)
├── schemas/        # Data models (Pydantic)
```

---

## 🛠️ Tech Stack

- Python 3
- FastAPI
- Pydantic
- xmltodict
- Uvicorn

---

## ▶️ Running Locally

```bash
git clone https://github.com/OeGiaretta/Notax.git
cd Notax
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧪 Testing

Use Swagger UI at:
http://localhost:8000/docs

---

## 🔮 Roadmap

- Advanced validation rules
- Database persistence
- Batch processing
- Dashboard

---

## 📄 License

MIT License
