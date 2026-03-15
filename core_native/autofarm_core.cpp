#include <jni.h>
#include <android/log.h>
#include <pthread.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>

#define LOG_TAG "AutoFarm_Native"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define PORT 5000

uintptr_t cocosBase = 0;
void* fakeThis = nullptr;

typedef int (*UseSkillFunc)(void* instance, int x, int y, int skillId, int flag);

uintptr_t find_library_base(const char* library_name) {
    uintptr_t address = 0;
    char line[512];
    FILE* fp = fopen("/proc/self/maps", "r");
    if (fp) {
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, library_name)) {
                address = (uintptr_t)strtoul(line, NULL, 16);
                break;
            }
        }
        fclose(fp);
    }
    return address;
}
void CallSkill(int id, int x, int y) {
    if (cocosBase == 0) {
        LOGI("[-] Loi: Chua tim thay Base Address libcocos2dcpp.so");
        return;
    }
    if (fakeThis == nullptr) {
        fakeThis = malloc(0x100);
    }
    UseSkillFunc useSkill = (UseSkillFunc)(cocosBase + 0x732240);
    int result = useSkill(fakeThis, x, y, id, -1);

    LOGI("[+] BÙM! Da goi ky nang ID=%d, tai X=%d, Y=%d (Return: %d)", id, x, y, result);
}

typedef void (*SendRepairFunc)(unsigned int dbid);
void AutoRepairItem(int idvatpham) {
    if (cocosBase == 0) return;
    uintptr_t basePtr = *(uintptr_t*)(cocosBase + 0xFC3A68);
    if (basePtr == 0) {
        LOGI("[-] Loi: Con tro mang vat pham rong (0xFC3A68 == 0)");
        return;
    }
    uintptr_t itemAddr = basePtr + (idvatpham * 0x76C);
    char* itemName = (char*)(itemAddr + 0x48);
    int currentDurability = *(int*)(itemAddr + 0x5FC);
    if (currentDurability == -1) {
        LOGI("[-] [Slot %d] '%s' khong the hong.", idvatpham, itemName);
        return;
    }
    int maxDurability = -1;
    for (int i = 0; i <= 6; i++) {
        int magicNumber = *(int*)(itemAddr + 0x420 + (i * 0x14));
        if (magicNumber == 0x1F) {
            maxDurability = *(int*)(itemAddr + 0x424 + (i * 0x14));
            break;
        }
    }
    unsigned int dbid = *(unsigned int*)(itemAddr + 0x5F8);
    if (maxDurability != -1 && currentDurability < maxDurability) {
        LOGI("[!] [Slot %d] Dang sua '%s' | DBID=%u | Do ben: %d/%d", idvatpham, itemName, dbid, currentDurability, maxDurability);
        SendRepairFunc sendRepair = (SendRepairFunc)(cocosBase + 0x0077b2d0);
        sendRepair(dbid);

    } else {
        LOGI("[+] [Slot %d] '%s' con tot (%d/%d), chua can sua.", idvatpham, itemName, currentDurability, maxDurability);
    }
}

struct UseItemPos {
    int vitriruong;
    int vitrix;
    int vitriy;
};

typedef void (*UseItemFunc)(void* instance, int idvatpham, UseItemPos pos);

static void* fakePlayer = nullptr;

void AutoUseItem(int idvatpham, int vitriruong, int vitrix, int vitriy) {
    if (cocosBase == 0) return;

    if (fakePlayer == nullptr) {
        fakePlayer = malloc(0x4000);
        memset(fakePlayer, 0, 0x4000);
        *(int*)((uintptr_t)fakePlayer + 0x24) = 100;

        *(int*)((uintptr_t)fakePlayer + 0x68) = 1;

        *(int*)((uintptr_t)fakePlayer + 0x3D3C) = 0;
    }
    UseItemPos pos = {vitriruong, vitrix, vitriy};
    UseItemFunc useItem = (UseItemFunc)(cocosBase + 0x769374);
    LOGI("[!] DANG DUNG ITEM: Slot=%d | Ruong=%d | X=%d, Y=%d", idvatpham, vitriruong, vitrix, vitriy);
    useItem(fakePlayer, idvatpham, pos);

    LOGI("[+] Goi ham UseItem thanh cong bang fakePlayer!");
}

