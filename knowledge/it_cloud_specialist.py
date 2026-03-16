from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SpecialistQueryPlan:
    intent: str
    sub_queries: list[str]
    must_include_sources: list[str]
    response_shape: list[str]


class ITCloudSpecialist:
    def plan(self, user_query: str) -> SpecialistQueryPlan:
        lowered = user_query.lower()
        if "aws" in lowered and "architecture" in lowered:
            return SpecialistQueryPlan(
                intent="aws_architecture",
                sub_queries=[
                    user_query,
                    "aws reference architecture",
                    "aws security best practices",
                    "aws cost optimization checklist",
                ],
                must_include_sources=["aws_docs", "rfc_bulk"],
                response_shape=["requirements", "architecture", "security", "cost", "operations"],
            )
        if "kubernetes" in lowered or "k8s" in lowered:
            return SpecialistQueryPlan(
                intent="kubernetes_support",
                sub_queries=[
                    user_query,
                    "kubernetes troubleshooting",
                    "kubernetes production best practices",
                    "kubernetes networking and observability",
                ],
                must_include_sources=["kubernetes_docs", "stackexchange_dump"],
                response_shape=["root_cause", "commands", "fix", "prevention"],
            )
        return SpecialistQueryPlan(
            intent="general_it",
            sub_queries=[user_query, "official docs", "best practices", "real world postmortem"],
            must_include_sources=["stackexchange_dump"],
            response_shape=["summary", "deep_dive", "commands", "tradeoffs"],
        )
