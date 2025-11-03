from enum import Enum, auto
import subprocess
from pathlib import Path
from typing import Protocol, runtime_checkable

class MultiplexerType(str, Enum):
    WINDOWS_TERMINAL = auto()
    TMUX = auto()
    ZELLIJ = auto()

class InterfaceType(str, Enum):
    JUPYTER_CONSOLE = auto()
    EUPORIE_CONSOLE = auto()

@runtime_checkable
class Multiplexer(Protocol):
    def open(
        self,
        project_dir: Path,
        command: list[str],
        profile: str | None
    ):
        ... 

@runtime_checkable
class NotebookInterface(Protocol):

    def build_command(self, connection_file: Path) -> list[str]:
        ...

class WindowsTerminal(Multiplexer):
    def open(self, project_dir: Path, command: list[str], profile: str | None = None) -> None:
        args = [
            "wt", "-w", "0", "sp", "-v", "-d", str(project_dir),
        ]
        if profile:
            args += ["--profile", profile]
        args += ["cmd.exe", "/k"] + command
        subprocess.Popen(args, cwd=project_dir)

#Not tested
class Tmux(Multiplexer):
    def open(self, project_dir: Path, command: list[str], profile: str | None = None) -> None:
        subprocess.Popen(["tmux", "new-window"] + command, cwd=project_dir)

#Not Tested
class Zellij(Multiplexer):
    def open(self, project_dir: Path, command: list[str], profile: str | None = None) -> None:
        subprocess.Popen(["zellij", "action", "new-tab", "--"] + command, cwd=project_dir)

class JupyterConsole(NotebookInterface):
    def build_command(self, connection_file: Path) -> list[str]:
        return [
            "uv", "run", "jupyter", "console",
            "--existing", str(connection_file),
            "--ZMQTerminalInteractiveShell.include_other_output", "True",
            "--ZMQTerminalInteractiveShell.other_output_prefix", "''",
            "--ZMQTerminalInteractiveShell.true_color", "True",
        ]

class EuporieConsole(NotebookInterface):
    def build_command(self, connection_file: Path) -> list[str]:
        return [
            "uv", "run", "euporie-console",
            "--connection-file", str(connection_file),
            "--show-remote-inputs",
            "--show-remote-outputs",
        ]

def open_multiplexer(
    mux: Multiplexer,
    interface: NotebookInterface,
    project_dir: Path,
    connection_file: Path,
    *,
    profile: str | None = None,
) -> None:
    """Run the given notebook interface in a given multiplexer."""
    command = interface.build_command(connection_file)
    mux.open(project_dir, command, profile=profile)
