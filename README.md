# Finance AI Assistant

An enterprise finance assistant that answers natural-language business questions using a governed SQL workflow and a document-retrieval layer for supporting context.

The project currently uses a local LLM to generate SQL, validates the query against business rules, executes it against Snowflake, and then turns the result into a business-friendly answer.

## What this app does

- Converts business questions into SQL using an LLM
- Parses the user intent into structured fields such as measure, dimension, filters, year, and quarter
- Validates SQL to block unsafe operations and enforce approved table access
- Executes read-only queries against Snowflake
- Uses retrieved document context to support narrative explanations
- Produces concise financial answers for business users

## Main features

- Governed text-to-SQL layer
- Intent parsing for finance questions
- Snowflake-backed query execution
- Local LLM integration through Ollama
- Semantic model for revenue and dimension rules
- RAG-style retrieval using embeddings and similarity matching

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM runtime | Ollama |
| Model | `qwen2.5:1.5b-instruct` |
| Data warehouse | Snowflake |
| Database access | `snowflake-connector-python` |
| Environment config | `python-dotenv` |
| Embeddings | `sentence-transformers` |
| Data processing | `pandas` |
| Vector math | `numpy` |
| ML backend | `torch` |
| Additional ML support | `scikit-learn` |
| API calls | `requests` |

## Current project structure

```text
finance-ai-assistant/
├── .env
├── README.md
├── .gitignore
├── data/
│   ├── finance_revenue.csv
│   └── documents/
│       └── apac_q2_commentary.txt
├── src/
│   ├── __init__.py
│   ├── app/
│   │   ├── governed_query.py
│   │   └── intent_parser.py
│   ├── database/
│   │   ├── create_data.py
│   │   ├── create_database.py
│   │   ├── query_database.py
│   │   ├── semantic_model.py
│   │   ├── snowflake_connection.py
│   │   └── sql_rules.py
│   ├── evaluation/
│   ├── governance/
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   ├── ollama_client.py
│   │   ├── response_generator.py
│   │   └── sql_prompt.py
│   └── rag/
│       ├── embeddings.py
│       ├── rag_answer.py
│       ├── similarity.py
│       ├── test_embeddings.py
│       ├── vector_retriever.py
│       └── __pycache__/
└── tests/
```

## Key architecture components

### 1. App layer
- `src/app/governed_query.py` orchestrates the full SQL flow
- `src/app/intent_parser.py` extracts structured business intent from a natural-language question

### 2. Database layer
- `src/database/semantic_model.py` defines the business semantic rules for measures and dimensions
- `src/database/sql_rules.py` validates that only safe, approved SQL is allowed
- `src/database/snowflake_connection.py` opens the Snowflake connection using environment variables

### 3. LLM layer
- `src/llm/llm_client.py` routes generation requests
- `src/llm/ollama_client.py` calls the local Ollama API
- `src/llm/sql_prompt.py` builds the prompt used to generate finance SQL
- `src/llm/response_generator.py` turns query results into business-friendly narrative responses

### 4. RAG layer
- `src/rag/embeddings.py` creates embeddings for document content
- `src/rag/vector_retriever.py` retrieves the most relevant context
- `src/rag/similarity.py` calculates similarity for matching documents
- `src/rag/rag_answer.py` uses retrieved context to answer questions with supporting narrative

## Configuration

The project uses a `.env` file for Snowflake credentials. Example variables include:

```env
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=...
SNOWFLAKE_SCHEMA=...
```

## Prerequisites

1. Python environment
2. Ollama installed locally
3. Snowflake access configured in `.env`
4. Model pulled in Ollama, for example:

```bash
ollama pull qwen2.5:1.5b-instruct
```

## Setup

```bash
# Activate the virtual environment
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

If requirements are not pinned in the repo yet, install the packages used by the project:

```bash
pip install python-dotenv snowflake-connector-python requests pandas numpy sentence-transformers torch scikit-learn
```

## Usage

### Run the governed SQL flow

```bash
python src/app/governed_query.py
```

This builds a SQL prompt, validates it, executes the approved query in Snowflake, and returns a business explanation.

### Run the RAG retrieval flow

```bash
python src/rag/rag_answer.py
```

This loads finance document content, creates embeddings, retrieves the most relevant passages, and uses them as supporting context for answers.

## Data model and business rules

The SQL prompt and validation logic are built around a full finance semantic model. The project explicitly governs:

- measure: revenue
- allowed dimensions: region, client, product
- quarter logic: Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec
- allowed Snowflake tables:
  - `FINANCE_DEV.CORE.FACT_SALES`
  - `FINANCE_DEV.CORE.DIM_REGION`
  - `FINANCE_DEV.CORE.DIM_CUSTOMER`
  - `FINANCE_DEV.CORE.DIM_PRODUCT`

The validation layer rejects unsafe operations such as `DELETE`, `DROP`, `ALTER`, and other non-read-only SQL.

## License

This project does not currently include a license file.
