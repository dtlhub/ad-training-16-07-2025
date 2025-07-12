#include "flagsdb.h"

#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/mman.h>
#include <dirent.h>
#include <stdlib.h>

static char* existing_flags = 0;


char *flagsdb_get_existing() {
    if (!existing_flags)
        existing_flags = mmap(0, 4096 * 4294967296, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE | MAP_NORESERVE, -1, 0);

    struct dirent **namelist;
    int n;
    n = scandir(FLAGSPATH, &namelist, NULL, alphasort);
    
    int j = 0;
    for (int i = 0; i < n; i++) {
        strcpy(existing_flags + j, namelist[i]->d_name);
        j += strlen(namelist[i]->d_name);
        existing_flags[j++] = '\n';
        free(namelist[i]);
    }
    free(namelist);
    existing_flags[j] = 0;

    return existing_flags;
}

void flagsdb_store(char *id, char *flag, unsigned int size) {
    char path[32];
    sprintf(path, FLAGSPATH"/%s", id);
    
    int fd = open(path, O_WRONLY | O_CREAT, 0644);
    write(fd, flag, strlen(flag));
    close(fd);
}


int flagsdb_retrieve(char *id, uint64_t offset, uint64_t size, char *buf) {
    char path[32];
    sprintf(path, FLAGSPATH"/%s", id);
    int fd = open(path, O_RDONLY); 

    if (fd < 0)
        return -1;

    lseek(fd, offset, SEEK_SET);
    read(fd, buf, size);
    close(fd);

    return 0;
}

