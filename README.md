# Finance AI Assistant

An enterprise finance AI assistant that answers natural-language business questions using two pipelines: a governed **Text-to-SQL** pipeline and a **Retrieval-Augmented Generation (RAG)** pipeline.

Ask questions like *"What was APAC revenue in Q2 2026?"* or *"Why did APAC revenue increase?"* and get business-friendly answers powered by a local LLM.

## Features

- **Text-to-SQL Pipeline** — Converts natural language to SQL, validates it against governance rules, executes against a SQLite database, and generates a narrative answer.
- **RAG Pipeline** — Retrieves relevant finance documents using semantic similarity and generates answers grounded in enterprise documents.
- **SQL Governance** — Enforces read-only queries, blocks forbidden keywords, and validates table references.
- **Local LLM** — Runs entirely on your machine using Ollama with the `llama3` model. No data leaves your network.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.14 |
| LLM | Ollama (`llama3`) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Database | SQLite |
| Vector Search | NumPy cosine similarity |

## Project Structure

```
finance-ai-assistant/
├── data/
│   ├── finance.db                  # SQLite database (star schema)
│   ├── finance_revenue.csv         # 90 revenue records
│   └── documents/
│       └── apac_q2_commentary.txt  # Finance commentary for RAG
└── src/
    ├── app/
    │   └── governed_query.py       # Main entry point — text-to-SQL pipeline
    ├── database/
    │   ├── create_data.py          # Generates sample CSV data
    │   ├── create_database.py      # Creates SQLite DB from CSV
    │   ├── semantic_model.py       # Measures and dimensions definition
    │   └── sql_rules.py            # SQL governance / validation
    ├── llm/
    │   ├── ollama_client.py        # Ollama HTTP client
    │   ├── response_generator.py   # Business-friendly answer generation
    │   └── sql_prompt.py           # Text-to-SQL prompt builder
    └── rag/
        ├── embeddings.py           # Sentence embeddings
        ├── similarity.py           # Cosine similarity
        ├── vector_retriever.py     # Top-k document retrieval
        └── rag_answer.py           # RAG pipeline entry point
```

## Prerequisites

1. **Python 3.14+**
2. **Ollama** — Install from [ollama.com](https://ollama.com), then pull the model:
   ```bash
   ollama pull llama3
   ```
   Ensure Ollama is running on `http://localhost:11434`.

## Setup

```bash
# Activate the virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Generate sample data
python src/database/create_data.py

# Create the SQLite database
python src/database/create_database.py
```

## Usage

### Text-to-SQL Pipeline

```bash
python src/app/governed_query.py
```

Asks: *"What was APAC revenue in Q2 2026?"*

**How it works:**
1. Builds a prompt with the database schema and semantic model
2. Sends it to Ollama to generate SQL
3. Validates the SQL against governance rules (read-only, allowed tables)
4. Executes the SQL against the SQLite database
5. Generates a business-friendly answer from the results

### RAG Pipeline

```bash
python src/rag/rag_answer.py
```

Asks: *"Why did APAC revenue increase in Q2 2026?"*

**How it works:**
1. Embeds the query using `all-MiniLM-L6-v2`
2. Retrieves the most relevant documents via cosine similarity
3. Passes the context and question to the LLM for answer generation

## Data Model

The SQLite database uses a **star schema**:

| Table | Description |
|---|---|
| `fact_revenue` | 90 records — revenue, cost, profit by year, quarter, client, region, product |
| `dim_client` | 5 clients (Alpha Capital, Beta Investments, etc.) |
| `dim_region` | 3 regions (APAC, EMEA, Americas) |
| `dim_product` | 3 products (Equities, Fixed Income, Derivatives) |

## Dependencies

| Package | Purpose |
|---|---|
| requests | Ollama API communication |
| pandas | Data manipulation |
| numpy | Cosine similarity computation |
| sentence-transformers | Text embeddings |
| torch | ML backend |
| scikit-learn | ML utilities |

## License

This project does not currently include a license.
