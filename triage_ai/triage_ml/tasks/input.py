
def build_prompt(missing_fields):
    """Create system and user messages for missing data."""
    user = "Please provide the following fields: " + ", ".join(missing_fields)
    return [
        {"role": "system", "content": "You are an ER triage nurse assistant."},
        {"role": "user", "content": user},
    ]
