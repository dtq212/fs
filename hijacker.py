import ctypes
from ctypes import wintypes
import psutil
import traceback
import sys

SystemExtendedHandleInformation = 64
STATUS_INFO_LENGTH_MISMATCH = 0xC0000004
PROCESS_DUP_HANDLE = 0x0040
DUPLICATE_SAME_ACCESS = 0x00000002

PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_ALL_ACCESS = 0x1FFFFF

ntdll = ctypes.windll.ntdll
kernel32 = ctypes.windll.kernel32


# ÉP CỨNG KIỂU 64-BIT: Cứu cánh cho Python 32-bit chạy trên Win 64-bit
class SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX(ctypes.Structure):
    _fields_ = [
        ("Object", ctypes.c_uint64),
        ("UniqueProcessId", ctypes.c_uint64),
        ("HandleValue", ctypes.c_uint64),
        ("GrantedAccess", ctypes.c_ulong),
        ("CreatorBackTraceIndex", ctypes.c_ushort),
        ("ObjectTypeIndex", ctypes.c_ushort),
        ("HandleAttributes", ctypes.c_ulong),
        ("Reserved", ctypes.c_ulong),
    ]


def get_target_pids(process_names):
    pids = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in [n.lower() for n in process_names]:
                pids.append(proc.pid)
        except:
            pass
    return pids


def hijack_game_handle(target_game_pid, host_process_names = ["explorer.exe", "discord.exe", "steam.exe"]):
    print(f">>> [DEBUG] Bắt đầu gọi Hijack Handle cho Game PID [{target_game_pid}]...")
    try:
        host_pids = get_target_pids(host_process_names)
        if not host_pids:
            return None

        buffer_size = ctypes.c_ulong(0x10000)
        buffer = ctypes.create_string_buffer(buffer_size.value)
        return_length = ctypes.c_ulong(0)

        while ntdll.NtQuerySystemInformation(SystemExtendedHandleInformation, buffer, buffer_size, ctypes.byref(return_length)) == STATUS_INFO_LENGTH_MISMATCH:
            buffer_size.value = return_length.value + 1048576
            buffer = ctypes.create_string_buffer(buffer_size.value)

        # Trích xuất Header an toàn (Luôn chiếm 16 bytes đầu tiên)
        handle_count = int.from_bytes(buffer[:8], byteorder = sys.byteorder)
        offset = 16
        struct_size = ctypes.sizeof(SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX)

        # CHỐT CHẶN AN TOÀN: Tính toán số handle thực tế chứa vừa trong buffer
        max_safe_handles = (return_length.value - offset) // struct_size
        safe_count = min(handle_count, max_safe_handles)

        REQUIRED_ACCESS = PROCESS_VM_READ | PROCESS_VM_OPERATION
        print(f">>> [DEBUG] Bắt đầu duyệt AN TOÀN {safe_count} handles...")

        handles_array = ctypes.cast(
            ctypes.byref(buffer, offset),
            ctypes.POINTER(SYSTEM_HANDLE_TABLE_ENTRY_INFO_EX)
        )

        for i in range(safe_count):
            handle_info = handles_array[i]
            pid = int(handle_info.UniqueProcessId)  # Ép kiểu về số nguyên của Python

            if pid not in host_pids:
                continue

            has_all_access = (handle_info.GrantedAccess == PROCESS_ALL_ACCESS)
            has_required_access = ((handle_info.GrantedAccess & REQUIRED_ACCESS) == REQUIRED_ACCESS)

            if not (has_all_access or has_required_access):
                continue

            source_process_handle = kernel32.OpenProcess(PROCESS_DUP_HANDLE, False, pid)
            if not source_process_handle:
                continue

            target_handle = wintypes.HANDLE()

            success = kernel32.DuplicateHandle(
                source_process_handle,
                int(handle_info.HandleValue),
                kernel32.GetCurrentProcess(),
                ctypes.byref(target_handle),
                0,
                False,
                DUPLICATE_SAME_ACCESS
            )

            kernel32.CloseHandle(source_process_handle)

            if success:
                if kernel32.GetProcessId(target_handle) == target_game_pid:
                    print(f"[+] THÀNH CÔNG! Lấy được Handle [{target_handle.value}] từ vật chủ PID [{pid}]")
                    return target_handle.value
                else:
                    kernel32.CloseHandle(target_handle)

        print("[-] Duyệt xong nhưng không tìm thấy handle phù hợp.")
        return None

    except Exception as e:
        print(">>> [LỖI NGHIÊM TRỌNG]:")
        traceback.print_exc()
        return None