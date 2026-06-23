import os
import platform
import ctypes
import subprocess
import sys
import winreg


def is_admin():
    """Kiểm tra xem script có đang chạy bằng quyền Administrator hay không."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def get_core_isolation_status():
    """Kiểm tra tính năng Memory Integrity (Core Isolation) của Windows."""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "Enabled")
        winreg.CloseKey(key)
        return "Bật (Nguy cơ cao gây crash game khi dùng PyMem)" if value == 1 else "Tắt (An toàn)"
    except FileNotFoundError:
        return "Không tìm thấy registry (Có thể tính năng này không được hỗ trợ/đã tắt)"
    except Exception as e:
        return f"Không thể kiểm tra: {e}"


def get_antivirus_status():
    """Lấy danh sách các phần mềm Antivirus đang hoạt động qua WMI."""
    try:
        # Chạy lệnh PowerShell để truy vấn WMI SecurityCenter2
        cmd = 'powershell "Get-WmiObject -Namespace root\\SecurityCenter2 -Class AntiVirusProduct | Select-Object -ExpandProperty displayName"'
        result = subprocess.run(cmd, capture_output = True, text = True, shell = True)
        av_list = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return ", ".join(av_list) if av_list else "Không tìm thấy hoặc Windows Defender mặc định"
    except Exception as e:
        return f"Lỗi truy vấn AV: {e}"


def in_thong_so_he_thong():
    print("=" * 50)
    print("BÁO CÁO MÔI TRƯỜNG HỆ THỐNG MÁY KHÁCH")
    print("=" * 50)

    # 1. Thông tin Hệ điều hành
    print(f"[1] Hệ điều hành: {platform.system()} {platform.release()} (Phiên bản: {platform.version()})")
    print(f"[2] Kiến trúc HĐH: {platform.machine()}")

    # 2. Thông tin Python
    print(f"[3] Phiên bản Python: {platform.python_version()}")
    print(f"[4] Kiến trúc Python: {platform.architecture()[0]}")

    # 3. Thông tin Quyền hạn
    print(f"[5] Đang chạy quyền Admin: {'CÓ' if is_admin() else 'KHÔNG (Cần chạy file bằng Run as Administrator)'}")

    # 4. Bảo mật Windows
    print(f"[6] Trạng thái Core Isolation (Memory Integrity): {get_core_isolation_status()}")
    print(f"[7] Phần mềm Diệt Virus phát hiện được: {get_antivirus_status()}")

    print("=" * 50)
    print("Vui lòng copy toàn bộ kết quả này gửi lại cho Dev.")
    print("=" * 50)

    os.system("pause")


if __name__ == "__main__":
    in_thong_so_he_thong()