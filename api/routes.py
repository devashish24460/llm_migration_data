from fastapi import APIRouter, UploadFile, File
import pandas as pd
import json

from core.schema import analyze_schema
from core.llm_engine import generate_mapping
from core.validator import validate_mapping
from core.executor import execute_migration

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return analyze_schema(df)

@router.post("/generate-mapping")
async def generate_mapping_api(file: UploadFile = File(...), schema: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    target_schema = json.load(schema.file)

    source_info = analyze_schema(df)
    mapping_output = generate_mapping(source_info, target_schema)

    return mapping_output

@router.post("/execute")
async def execute(file: UploadFile = File(...), schema: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    target_schema = json.load(schema.file)

    source_info = analyze_schema(df)
    mapping_output = generate_mapping(source_info, target_schema)

    validate_mapping(mapping_output, target_schema)

    result_df, report = execute_migration(df, mapping_output)

    return {
        "report": report,
        "preview": result_df.head().to_dict()
    }