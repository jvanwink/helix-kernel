from jupyter_client import BlockingKernelClient
from pathlib import Path


def execute_code(code: str, connection_file: Path):
    kc = BlockingKernelClient()
    kc.load_connection_file(connection_file)
    kc.start_channels()
    kc.execute(code)
    while True:
        msg = kc.get_iopub_msg(timeout=1.0)
        msg_type = msg["header"]["msg_type"]
        if msg_type == "stream":
            print(msg["content"]["text"], end="")
        elif msg_type == "execute_result":
            print(msg["content"]["data"].get("text/plain", ""))
        elif msg_type == "error":
            print("\n".join(msg["content"]["traceback"]))
        elif msg_type == "status" and msg["content"]["execution_state"] == "idle":
            break

    kc.stop_channels()

