from __future__ import annotations


class CloudOperations:
    """Legacy provider dispatch kept intentionally simple for the evaluation."""

    def delete_external_resource(self, provider: str, external_id: str) -> str:
        if provider == "aws":
            return f"aws:deleted:{external_id}"
        if provider == "azure":
            return f"azure:deleted:{external_id}"
        raise ValueError(f"unsupported provider: {provider}")

    def health_check(self, provider: str) -> str:
        if provider == "aws":
            return "aws:ok"
        if provider == "azure":
            return "azure:ok"
        raise ValueError(f"unsupported provider: {provider}")
