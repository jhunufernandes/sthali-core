"""{...}."""
from os import getenv

from pydantic import BaseModel
from yaml import safe_load


class ConfigSchema(BaseModel):
    pass


class Config:
    """{...}."""
    config_schema = ConfigSchema

    def __init__(self, config_file_path: str) -> None:
        """{...}."""
        with open(config_file_path) as f:
            self.yaml_config = safe_load(f)
        self._validate()

    @staticmethod
    def get_config_file_path() -> str:
        return getenv("CONFIG_FILE_PATH", "config.yaml")

    @classmethod
    def load(cls) -> "Config":
        config_file_path = cls.get_config_file_path()
        return cls(config_file_path)

    def _validate(self) -> None:
        self.config_schema.model_validate(self.yaml_config)
