from __future__ import annotations

import os
import re

from .cv_profile import (
    certifications_text,
    contact_text,
    education_text,
    employer_text,
    experience_text,
    internships_text,
    languages_text,
    location_text,
    recruiter_summary_text,
    skills_text,
    summary_text,
)


def select_model(message: str) -> str:
    lowered = message.lower()
    score = 0
    score += min(len(message.split()) // 20, 5)
    score += 2 if any(word in lowered for word in ["experience", "certification", "skill", "education"]) else 0
    if score <= 3:
        return "gemini_flash"
    if score <= 7:
        return "groq_llama"
    return "thinker"


def generate_response(model_used: str, prompt: dict) -> str:
    mode = os.getenv("MODEL_MODE", "mock")
    user_message = prompt["user"].strip()
    if mode != "mock":
        return f"Live provider mode is configured, but provider integration is still abstracted. Request: {user_message}"

    stripped_message, _ = extract_mode(user_message)
    first_person = wants_first_person(stripped_message)
    lowered = normalize_message(resolve_profile_pronouns(stripped_message, first_person)).lower()

    if asks_where_he_lives(lowered):
        return finalize(
            polish_location(first_person),
            [
                "What is his current role at DXC Technology?",
                "Give me a recruiter-style summary of his profile.",
                "What certifications does he have?",
            ],
        )
    if asks_for_contact(lowered):
        return finalize(
            polish_contact(first_person),
            [
                "What are his current role and responsibilities?",
                "What are his core skills?",
                "How do his certifications strengthen his profile?",
            ],
        )
    if asks_where_he_works(lowered):
        return finalize(
            polish_employer(first_person),
            [
                "Give me the full technical deep-dive with step-by-step process.",
                "What tools and platforms does he work with?",
                "Summarize his DXC role for a recruiter.",
            ],
        )
    if asks_for_certifications(lowered):
        return finalize(
            polish_certifications(first_person),
            [
                "How do his AWS and Oracle certifications support his profile?",
                "Tell me about his education path too.",
                "Give me a concise recruiter summary that includes these credentials.",
            ],
        )
    if asks_for_education(lowered):
        return finalize(
            polish_education(first_person),
            [
                "How does his Diploma in Electronics Engineering connect to his infrastructure work?",
                "Tell me about his internships and early career exposure.",
                "How does his education support his current DXC role?",
            ],
        )
    if asks_for_skills(lowered):
        return finalize(
            polish_skills(first_person),
            [
                "Connect these skills to his daily responsibilities at DXC Technology.",
                "Explain his ITSM and infrastructure strengths in more depth.",
                "Which certifications align best with these skills?",
            ],
        )
    if asks_for_languages(lowered):
        return finalize(
            polish_languages(first_person),
            [
                "Show me his contact details too.",
                "Give me a recruiter summary of his overall profile.",
                "Tell me about his internships and early experience.",
            ],
        )
    if asks_for_internships(lowered):
        return finalize(
            polish_internships(first_person),
            [
                "How do these early experiences connect to his current DXC role?",
                "Tell me about his education journey next.",
                "Give me a broader summary of his professional profile.",
            ],
        )
    if asks_for_recruiter_summary(lowered):
        return finalize(
            polish_recruiter_summary(first_person),
            [
                "Break down his DXC responsibilities in more detail.",
                "Tell me about his certifications and technical strengths.",
                "Give me a compact 3-line version for recruiter screening.",
            ],
        )
    if asks_for_experience(lowered):
        return finalize(
            polish_experience(first_person),
            [
                "Give me the full technical deep-dive with step-by-step process.",
                "How does he handle Change Management from RFC to PIR?",
                "Tell me more about his patching, Windows Server, and access management work.",
            ],
        )
    if asks_about_kumar_nikhil(lowered):
        return finalize(
            polish_summary(first_person),
            [
                "Where does he work right now?",
                "Show me his certifications and technical skills.",
                "Give me a recruiter-style introduction to his profile.",
            ],
        )
    return exact_fallback()


def extract_mode(message: str) -> tuple[str, str]:
    match = re.match(r"\[mode:(?P<mode>[^\]]+)\]\s*(?P<body>.*)", message, re.IGNORECASE)
    if not match:
        return message, "standard"
    return match.group("body").strip(), match.group("mode").strip().lower()


def normalize_message(message: str) -> str:
    cleaned = message.strip()
    cleaned = re.sub(r"^(hey|hi|hello)[,\s]+", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def wants_first_person(message: str) -> bool:
    lowered = message.lower()
    return any(
        phrase in lowered
        for phrase in [
            "switch to first person",
            "speak as kumar",
            "interview me as kumar",
            "talk as kumar",
            "reply as kumar",
        ]
    )


def resolve_profile_pronouns(message: str, first_person: bool) -> str:
    if first_person:
        return message.strip()
    resolved = f" {message.strip()} "
    resolved = re.sub(r"\bhe\b", "Kumar Nikhil", resolved, flags=re.IGNORECASE)
    resolved = re.sub(r"\bhim\b", "Kumar Nikhil", resolved, flags=re.IGNORECASE)
    resolved = re.sub(r"\bhis\b", "Kumar Nikhil's", resolved, flags=re.IGNORECASE)
    return resolved.strip()


def asks_for_contact(lowered: str) -> bool:
    return any(token in lowered for token in ["contact", "email", "phone", "location", "address"])


def asks_where_he_lives(lowered: str) -> bool:
    return any(
        token in lowered
        for token in [
            "where does kumar nikhil live",
            "where does nikhil live",
            "where is kumar nikhil from",
            "where is kumar nikhil based",
            "where does kumar nikhil reside",
            "kumar nikhil live",
            "kumar nikhil lives",
            "kumar nikhil stay",
            "kumar nikhil stays",
        ]
    )


def asks_for_certifications(lowered: str) -> bool:
    return "certification" in lowered or "certified" in lowered


def asks_for_education(lowered: str) -> bool:
    return any(token in lowered for token in ["education", "study", "degree", "college", "university", "diploma"])


def asks_for_skills(lowered: str) -> bool:
    return any(token in lowered for token in ["skills", "technologies", "tools", "tech stack", "strengths"])


def asks_for_experience(lowered: str) -> bool:
    return any(token in lowered for token in ["experience", "responsibilities", "responsibility", "worked", "dxc", "job", "role", "itsm", "infrastructure", "what does kumar nikhil do"])


def asks_where_he_works(lowered: str) -> bool:
    return any(
        pattern in lowered
        for pattern in [
            "where does kumar nikhil work",
            "does kumar nikhil work at",
            "which company",
            "current company",
            "employer",
            "where is kumar nikhil working",
        ]
    )


def asks_for_languages(lowered: str) -> bool:
    return "language" in lowered or "speak" in lowered


def asks_for_internships(lowered: str) -> bool:
    return "internship" in lowered or "training" in lowered or "student partner" in lowered or "campus ambassador" in lowered


def asks_for_recruiter_summary(lowered: str) -> bool:
    return any(token in lowered for token in ["recruiter summary", "summary", "profile summary", "introduce", "about kumar nikhil", "career summary"])


def asks_about_kumar_nikhil(lowered: str) -> bool:
    return any(
        token in lowered
        for token in [
            "kumar nikhil",
            "nikhil",
            "who is kumar",
            "profile",
        ]
    )


def exact_fallback() -> str:
    return (
        "That specific detail isn’t in Kumar’s CV. Instead, would you like to know about his current role at DXC Technology, "
        "his certifications, or his core skills?\n\n"
        "Would you like to know about his DXC responsibilities?\n"
        "Would you like to explore his certifications?\n"
        "Would you like a summary of his strongest technical skills?"
    )


def finalize(answer: str, follow_ups: list[str]) -> str:
    chosen = follow_ups[:3]
    return answer + "\n\n" + "\n".join(chosen)


def exact_fallback() -> str:
    return (
        "That specific detail isn't in Kumar's CV. Instead, you can ask about his current role at DXC Technology, "
        "his certifications, or his core skills.\n\n"
        "What are his DXC responsibilities?\n"
        "What certifications does he have?\n"
        "What are his strongest technical skills?"
    )


def polish_summary(first_person: bool) -> str:
    base = summary_text()
    if first_person:
        return (
            f"I am an IT Service Management and Infrastructure professional with strong hands-on experience across Change Management, "
            f"Incident Management, and Service Request operations in large-scale enterprise environments. {base} "
            "What makes the profile especially strong is the mix of operations discipline, infrastructure exposure, and client-facing knowledge transfer. "
            "It is the kind of background that fits high-responsibility support and governance-heavy enterprise environments well."
        )
    return (
        f"Kumar Nikhil is an IT Service Management and Infrastructure professional with strong hands-on experience across Change Management, "
        f"Incident Management, and Service Request operations in large-scale enterprise environments. {base} "
        "What makes his profile stand out is that he combines operational discipline with technical infrastructure exposure and client-facing coordination. "
        "That gives him a solid blend of execution, governance, and support reliability."
    )


def polish_location(first_person: bool) -> str:
    if first_person:
        return "I live in Palam, New Delhi, India."
    return "Kumar Nikhil lives in Palam, New Delhi, India."


def polish_contact(first_person: bool) -> str:
    base = contact_text().replace("Kumar Nikhil lives", "He lives")
    if first_person:
        return (
            "I live in Palam, New Delhi, India, and my contact details in the CV are phone 9315600875 and email nkashyapnikhilnk@gmail.com. "
            "This makes the profile easy for recruiters and hiring teams to follow up on directly."
        )
    return (
        "Kumar Nikhil lives in Palam, New Delhi, India, and his CV lists phone 9315600875 and email nkashyapnikhilnk@gmail.com. "
        "That gives recruiters a direct way to connect with him for role discussions or interviews. "
        "The contact section is simple, clean, and immediately usable."
    )


def polish_employer(first_person: bool) -> str:
    if first_person:
        return (
            "I currently work at DXC Technology as an Analyst III in Infrastructure Services, and I have been in that role since July 2022. "
            "My work sits at the intersection of IT service operations, infrastructure coordination, and governance-heavy enterprise support. "
            "In practical terms, that means I help keep systems stable, changes controlled, and incidents resolved without losing sight of SLA and OLA commitments."
        )
    return (
        "Kumar Nikhil currently works at DXC Technology as an Analyst III in Infrastructure Services, and he has been in that role since July 2022. "
        "His work sits at the intersection of IT service operations, infrastructure coordination, and governance-heavy enterprise support. "
        "In practical terms, that means he helps keep systems stable, changes controlled, and incidents resolved while staying aligned to SLA and OLA expectations."
    )


def polish_experience(first_person: bool) -> str:
    if first_person:
        return (
            "I work in a role where stability, control, and response quality matter every day. "
            "At DXC Technology, I handle Incident Management, Change Management, and Service Requests across enterprise environments using tools like ServiceNow and HPE Service Manager. "
            "I validate RFCs before CAB and eCAB decisions, coordinate with infrastructure, application, network, security, storage, and vendor teams, and support patching, Windows Server troubleshooting, access workflows, and CMDB accuracy. "
            "The business value is simple: fewer surprises in production, better control during change windows, and faster recovery when something breaks. "
            "Kumar has survived more midnight patch windows than he cares to count, and coffee was clearly his silent partner."
        )
    return (
        "Kumar Nikhil works in a role where stability, control, and response quality matter every day. "
        "At DXC Technology, he handles Incident Management, Change Management, and Service Requests across enterprise environments using tools like ServiceNow and HPE Service Manager. "
        "He validates RFCs before CAB and eCAB decisions, coordinates with infrastructure, application, network, security, storage, and vendor teams, and supports patching, Windows Server troubleshooting, access workflows, and CMDB accuracy. "
        "The business value is straightforward: fewer surprises in production, better control during change windows, and faster recovery when something breaks. "
        "Kumar has survived more midnight patch windows than he cares to count, and coffee was very likely his silent partner."
    )


def polish_skills(first_person: bool) -> str:
    base = skills_text()
    if first_person:
        return (
            f"{base} "
            "What is especially useful here is how these skills connect across process and infrastructure, rather than sitting in separate silos. "
            "The profile shows strength in ITSM discipline, enterprise tooling, server support, access control, patch governance, and operational reporting. "
            "That combination makes the role fit strong for support environments where execution quality and control matter as much as technical handling."
        )
    return (
        f"{base} "
        "What is especially useful here is how these skills connect across process and infrastructure, rather than sitting in separate silos. "
        "His profile shows strength in ITSM discipline, enterprise tooling, server support, access control, patch governance, and operational reporting. "
        "That combination makes him a strong fit for support environments where execution quality and control matter as much as technical handling."
    )


def polish_certifications(first_person: bool) -> str:
    base = certifications_text()
    if first_person:
        return (
            f"{base} "
            "These certifications strengthen my profile by showing breadth across cloud, data, networking, and business intelligence foundations. "
            "Even though the role is heavily service and infrastructure focused, the certifications help show that I understand wider technology ecosystems beyond day-to-day operations. "
            "That makes the profile more rounded for future growth into broader infrastructure, cloud, or platform-facing roles."
        )
    return (
        f"{base} "
        "These certifications strengthen his profile by showing breadth across cloud, data, networking, and business intelligence foundations. "
        "Even though his current role is heavily service and infrastructure focused, the certifications show that he understands wider technology ecosystems beyond day-to-day operations. "
        "That makes his profile more rounded for future growth into broader infrastructure, cloud, or platform-facing roles."
    )


def polish_education(first_person: bool) -> str:
    base = education_text()
    if first_person:
        return (
            f"{base} "
            "The education journey shows a practical progression from early IT foundations to electronics engineering and then into Computer Science and Engineering. "
            "That progression helps explain why I am comfortable with structured troubleshooting, systems thinking, and enterprise support work. "
            "It gives the CV a clear foundation-to-career story rather than a disconnected list of qualifications."
        )
    return (
        f"{base} "
        "The education journey shows a practical progression from early IT foundations to electronics engineering and then into Computer Science and Engineering. "
        "That progression helps explain why he is comfortable with structured troubleshooting, systems thinking, and enterprise support work. "
        "It gives the CV a clear foundation-to-career story rather than a disconnected list of qualifications."
    )


def polish_internships(first_person: bool) -> str:
    base = internships_text()
    if first_person:
        return (
            f"{base} "
            "These early roles may look lighter than the current DXC work, but they show something useful: communication, outreach, coordination, and campus-level representation. "
            "Those experiences matter because enterprise support is not only technical, it also depends on clarity, ownership, and working well with people. "
            "In that sense, the internships quietly support the stronger professional discipline visible later in the CV."
        )
    return (
        f"{base} "
        "These early roles may look lighter than his current DXC work, but they show something useful: communication, outreach, coordination, and campus-level representation. "
        "Those experiences matter because enterprise support is not only technical, it also depends on clarity, ownership, and working well with people. "
        "In that sense, the internships quietly support the stronger professional discipline visible later in the CV."
    )


def polish_languages(first_person: bool) -> str:
    base = languages_text()
    if first_person:
        return (
            f"{base} "
            "Fluency in both English and Hindi gives me a practical communication advantage in professional and client-facing environments. "
            "That matters in KT sessions, transition discussions, reporting, and day-to-day collaboration across teams. "
            "It is a small section in the CV, but it supports the broader picture of reliable communication."
        )
    return (
        f"{base} "
        "Fluency in both English and Hindi gives him a practical communication advantage in professional and client-facing environments. "
        "That matters in KT sessions, transition discussions, reporting, and day-to-day collaboration across teams. "
        "It is a small section in the CV, but it supports the broader picture of reliable communication."
    )


def polish_recruiter_summary(first_person: bool) -> str:
    base = recruiter_summary_text()
    if first_person:
        return (
            f"{base} "
            "The strongest part of my profile is that it combines technical operations with discipline, process ownership, and cross-team coordination. "
            "For a recruiter, that means I am not just familiar with tools, I am used to environments where accountability and production stability matter. "
            "It is the kind of profile that feels dependable in enterprise infrastructure and IT service operations."
        )
    return (
        f"{base} "
        "The strongest part of his profile is that it combines technical operations with discipline, process ownership, and cross-team coordination. "
        "For a recruiter, that means he is not just familiar with tools, he is used to environments where accountability and production stability matter. "
        "It is the kind of profile that feels dependable in enterprise infrastructure and IT service operations."
    )
