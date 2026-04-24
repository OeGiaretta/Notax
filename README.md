# Notax

Notax is an automated invoice validation API for Brazilian NF-e (Nota Fiscal Eletrônica) documents.

It processes XML invoices, extracts structured data, and evaluates their quality through a rule-based validation engine.

---

## 🧠 What is Notax?

Notax is a backend system designed to analyze and validate electronic invoices (NF-e) in an automated and scalable way.

Instead of manually checking invoices for inconsistencies, Notax applies a set of validation rules to detect issues such as:

- Missing or invalid fields  
- Incorrect fiscal data (NCM, CFOP)  
- Invalid CNPJ numbers  
- Financial inconsistencies  
- Invalid or inconsistent dates  

It returns a structured validation result with severity levels and a quality score.

---

## 🎯 Objective

The goal of Notax is to:

- Automate invoice validation  
- Reduce manual auditing effort  
- Detect fiscal inconsistencies early  
- Provide a scalable validation engine  
- Serve as a foundation for financial/fiscal analysis systems  

---

## 🚀 Features

- Upload and parse NF-e XML files  
- Extract structured invoice data  
- Validate required fields and item consistency  
- Validate NCM and CFOP formats  
- Validate CNPJ using checksum algorithm  
- Validate invoice date  
- Validate total value consistency  
- Apply rule-based validation with severity levels  
- Generate a quality score for each invoice  
- Modular validation engine (scalable architecture)  

---

## 📦 Example Response

````json
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
````

---

## 🧠 Architecture

````
app/
├── api/            # FastAPI routes  
├── services/       # Core logic (parser, validator)  
├── core/rules/     # Validation rules (modularized)  
├── schemas/        # Data models (Pydantic)  
````

---

## 🛠️ Tech Stack

* Python 3
* FastAPI
* Pydantic
* xmltodict
* Uvicorn

---

## ▶️ Running Locally

````bash
git clone https://github.com/OeGiaretta/Notax.git
cd Notax

pip install -r requirements.txt

uvicorn app.main:app --reload


Open:


http://localhost:8000/docs

````
---

## 🧪 Testing (coming soon)

Automated tests with pytest will be added to ensure rule reliability and prevent regressions.

---

## 🔮 Roadmap

* Automated tests (pytest)
* Advanced fiscal validation rules
* Database persistence
* Batch XML processing
* Dashboard for analytics

---

## 📌 Status

🚧 Active development — validation engine implemented

---

## 📄 License

MIT License

