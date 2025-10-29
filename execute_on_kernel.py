import sys
import os
import json
from jupyter_client import BlockingKernelClient


def send_code_to_kernel(code, connection_file):

    kc = BlockingKernelClient()
    kc.load_connection_file(connection_file)
    kc.start_channels()
    print(type(code))
    print(code)
    kc.execute(code)
    # we can also start a session, then we can add some parameters
    while True:
        msg = kc.get_iopub_msg(timeout=1.0)
        msg_type = msg["header"]["msg_type"]

        if msg_type == "execute_input":
            print(f"In [{msg['content']['execution_count']}]: {msg['content']['code']}")
        elif msg_type in ["execute_result", "display_data"]:
            print(msg["content"]["data"].get("text/plain", ""))
        elif msg_type == "stream":
            print(msg["content"]["text"], end="")
        elif msg_type == "error":
            print("\n".join(msg["content"]["traceback"]))
        elif msg_type == "status" and msg["content"]["execution_state"] == "idle":
            break
    kc.stop_channels()


if __name__ == "__main__":
    code = sys.stdin.read()
    connection_file = os.path.join(os.getcwd(), "jup_kernel.json")
    send_code_to_kernel(code, connection_file)
