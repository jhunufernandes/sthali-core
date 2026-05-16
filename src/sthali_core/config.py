"""Configuration loading and validation."""
from os import getenv
from typing import Any, ClassVar, Self

from pydantic import BaseModel
from yaml import safe_load


class ConfigSchema(BaseModel):
    """Base Pydantic schema for configuration validation."""


class Config:
    """Loads and validates a YAML configuration file against a schema."""

    config_schema: ClassVar[type[ConfigSchema]] = ConfigSchema

    def __init__(self, config_file_path: str) -> None:
        """Read and validate the YAML file at the given path.

        Args:
            config_file_path: Path to the YAML configuration file.
        """
        self.yaml_config: Any
        with open(config_file_path) as f:  # noqa: PTH123
            self.yaml_config = safe_load(f)
        self.validate()

    @classmethod
    def load(cls) -> Self:
        """Load config from the path specified by the CONFIG_FILE_PATH env var.

        Returns:
            A validated Config instance.
        """
        config_file_path = getenv("CONFIG_FILE_PATH", "config.yaml")
        return cls(config_file_path)

    def validate(self) -> None:
        """Validate the loaded YAML data against the config schema."""
        self.config_schema.model_validate(self.yaml_config)
