"""Workflow definitions for different agent types

This module loads workflow definitions from markdown template files,
making it easier to maintain and version control workflow content.
"""

from pathlib import Path


class AgentWorkflows:
    """Workflow definitions for different agent types

    Workflows are loaded from markdown template files in the
    templates/workflows/ directory, allowing for easier maintenance
    and version control of workflow content.
    """

    # Supported workflow types
    WORKFLOW_TYPES = [
        "code-review",
        "deployment",
        "testing",
        "documentation",
        "security",
        "general-purpose",
    ]

    @classmethod
    def _load_workflow_template(cls, workflow_type: str) -> str:
        """Load a workflow template from a markdown file

        Args:
            workflow_type: The type of workflow to load (e.g., 'code-review')

        Returns:
            str: The workflow template content

        Raises:
            FileNotFoundError: If the template file doesn't exist
        """
        current_dir = Path(__file__).parent
        template_file = current_dir.parent / "templates" / "workflows" / f"{workflow_type}.md"

        if not template_file.exists():
            raise FileNotFoundError(
                f"Workflow template not found: {template_file}\n"
                f"Available workflows: {', '.join(cls.WORKFLOW_TYPES)}"
            )

        return template_file.read_text(encoding="utf-8")

    @classmethod
    def get_workflow(cls, agent_type: str) -> str:
        """Get the workflow definition for a specific agent type

        Args:
            agent_type: The type of agent (e.g., 'code-review', 'deployment')

        Returns:
            str: The workflow definition as a string

        Note:
            If the agent_type is not found, falls back to 'general-purpose'
        """
        # Normalize agent type (handle potential variations)
        normalized_type = agent_type.lower().replace("_", "-")

        # Try to get the specific workflow
        try:
            if normalized_type in cls.WORKFLOW_TYPES:
                return cls._load_workflow_template(normalized_type)
        except FileNotFoundError:
            pass

        # Fall back to general-purpose if specific workflow not found
        try:
            return cls._load_workflow_template("general-purpose")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No workflow templates found. Please ensure templates/workflows/ directory exists."
            )
