import os
import re
from typing import Dict


class PlaceholderInjector:
    """
    A utility class for injecting environment variables into strings.
    Replaces placeholders like PLACEHOLDER_NAME with corresponding environment variable values.
    """

    def __init__(
        self,
        placeholder_pattern: str = r"PLACEHOLDER_([A-Z0-9_]+)",
    ):
        """
        Initialize the PlaceholderInjector with customizable pattern.

        Args:
            placeholder_pattern: Regex pattern to match placeholders.
                                Default finds PLACEHOLDER_NAME.
        """
        self.placeholder_pattern = re.compile(placeholder_pattern)
        self.custom_mappings: Dict[str, str] = {}

    def add_custom_mapping(self, placeholder: str, env_var: str) -> None:
        """
        Add a custom mapping from placeholder to environment variable name.

        Args:
            placeholder: The placeholder name without prefix (e.g., "FIREBASE_API_KEY")
            env_var: The environment variable name to use (e.g., "FIREBASE_WEB_API_KEY")
        """
        self.custom_mappings[placeholder] = env_var

    def inject(self, content: str, default_value: str = "") -> str:
        """
        Replace all placeholders in the content with values from environment variables.

        Args:
            content: The content containing placeholders
            default_value: Default value to use if environment variable is not set

        Returns:
            Content with placeholders replaced by environment variable values
        """

        def replace_match(match: re.Match) -> str:
            placeholder = match.group(1)

            # Check if we have a custom mapping for this placeholder
            if placeholder in self.custom_mappings:
                env_var = self.custom_mappings[placeholder]
            else:
                env_var = placeholder

            return os.environ.get(env_var, default_value)

        return self.placeholder_pattern.sub(replace_match, content)
