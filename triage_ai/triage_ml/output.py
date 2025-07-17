
def prediction_to_message(ktas: int, flag: str | None = None) -> str:
    """Format prediction and flag into a human friendly message."""
    message = f"Patient likely falls under KTAS level {ktas}."
    if flag:
        message += f" {flag}"
    if ktas <= 3:
        message += " Immediate nurse review is recommended."
    return message
