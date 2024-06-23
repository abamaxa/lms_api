from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_summarize_text():
    response = client.post(
        "/api/v1/summarize",
        json={
            "text": "FastAPI is a modern, fast (high-performance), web "
            "framework for building APIs with Python 3.6+ based on "
            "standard Python type hints. The key features are: Fast, "
            "Fast to code, Fewer bugs, Intuitive, Easy, Short, Robust, "
            "Standards-based.",
            "max_length": 30,
            "min_length": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "original_length" in data
    assert "summary_length" in data

    count_words = len(data["summary"].split())

    assert count_words <= 30
    assert count_words >= 10


def test_invalid_input_too_short():
    response = client.post(
        "/api/v1/summarize",
        json={"text": "Too short", "max_length": 50, "min_length": 20},
    )
    assert response.status_code == 422


def test_invalid_input_too_long():
    response = client.post(
        "/api/v1/summarize",
        json={"text": "T" * 1001, "max_length": 50, "min_length": 20},
    )
    assert response.status_code == 422
