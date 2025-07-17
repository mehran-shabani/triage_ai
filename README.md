# Triage AI

This project provides a KTAS-based triage API built with Django and DRF.

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoint

`POST /api/triage/predict/`

See `codex_build.md` for request and response specifications.

## TalkBot Integration

Configure the `TALKBOT_API_KEY` environment variable to enable NLP features.

## Reference

See `docs/triage.pdf` for clinical guidelines and pain-related mis-triage errors.