void* SocketServerThread(void* arg) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) return nullptr;

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) return nullptr;
    if (listen(server_fd, 3) < 0) return nullptr;

    LOGI("[+] Socket Server dang lang nghe tren cong %d", PORT);

    while (true) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) continue;

        int valread = read(new_socket, buffer, 1024);
        if (valread > 0) {
            char action[32] = {0};
            int p1 = 0, p2 = 0, p3 = 0, p4 = 0;

            int parsed = sscanf(buffer, "%31[^,],%d,%d,%d,%d", action, &p1, &p2, &p3, &p4);

            if (parsed >= 1) {
                if (strcmp(action, "skill") == 0 && parsed >= 4) {
                    CallSkill(p1, p2, p3);
                    send(new_socket, "OK", 2, 0);
                }
                else if (strcmp(action, "repair") == 0 && parsed >= 2) {
                    AutoRepairItem(p1);
                    send(new_socket, "OK", 2, 0);
                }
                else if (strcmp(action, "getname") == 0 && parsed >= 2) {
                    if (cocosBase != 0) {
                        uintptr_t basePtr = *(uintptr_t*)(cocosBase + 0xFC3A68);
                        if (basePtr != 0) {
                            uintptr_t itemAddr = basePtr + (p1 * 0x76C);
                            char* itemName = (char*)(itemAddr + 0x48);
                            if (strlen(itemName) > 0) send(new_socket, itemName, strlen(itemName), 0);
                            else send(new_socket, "EMPTY", 5, 0);
                        } else send(new_socket, "EMPTY", 5, 0);
                    } else send(new_socket, "EMPTY", 5, 0);
                }
                else if (strcmp(action, "getpos") == 0 && parsed >= 2) {
                    if (cocosBase != 0) {
                        uintptr_t ptr1 = *(uintptr_t*)(cocosBase + 0x11EEA78);
                        if (ptr1 != 0) {
                            uintptr_t posAddr = ptr1 + 0x5AD4 + (p1 * 0x10);
                            int idvatpham = *(int*)(posAddr);
                            int vitriruong = *(int*)(posAddr + 4);
                            int vitrix = *(int*)(posAddr + 8);
                            int vitriy = *(int*)(posAddr + 12);

                            char resp[128];
                            sprintf(resp, "%d,%d,%d,%d", idvatpham, vitriruong, vitrix, vitriy);
                            send(new_socket, resp, strlen(resp), 0);
                        } else send(new_socket, "0,0,0,0", 7, 0);
                    } else send(new_socket, "0,0,0,0", 7, 0);
                }
                else if (strcmp(action, "useitem") == 0 && parsed >= 5) {
                    AutoUseItem(p1, p2, p3, p4);
                    send(new_socket, "OK", 2, 0);
                }
                else if (strcmp(action, "exit") == 0) {
                    LOGI("[!] DA NHAN LENH TU HUY. GIAI PHONG CONG 5000!");
                    send(new_socket, "OK", 2, 0);
                    close(new_socket);
                    close(server_fd);
                    return nullptr;
                }
                else {
                    LOGI("[-] Lenh khong hop le: %s", buffer);
                    send(new_socket, "ERR", 3, 0);
                }
            }
        }
        close(new_socket);
        memset(buffer, 0, sizeof(buffer));
    }
    return nullptr;
}

void* MainLogicThread(void* arg) {
    cocosBase = find_library_base("libcocos2dcpp.so");
    if (cocosBase != 0) {
        LOGI("[+] Found libcocos2dcpp.so Base Address at: 0x%lx", cocosBase);
    }
    return nullptr;
}

JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved) {
    pthread_t thread1, thread2;
    pthread_create(&thread1, nullptr, MainLogicThread, nullptr);
    pthread_create(&thread2, nullptr, SocketServerThread, nullptr);
    return JNI_VERSION_1_6;
}