import os
import sys
import io
import time
import socket
import threading
import webbrowser

def get_base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def wait_for_server(host, port, timeout=15):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

def open_browser_when_ready():
    if wait_for_server("127.0.0.1", 8000):
        webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    base_dir = get_base_dir()
    os.chdir(base_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iOS.settings")

    import django
    from django.core.management import call_command

    django.setup()

    call_command(
        "migrate",
        interactive=False,
        stdout=io.StringIO(),
        stderr=io.StringIO(),
    )

    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    call_command(
        "runserver",
        "127.0.0.1:8000",
        use_reloader=False,
        stdout=io.StringIO(),
        stderr=io.StringIO(),
    )