from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "kumar_nikhil_cv.json"


@lru_cache(maxsize=1)
def load_cv_profile() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def summary_text() -> str:
    profile = load_cv_profile()
    return profile["summary"]


def contact_text() -> str:
    identity = load_cv_profile()["identity"]
    return (
        f"Kumar Nikhil lives in {identity['location']}. "
        f"Phone: {identity['phone']}. Email: {identity['email']}."
    )


def location_text() -> str:
    identity = load_cv_profile()["identity"]
    return f"Kumar Nikhil lives in {identity['location']}."


def employer_text() -> str:
    role = load_cv_profile()["experience"][0]
    return (
        f"Kumar Nikhil currently works at {role['company']} as {role['role']} "
        f"({role['duration']})."
    )


def experience_text() -> str:
    role = load_cv_profile()["experience"][0]
    highlights = "; ".join(role["highlights"][:5])
    return (
        f"Kumar Nikhil works at {role['company']} as {role['role']} ({role['duration']}). "
        f"Key responsibilities include: {highlights}."
    )


def skills_text() -> str:
    skills = load_cv_profile()["skills"]
    return "Kumar Nikhil's core skills include: " + "; ".join(skills) + "."


def certifications_text() -> str:
    certifications = load_cv_profile()["certifications"]
    return "Kumar Nikhil's certifications are: " + "; ".join(certifications) + "."


def education_text() -> str:
    education = load_cv_profile()["education"]
    return "Kumar Nikhil's education includes: " + "; ".join(education) + "."


def internships_text() -> str:
    internships = load_cv_profile()["internships"]
    return "Kumar Nikhil's trainings and internships include: " + "; ".join(internships) + "."


def languages_text() -> str:
    languages = load_cv_profile()["languages"]
    return "Kumar Nikhil's languages are: " + "; ".join(languages) + "."


def recruiter_summary_text() -> str:
    role = load_cv_profile()["experience"][0]
    return (
        f"Kumar Nikhil is an IT Service Management and Infrastructure professional currently working at "
        f"{role['company']} as {role['role']}. He has hands-on experience in incident management, change management, "
        f"service request operations, Windows Server support, patch coordination, Active Directory, PAM, VMware, "
        f"NetApp, CMDB operations, KT delivery, and ITIL-aligned service governance."
    )
