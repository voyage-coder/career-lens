
import pytest

from app.ai.analyzer import (
    find_skills,
    analyze_resume,
    match_job_description
)


def test_find_skills():
    result = find_skills(
        "I know Python, React, SQL and MongoDB."
    )

    assert "python" in result
    assert "react" in result
    assert "sql" in result
    assert "mongodb" in result


def test_find_skills_case_insensitive():
    result = find_skills("PYTHON and REACT")

    assert "python" in result
    assert "react" in result


def test_analyze_complete_resume():
    text = (
        "Education Experience Projects Skills Certifications "
        "Python Java React SQL MongoDB. "
        "navya@example.com "
    ) * 30

    result = analyze_resume(text)

    assert result["ats_score"] > 0
    assert result["readability_score"] >= 0
    assert len(result["skills"]) > 0
    assert len(result["sections_found"]) == 5


def test_analyze_resume_missing_sections():
    text = "Python Java React SQL MongoDB. " * 10

    result = analyze_resume(text)

    assert len(result["missing_sections"]) > 0
    assert "education" in result["missing_sections"]


def test_analyze_short_resume():
    text = "Python developer with React skills."

    result = analyze_resume(text)

    assert result["word_count"] < 250
    assert result["ats_score"] >= 0
    assert any("short" in w.lower() for w in result["weaknesses"])


def test_job_description_matching():
    resume = "Python Java React SQL MongoDB"
    job = "Python React SQL Docker AWS"

    result = match_job_description(resume, job)

    assert result["matched_skills"] == ["python", "react", "sql"]
    assert result["missing_skills"] == ["aws", "docker"]
    assert result["match_percentage"] == 60


def test_job_description_without_skills():
    resume = "I am a hardworking student."
    job = "We need a motivated candidate."

    result = match_job_description(resume, job)

    assert result["match_percentage"] == 0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
