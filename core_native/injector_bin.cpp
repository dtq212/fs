#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <unistd.h>
int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <pid> <so_path>\n", argv[0]);
        return 1;
    }
    int pid = atoi(argv[1]);
    const char* so_path = argv[2];
    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) < 0) {
        perror("ptrace_attach");
        return 1;
    }
    waitpid(pid, NULL, 0);
    ptrace(PTRACE_DETACH, pid, NULL, NULL);
    printf("Hay su dung binary injector chuyen dung cho x86.\n");
    return 0;
}