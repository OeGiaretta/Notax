Traduzindo o conteúdo do arquivo para inglês:


[1 tool called]

Tradução para inglês:

```markdown
## STRUCTURED TODO - Notax MicroSaaS

### PHASE 1: FOUNDATION (Minimum Viable MVP)

#### 1. Structure and Environment
- [ ] Create directory structure
  - Decision: follow the plan structure or adapt?
  - Tip: start simple, add folders as needed
  - Suggested structure:
    ```
    app/
    ├── models/
    ├── schemas/
    ├── api/
    ├── services/
    ├── validators/
    └── utils/
    streamlit_app/
    tests/
    ```

- [ ] Create `requirements.txt`
  - Decision: which versions to pin?
  - Tip: use recent stable versions, test compatibility later
  - Essential packages: FastAPI, SQLAlchemy, psycopg2-binary, xmltodict, ReportLab, Streamlit, Pydantic

- [ ] Configure virtual environment
  - Activate venv and install dependencies
  - Create `.env.example` with necessary variables

#### 2. Database
- [ ] Configure PostgreSQL
  - Decision: local Docker Compose or installed PostgreSQL?
  - Tip: Docker Compose makes it easier for other developers
  - Create `docker-compose.yml` with PostgreSQL

- [ ] Create `app/database.py`
  - Configure SQLAlchemy engine
  - Create SessionLocal and `get_db()` function
  - Decision: use async or sync? (sync is simpler to start)

- [ ] Create `app/config.py`
  - Use Pydantic Settings for environment variables
  - Define: DATABASE_URL, SECRET_KEY, etc.

#### 3. Data Models
- [ ] Create `app/models/user.py`
  - Think: which fields are essential in the MVP?
  - Minimum fields: id, email, password_hash, plan_type
  - Decision: authentication in MVP or later?

- [ ] Create `app/models/invoice.py`
  - Think: which invoice data is critical for validation?
  - Essential fields: chave_acesso, modelo (55 or NFSe), emitente, valores, dados_fiscais (JSON)
  - Decision: save complete XML or only extracted data?

- [ ] Create `app/models/audit.py`
  - Think: how to structure audit results?
  - Fields: user_id, total_invoices, errors_summary (JSON), report_path

- [ ] Create Alembic migrations
  - Initialize Alembic
  - Create first migration with all models

#### 4. XML Parser (System Core)
- [ ] Create `app/services/xml_parser.py`
  - Critical decision: start with NFe (model 55) or NFSe first?
  - Tip: start with NFe, it's more common
  - Required functions:
    - `parse_nfe(xml_content)` → extracts main data
    - `parse_nfse(xml_content)` → for later
    - `identify_modelo(xml_content)` → automatically detects type

- [ ] Test parser with real XMLs
  - Get some example XMLs (NFe)
  - Validate extraction: chave_acesso, emitente, destinatário, produtos, impostos
  - Think: can XML structure vary? How to handle variations?

#### 5. Fiscal Validators
- [ ] Create `app/validators/ncm_validator.py`
  - Validate: does NCM have 8 digits?
  - Decision: validate only format or also existence in official table?
  - MVP tip: format validation is sufficient initially

- [ ] Create `app/validators/cfop_validator.py`
  - Validate: does CFOP exist in official list?
  - Think: maintain list of valid CFOPs or consult API?
  - Tip: start with basic list of most common CFOPs

- [ ] Create `app/validators/cst_validator.py`
  - Validate: is CST compatible with tax regime?
  - Think: how to know client's regime? (ask in registration or infer)
  - MVP tip: basic format and expected value validations

- [ ] Create `app/validators/tax_calculator.py`
  - Validate: are ICMS, ISS calculations correct?
  - Function: `validate_icms_calculation(base, aliquota, valor)` → compares with invoice value
  - Think: tolerance for rounding differences?

- [ ] Create `app/services/fiscal_validator.py` (orchestrator)
  - Combines all validators
  - Returns list of errors found
  - Structure: `validate_invoice(invoice_data) → List[Error]`

#### 6. Upload and Processing
- [ ] Create `app/utils/file_handler.py`
  - Function: `extract_zip(zip_file)` → list of XMLs
  - Function: `process_xml_files(xml_files)` → calls parser for each one
  - Think: how to handle errors in individual files? (continue processing or stop?)

- [ ] Create FastAPI route `/api/upload`
  - Receive ZIP file
  - Extract and process XMLs
  - Save to database
  - Return summary: how many invoices processed, how many with errors

#### 7. Audit Service
- [ ] Create `app/services/audit_service.py`
  - Orchestrates: upload → parser → validators → results
  - Function: `audit_invoices(user_id, invoice_ids)` → returns complete report
  - Think: process synchronously or asynchronously? (MVP: synchronous is simpler)

#### 8. PDF Report Generation
- [ ] Create `app/services/report_generator.py`
  - Use ReportLab to generate PDF
  - Minimum content:
    - Executive summary (total invoices, errors found)
    - List of errors per invoice
    - Tax summary
  - Decision: fixed template or customizable? (MVP: fixed)

#### 9. Streamlit Interface (MVP)
- [ ] Create `streamlit_app/main.py`
  - Home page with file upload
  - Show processing progress
  - Display audit results

- [ ] Create `streamlit_app/pages/dashboard.py`
  - Basic metrics: total invoices, errors found
  - List of processed invoices
  - Link to download PDF

#### 10. Final Integration
- [ ] Create `app/main.py` (FastAPI)
  - Configure CORS
  - Include API routes
  - Health check endpoint

- [ ] Test complete flow
  - Upload ZIP → Processing → Validation → Report → Visualization
  - Identify bottlenecks and improvement points

---

### PHASE 2: EVOLUTION (Professional MVP)

#### 11. Authentication
- [ ] Login/registration system
- [ ] JWT tokens
- [ ] Protect API routes

#### 12. Plans and Limits
- [ ] Implement limits per plan
- [ ] Middleware to check limits before processing

#### 13. Advanced Dashboard
- [ ] Error charts by type
- [ ] Audit history
- [ ] Filters and searches

#### 14. Complete REST API
- [ ] Swagger documentation
- [ ] Endpoints for invoice CRUD
- [ ] Report endpoints

---

## IMPORTANT DECISIONS TO MAKE

1. Authentication in MVP?
   - Yes: more secure, but adds complexity
   - No: faster to test, add later

2. Asynchronous processing?
   - MVP: synchronous (simpler)
   - Later: Celery or FastAPI Background Tasks

3. XML storage?
   - Save complete: more space, but allows re-analysis
   - Only extracted data: lighter, but loses flexibility

4. Fiscal validations: how strict?
   - MVP: basic validations (format, simple calculations)
   - Later: integration with official tables, complex rules

---

## SUGGESTED EXECUTION ORDER

1. Week 1: Structure + Database + Models (items 1-3)
2. Week 2: XML Parser + Basic validators (items 4-5)
3. Week 3: Upload + Audit + PDF (items 6-8)
4. Week 4: Streamlit Interface + Tests (items 9-10)

---

## IMPLEMENTATION TIPS

- Start small: make it work with 1 XML before processing ZIPs
- Test with real data: get real XMLs to validate
- Document decisions: note why you chose each approach
- Versioning: small and frequent commits
- Incremental validations: add one validation rule at a time
```

Você está em modo "ask". Para salvar no arquivo, copie o conteúdo acima ou mude para modo "agent" para eu salvar automaticamente.