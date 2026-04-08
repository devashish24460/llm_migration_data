def validate_mapping(mapping_output,target_schema):
    mapping = mapping_output.get("mapping",{})
    confidence = mapping_output.get("Confidence",0)
    
    
    target_fields = list(target_schema.values())[0].keys()

    mapped_targets = list(mapping.values())

    missing = [field for field in target_fields if field not in mapped_targets]

    if missing:
        raise Exception(f"Missing mappings for fields: {missing}")

    if confidence < 0.6:
        raise Exception("Low confidence mapping. Requires review")

    return True