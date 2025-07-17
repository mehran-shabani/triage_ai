from triage_ai.triage_ml.tasks import talkbot_complete


def test_talkbot(monkeypatch):
    def mock_post(url, headers=None, data=None, timeout=10):
        class Resp:
            status_code = 200

            def json(self):
                return {"choices": [{"message": {"content": "ok"}}]}

        return Resp()

    monkeypatch.setattr('requests.post', mock_post)
    data = talkbot_complete([{"role": "user", "content": "hi"}])
    assert data["choices"][0]["message"]["content"] == "ok"
