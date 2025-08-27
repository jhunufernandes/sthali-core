"""Dynamically creates an Enum for available clients."""

import enum
import importlib
import pathlib
import types
import typing

__all__ = [
    "Config",
]


class Config:
    """Discovers and provides an Enum for client modules."""

    def __init__(self, parent_path: pathlib.Path) -> None:
        """Initialize Config.

        Args:
            parent_path: The parent directory path where the 'clients' subdirectory resides.
        """
        self.clients_directory = parent_path / "clients"
        self.package = parent_path.name

    @property
    def _clients_map(self) -> dict[str, types.ModuleType]:
        clients_file_path = list(filter(lambda file: file.stem != "__init__", self.clients_directory.glob("*.py")))
        return {
            file_path.stem: importlib.import_module(self._relative_to_formatted(file_path), package=self.package)
            for file_path in clients_file_path
        }

    @property
    def enum(self) -> type[enum.Enum]:
        """Dynamically create an Enum representing available clients.

        The Enum members will have names and values corresponding to the client names.

        Returns:
            An Enum type where members are the discovered client names.
        """
        client_enum_map = {k: k for k in self._clients_map}
        return enum.Enum("ClientEnum", client_enum_map)

    def _relative_to_formatted(self, path: pathlib.Path) -> str:
        src_path = next(filter(lambda x: x.name in ["src", "site-packages"], self.clients_directory.parents))
        return str(path.relative_to(src_path)).removesuffix(".py").replace("/", ".")

    def get_client(self, client_name: str, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Dynamically instantiate and return a client class based on the provided client name.

        Args:
            client_name (str): The name of the client to instantiate. Must match a client module and class.
            *args (typing.Any): Positional arguments to pass to the client class constructor.
            **kwargs (typing.Any): Keyword arguments to pass to the client class constructor.

        Returns:
            Any: An instance of the requested client class.
        """
        client_module = self._clients_map[client_name]
        client_class = getattr(client_module, f"{client_name.title()}Client")
        return client_class(*args, **kwargs)
