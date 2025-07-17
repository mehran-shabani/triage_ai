from .input import build_prompt
from .cleaner import parse_response
from .generate_response import format_output
from ..tasks import talkbot_complete


def request_missing_fields(missing_fields):
    messages = build_prompt(missing_fields)
    raw = talkbot_complete(messages)
    parsed = parse_response(raw)
    return format_output(parsed)
