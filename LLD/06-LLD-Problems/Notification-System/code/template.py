"""
NotificationTemplate - Template system with placeholder substitution.
Supports {{variable}} syntax for dynamic content.
"""

import re


class NotificationTemplate:
    """Template for generating notification content with placeholders."""

    def __init__(self, template_id: str, subject_template: str, body_template: str):
        """
        Args:
            template_id: Unique template identifier.
            subject_template: Subject with {{placeholders}}.
            body_template: Body with {{placeholders}}.
        """
        self.template_id = template_id
        self.subject_template = subject_template
        self.body_template = body_template

    def render(self, variables: dict[str, str]) -> tuple[str, str]:
        """
        Render the template with the given variables.

        Args:
            variables: Dict of placeholder_name -> value.

        Returns:
            Tuple of (rendered_subject, rendered_body).
        """
        subject = self._substitute(self.subject_template, variables)
        body = self._substitute(self.body_template, variables)
        return subject, body

    @staticmethod
    def _substitute(template: str, variables: dict[str, str]) -> str:
        """Replace {{key}} placeholders with values from the variables dict."""
        def replacer(match: re.Match) -> str:
            key = match.group(1)
            return variables.get(key, f"[{key}]")
        return re.sub(r"\{\{(\w+)\}\}", replacer, template)
