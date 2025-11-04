import subprocess
import time
from pathlib import Path


class KernelManager:
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.connection_file = self.project_dir / "jup_kernel.json"
        self.process = None
        
    def start_kernel(self):
        """Start a Jupyter kernel in a uv-managed environment."""
        if self.connection_file.exists():
            self.connection_file.unlink()

        cmd = [
            "uv", "run", "jupyter", "kernel",
            f"--KernelManager.connection_file={self.connection_file}"
        ]

        self.process = subprocess.Popen(
            cmd,
            cwd=self.project_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Wait for connection file
        for _ in range(20):
            if self.connection_file.resolve().exists():
                return self.connection_file
            time.sleep(0.2)

        raise RuntimeError("Kernel did not start or connection file missing.")

    def stop_kernel(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=2)
