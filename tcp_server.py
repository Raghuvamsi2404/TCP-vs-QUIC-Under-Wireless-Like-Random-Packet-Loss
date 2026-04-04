import socket
import os

HOST = "127.0.0.1"
PORT = 5201
TESTFILE = "testfile.bin"

def main():
    with open(TESTFILE, "rb") as f:
        file_data = f.read()
    file_size_mb = len(file_data) / (1024 * 1024)
    print(f"TCP server listening on port {PORT}...")
    print(f"Loaded {TESTFILE} ({file_size_mb:.3f} MB) into memory")
    print("Waiting for connections... (Ctrl+C to stop)\n")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((HOST, PORT))

    server_sock.listen(5)

    trial_count = 0

    while True:
        conn, addr = server_sock.accept()
        trial_count += 1
        print(f"[Trial {trial_count}] Connection from {addr} — sending {file_size_mb:.3f} MB...")

        try:
            conn.sendall(file_data)
        except Exception as e:
            print(f"  ERROR during send: {e}")
        finally:
            conn.close()
            print(f"[Trial {trial_count}] Transfer complete.\n")

if __name__ == "__main__":
    main()