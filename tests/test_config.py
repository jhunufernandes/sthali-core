"""Tests for sthali_core.config."""
import unittest
from unittest.mock import MagicMock, mock_open, patch

from pydantic import ValidationError

from sthali_core.config import Config, ConfigSchema


class TestConfigSchema(unittest.TestCase):

    def test_model_validate_empty_dict_succeeds(self) -> None:
        result = ConfigSchema.model_validate({})
        self.assertIsInstance(result, ConfigSchema)

    def test_model_validate_extra_fields_are_ignored(self) -> None:
        result = ConfigSchema.model_validate({"unexpected": "value"})
        self.assertIsInstance(result, ConfigSchema)

    def test_model_validate_non_dict_raises_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            ConfigSchema.model_validate("not a dict")


class TestConfig(unittest.TestCase):

    @patch.object(Config, "validate")
    @patch("sthali_core.config.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_init_opens_given_path(self, mock_file: MagicMock, mock_safe_load: MagicMock, mock_validate: MagicMock) -> None:
        mock_safe_load.return_value = {}
        Config("config.yaml")
        mock_file.assert_called_once_with("config.yaml")

    @patch.object(Config, "validate")
    @patch("sthali_core.config.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_init_stores_parsed_yaml(self, mock_file: MagicMock, mock_safe_load: MagicMock, mock_validate: MagicMock) -> None:
        expected = {"key": "value"}
        mock_safe_load.return_value = expected
        config = Config("config.yaml")
        self.assertEqual(config.yaml_config, expected)

    @patch.object(Config, "validate")
    @patch("sthali_core.config.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_init_calls_validate(self, mock_file: MagicMock, mock_safe_load: MagicMock, mock_validate: MagicMock) -> None:
        mock_safe_load.return_value = {}
        Config("config.yaml")
        mock_validate.assert_called_once()

    def test_init_raises_file_not_found_on_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            Config("__nonexistent__.yaml")

    @patch.object(Config, "validate")
    @patch("sthali_core.config.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sthali_core.config.getenv")
    def test_load_returns_config_instance(self, mock_getenv: MagicMock, mock_file: MagicMock, mock_safe_load: MagicMock, mock_validate: MagicMock) -> None:
        mock_getenv.return_value = "config.yaml"
        mock_safe_load.return_value = {}
        result = Config.load()
        self.assertIsInstance(result, Config)

    @patch.object(Config, "validate")
    @patch("sthali_core.config.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sthali_core.config.getenv")
    def test_load_calls_getenv_with_correct_key_and_default(self, mock_getenv: MagicMock, mock_file: MagicMock, mock_safe_load: MagicMock, mock_validate: MagicMock) -> None:
        mock_getenv.return_value = "config.yaml"
        mock_safe_load.return_value = {}
        Config.load()
        mock_getenv.assert_called_once_with("CONFIG_FILE_PATH", "config.yaml")

    @patch.object(Config, "validate")
    @patch("sthali_core.config.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sthali_core.config.getenv")
    def test_load_opens_path_returned_by_env(self, mock_getenv: MagicMock, mock_file: MagicMock, mock_safe_load: MagicMock, mock_validate: MagicMock) -> None:
        mock_getenv.return_value = "custom.yaml"
        mock_safe_load.return_value = {}
        Config.load()
        mock_file.assert_called_once_with("custom.yaml")

    def test_validate_calls_model_validate_with_yaml_config(self) -> None:
        config = Config.__new__(Config)
        config.yaml_config = {"key": "value"}
        with patch.object(Config.config_schema, "model_validate") as mock_mv:
            config.validate()
        mock_mv.assert_called_once_with({"key": "value"})

    def test_validate_propagates_validation_error(self) -> None:
        config = Config.__new__(Config)
        config.yaml_config = "not a dict"
        with self.assertRaises(ValidationError):
            config.validate()


if __name__ == "__main__":
    unittest.main()
```
