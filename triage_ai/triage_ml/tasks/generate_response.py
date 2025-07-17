
def format_output(data):
    """Return final message string from parsed response."""
    msg = data.get("message", "")
    if data.get("missing_fields"):
        fields = ", ".join(data["missing_fields"])
        msg += f" (missing: {fields})"
    return msg
