# llm-data-migration


# LLM Data Migration Engine

An intelligent data migration system that uses LLMs to automatically map legacy schemas to structured formats and generate transformation logic.

##  Features

- Automatic schema mapping using LLM
- Data cleaning and transformation
- Validation layer to prevent incorrect mappings
- Retry + JSON correction for LLM reliability
- FastAPI-based API for execution

## How it Works

1. Analyze source schema (column names + sample values)
2. Use LLM to generate mapping + transformations
3. Validate mapping (confidence + structure)
4. Execute transformation pipeline
5. Output cleaned dataset + report

## ⚙️ Tech Stack

- FastAPI
- Pandas
- Groq (LLM inference)
- Python

## API Endpoints

- `/analyze` → Analyze dataset schema  
- `/generate-mapping` → Generate mapping using LLM  
- `/execute` → Run full migration pipeline  

## Example Use Case

Upload messy CSV:
