import sys
from enum import Enum, auto, StrEnum
import subprocess
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


#TODO: lazygit --> Can be directly in helix
#TODO: remove all breakpoints
#TODO: Comment out all breakpoint
#TODO: Helix key to set a breakpoint

@app.command()
def run(
    python_file: Path = typer.Option("main.py", help="The python file to run"),
    project_dir: Path = typer.Option(".", help="Project directory")
):
    #TODO: This should open a pane in the multiplexer
    subprocess.Popen(["uv", "run", python_file], cwd=project_dir)    

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
    code: str = typer.Argument(None , help="code to execute (if not piped)."),
    project_dir: Path = typer.Option(".", help="Project directory")
):
    """Execute a code snippet in the running kernel."""
    connection_file = Path(project_dir) / "jup_kernel.json"

    if code is None or code == "-":
        code = sys.stdin.read().strip()
    # code = code_file.read_text()
    execute_code(code, connection_file)

if __name__ == "__main__":
    app()

