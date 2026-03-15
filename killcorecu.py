import socket

def kill_core_cu():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1.0)
        client.connect(("127.0.0.1", 5000))
        client.sendall(b"exit")
        client.close()
        print("[+] Đã tiêu diệt Core cũ, cổng 5000 đã mở!")
    except:
        print("[-] Không có Core nào đang chạy.")

if __name__ == "__main__":
    kill_core_cu()