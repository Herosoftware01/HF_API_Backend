import socket
import time
import threading
from datetime import datetime

SCALE_IP = "192.168.1.101"
SCALE_PORT = 8080

RECONNECT_DELAY = 3
NO_DATA_TIMEOUT = 30

latest_reading = {
    "raw": None,
    "received_at": None,
    "connected": False,
}

reading_lock = threading.Lock()


def get_latest_reading():
    with reading_lock:
        return latest_reading.copy()


def read_scale():
    buffer = ""
    last_data_time = time.monotonic()

    with socket.create_connection(
        (SCALE_IP, SCALE_PORT), timeout=5
    ) as sock:
        sock.settimeout(2)

        with reading_lock:
            latest_reading["connected"] = True

        print(f"Connected to scale {SCALE_IP}:{SCALE_PORT}")

        while True:
            try:
                data = sock.recv(1024)

                if not data:
                    return

                last_data_time = time.monotonic()
                buffer += data.decode("ascii", errors="ignore")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    if line:
                        with reading_lock:
                            latest_reading["raw"] = line
                            latest_reading["received_at"] = (
                                datetime.now().astimezone().isoformat()
                            )

                        print("Received:", repr(line))

            except socket.timeout:
                if time.monotonic() - last_data_time >= NO_DATA_TIMEOUT:
                    return


def reader_loop():
    while True:
        try:
            read_scale()

        except OSError as error:
            print("Scale connection error:", error)

        finally:
            with reading_lock:
                latest_reading["connected"] = False

        time.sleep(RECONNECT_DELAY)


def start_reader():
    thread = threading.Thread(
        target=reader_loop,
        daemon=True,
        name="scale-reader",
    )
    thread.start()
    return thread
