from fastapi.testclient import TestClient
from unittest.mock import Mock
from code_intelligence.api.app import app
import code_intelligence.api.routes as routes


def test_index_repository():
    mock_app = Mock()
    routes._application = mock_app

    client = TestClient(app)
    response = client.post("/index", json={"repository_path": "test_path"})

    assert response.status_code == 200
    assert response.json() == {"message": "Repository indexed successfully."}
    mock_app.index.assert_called_once_with("test_path")


def test_index_repository_url():
    mock_app = Mock()
    routes._application = mock_app

    client = TestClient(app)
    response = client.post("/index", json={"repository_url": "https://github.com/test/repo"})

    assert response.status_code == 200
    assert response.json() == {"message": "Repository indexed successfully."}
    mock_app.index.assert_called_once_with("https://github.com/test/repo")


def test_index_repository_missing_args():
    mock_app = Mock()
    routes._application = mock_app

    client = TestClient(app)
    response = client.post("/index", json={})

    assert response.status_code == 400
    assert "repository_path or repository_url is required." in response.json()["detail"]


def test_index_repository_swagger_defaults():
    mock_app = Mock()
    routes._application = mock_app

    client = TestClient(app)
    response = client.post(
        "/index",
        json={"repository_path": "string", "repository_url": "https://github.com/test/repo"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Repository indexed successfully."}
    mock_app.index.assert_called_once_with("https://github.com/test/repo")


def test_ask():
    mock_app = Mock()
    routes._application = mock_app
    mock_app.ask.return_value = "mocked_answer"

    client = TestClient(app)
    response = client.post("/ask", json={"question": "What is X?"})

    assert response.status_code == 200
    assert response.json() == {"answer": "mocked_answer"}
    mock_app.ask.assert_called_once_with("What is X?")
