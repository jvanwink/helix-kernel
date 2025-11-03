from enum import Enum, auto, StrEnum
import typer
from pathlib import Path
from .kernel_manager import KernelManager
from .executor import execute_code

from .multiplexers import (
    JupyterConsole,
    Tmux,
    WindowsTerminal,
    EuporieConsole,
    Zellij,
    open_multiplexer,
)

app = typer.Typer(help="Helix Jupyter kernel manager")

class MultiplexerOption(StrEnum):
    TMUX = auto()
    WINDOWS_TERMINAL = auto()
    ZELLIJ = auto()
    NONE = auto()

class InterfaceOption(StrEnum):
    JUPYTER =  auto()
    EUPORIE = auto()

@app.command()
def start(
    mux: MultiplexerOption = typer.Option(MultiplexerOption.NONE, help="Multiplexer to attach"),
    interface: InterfaceOption = typer.Option(InterfaceOption.EUPORIE, "--interface", help="Notebook interface"),   
    project_dir: Path = typer.Option(".", help="Project directory"),
    profile: str | None = typer.Option(None, "--profile", "-p", help="Optional terminal profile")
):
    """Start a Jupyter kernel (and optionally open a console)."""
    km = KernelManager(project_dir)
    connection_file = km.start_kernel()
    typer.echo(f"Kernel started: {connection_file}")

    match mux:
        case MultiplexerOption.NONE:
            return
        case MultiplexerOption.WINDOWS_TERMINAL:
            mux_instance = WindowsTerminal()
        case MultiplexerOption.TMUX:
            mux_instance = Tmux()
        case MultiplexerOption.ZELLIJ:
            mux_instance = Zellij()
        case _:
            raise typer.BadParameter(f"Unsuported multiplexer: {mux}")

    match interface:
        case InterfaceOption.JUPYTER:
            interface_instance = JupyterConsole()
        case InterfaceOption.EUPORIE:
            interface_instance = EuporieConsole()
        
    open_multiplexer(
        mux_instance, 
        interface_instance, 
        project_dir, 
        connection_file,
        profile=profile
    )    


@app.command()
def exec(
    code: str = typer.Argument(..., help="code to execute."),
    project_dir: Path = typer.Option(".", help="Project directory")
):
    """Execute a code snippet in the running kernel."""
    connection_file = Path(project_dir) / "jup_kernel.json"
    # code = code_file.read_text()
    execute_code(code, connection_file)

if __name__ == "__main__":
    app()

