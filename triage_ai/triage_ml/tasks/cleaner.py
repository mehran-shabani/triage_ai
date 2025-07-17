
def parse_response(data):
    """Extract message and missing fields from TalkBot response."""
    message = data.get("message", "")
    context = data.get("context", {})
    missing = context.get("missing_fields", [])
    return {"message": message, "missing_fields": missing}
