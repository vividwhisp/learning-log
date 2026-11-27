
import pytest
from unittest.mock import MagicMock, patch

from src.relevance_grader import grade_relevance


@pytest.fixture
def relevant_results():
    return [
        {
            "source": "kubernetes.md",
            "chunk_index": 1,
            "text": "A Kubernetes Deployment manages ReplicaSets and maintains the desired number of Pod replicas."
        }
    ]


@pytest.fixture
def irrelevant_results():
    return [
        {
            "source": "python.md",
            "chunk_index": 2,
            "text": "Python lists are mutable data structures that store ordered collections of elements."
        }
    ]


def mock_groq_response(content):
    response = MagicMock()
    response.choices[0].message.content = content
    return response


@patch("src.relevance_grader.Groq")
def test_relevant_documents(mock_groq, relevant_results):

    mock_client = mock_groq.return_value
    mock_client.chat.completions.create.return_value = mock_groq_response(
        '{"relevant": true, "score": 0.92, "reason": "Documents explain Kubernetes Deployments."}'
    )

    result = grade_relevance(
        "How do Kubernetes Deployments manage replicas?",
        relevant_results
    )

    assert result["relevant"] is True
    assert result["score"] == 0.92
    assert isinstance(result["reason"], str)


@patch("src.relevance_grader.Groq")
def test_irrelevant_documents(mock_groq, irrelevant_results):

    mock_client = mock_groq.return_value
    mock_client.chat.completions.create.return_value = mock_groq_response(
        '{"relevant": false, "score": 0.12, "reason": "Documents discuss Python lists, not Kubernetes."}'
    )

    result = grade_relevance(
        "How do Kubernetes Deployments manage replicas?",
        irrelevant_results
    )

    assert result["relevant"] is False
    assert result["score"] == 0.12


def test_empty_results():

    result = grade_relevance(
        "Explain Kubernetes Deployments",
        []
    )

    assert result["relevant"] is False
    assert result["score"] == 0.0


def test_empty_question(relevant_results):

    with pytest.raises(ValueError):
        grade_relevance("", relevant_results)


@patch("src.relevance_grader.Groq")
def test_invalid_json(mock_groq, relevant_results):

    mock_client = mock_groq.return_value
    mock_client.chat.completions.create.return_value = mock_groq_response(
        "This is not JSON"
    )

    with pytest.raises(Exception):
        grade_relevance(
            "Explain Kubernetes Deployments",
            relevant_results
        )
