from unittest.mock import patch

from ddgs.exceptions import RatelimitException, TimeoutException

from src.tools.web_search import web_search


@patch("src.tools.web_search.DDGS")
def test_formats_results_compactly(mock_ddgs):
    mock_ddgs.return_value.text.return_value = [
        {"title": "Gemini API Docs", "body": "Official docs for the Gemini API.", "href": "https://ai.google.dev"},
    ]
    result = web_search.run({"query": "Google Gemini API"})
    assert "1. Gemini API Docs" in result
    assert "https://ai.google.dev" in result


@patch("src.tools.web_search.DDGS")
def test_no_results(mock_ddgs):
    mock_ddgs.return_value.text.return_value = []
    result = web_search.run({"query": "asdkjfhaskdjfhaskjdfh"})
    assert "Keine Ergebnisse" in result


@patch("src.tools.web_search.DDGS")
def test_rate_limit_error_is_handled(mock_ddgs):
    mock_ddgs.return_value.text.side_effect = RatelimitException("rate limited")
    result = web_search.run({"query": "test"})
    assert "Fehler" in result


@patch("src.tools.web_search.DDGS")
def test_timeout_error_is_handled(mock_ddgs):
    mock_ddgs.return_value.text.side_effect = TimeoutException("timed out")
    result = web_search.run({"query": "test"})
    assert "Fehler" in result


@patch("src.tools.web_search.DDGS")
def test_long_snippet_is_truncated(mock_ddgs):
    mock_ddgs.return_value.text.return_value = [
        {"title": "Long", "body": "x" * 500, "href": "https://example.com"},
    ]
    result = web_search.run({"query": "test"})
    body_line = result.splitlines()[1].strip()
    assert len(body_line) == 200
