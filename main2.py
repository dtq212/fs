import subprocess
import ctypes


def is_admin():
    """
    Hàm này kiểm tra xem chương trình có đang được chạy
    dưới quyền Quản trị viên (Administrator) hay không.
    """
    try:
        # Gọi API của Windows để kiểm tra quyền
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        # Nếu có lỗi trong quá trình kiểm tra, mặc định là không có quyền
        return False


def reboot_to_bios():
    """
    Hàm này thực thi lệnh hệ thống để khởi động lại máy tính
    và truy cập thẳng vào giao diện BIOS/UEFI.
    """
    print("Đang chuẩn bị khởi động lại máy tính vào BIOS/UEFI...")
    print("⚠️ Vui lòng lưu lại toàn bộ công việc đang làm!")

    # Lệnh Windows để khởi động lại vào firmware
    command = "shutdown /r /fw /t 0"

    try:
        subprocess.run(command, shell = True, check = True)
        print("✅ Lệnh đã được gửi đi. Máy tính sẽ khởi động lại ngay bây giờ.")
    except subprocess.CalledProcessError:
        print("❌ Lỗi: Bo mạch chủ hoặc hệ thống hiện tại không hỗ trợ gọi BIOS/UEFI trực tiếp từ Windows bằng lệnh này.")
    except Exception as e:
        print(f"Đã xảy ra lỗi không xác định: {e}")


# Điểm bắt đầu của chương trình
if __name__ == "__main__":
    print("Đang kiểm tra quyền truy cập hệ thống...")

    # Kiểm tra quyền Admin trước khi làm bất cứ điều gì
    if is_admin():
        print("✅ Chương trình đã được cấp quyền Administrator.")
        confirm = input("Bạn đã lưu công việc và sẵn sàng khởi động lại vào BIOS chưa? (y/n): ")

        if confirm.lower() == 'y':
            reboot_to_bios()
        else:
            print("Đã hủy thao tác khởi động lại.")
    else:
        print("❌ LỖI: Cần có quyền Administrator để thực hiện tác vụ này.")
        print("👉 Hướng dẫn: Hãy đóng cửa sổ này, mở lại Command Prompt (cmd) bằng cách nhấp chuột phải và chọn 'Run as Administrator', sau đó chạy lại mã.")