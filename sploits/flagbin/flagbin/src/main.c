#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include "flagsdb/flagsdb.h"


void store_flag() {
    uint64_t flag_id = random();

    char flag_id_str[9];
    sprintf(flag_id_str, "%08llx", flag_id);


    char flag[4096];
    printf("Flag: ");
    fgets(flag, 4096, stdin);
    
    flagsdb_store(flag_id_str, flag, strlen(flag));

    printf("Flag id: %s\n", flag_id_str);
}


void retrieve_flag() {
    puts("Due to bandwith limitations we can only read 32 bytes at a time.");
    puts("Sorry for the inconvenience!");

    char flag_id_str[32];
    printf("Flag id: ");
    fgets(flag_id_str, 32, stdin);
    *strchr(flag_id_str, '\n') = 0;

    char offset_str[32];
    printf("Offset: ");
    fgets(offset_str, 32, stdin);

    uint64_t offset;
    sscanf(offset_str, "%llu", &offset);

    char flag[33];
    flag[32] = 0;

    int res = flagsdb_retrieve(flag_id_str, offset, 32, flag);
    if (res < 0) {
        puts("We encountered a problem while retrieving your flag");
        return;
    }

    printf(flag);
}

void list_available_flags() {
    char *flags = flagsdb_get_existing() + 5;
    for (int i = 0; flags[i]; i += 9)
        printf("%.3s*****\n", flags + i);
}

void init() {
    srandom(time(0));

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


int main() {
    init();
    puts(
        "8 8888888888   8 8888                  .8.           ,o888888o.    8 888888888o    8 8888 b.             8 \n" \
        "8 8888         8 8888                 .888.         8888     `88.  8 8888    `88.  8 8888 888o.          8 \n" \
        "8 8888         8 8888                :88888.     ,8 8888       `8. 8 8888     `88  8 8888 Y88888o.       8 \n" \
        "8 8888         8 8888               . `88888.    88 8888           8 8888     ,88  8 8888 .`Y888888o.    8 \n" \
        "8 888888888888 8 8888              .8. `88888.   88 8888           8 8888.   ,88'  8 8888 8o. `Y888888o. 8 \n" \
        "8 8888         8 8888             .8`8. `88888.  88 8888           8 8888888888    8 8888 8`Y8o. `Y88888o8 \n" \
        "8 8888         8 8888            .8' `8. `88888. 88 8888   8888888 8 8888    `88.  8 8888 8   `Y8o. `Y8888 \n" \
        "8 8888         8 8888           .8'   `8. `88888.`8 8888       .8' 8 8888      88  8 8888 8      `Y8o. `Y8 \n" \
        "8 8888         8 8888          .888888888. `88888.  8888     ,88'  8 8888    ,88'  8 8888 8         `Y8o.` \n" \
        "8 8888         8 888888888888 .8'       `8. `88888.  `8888888P'    8 888888888P    8 8888 8            `Yo \n" \
        " - Share your flags securely with our revolutionary flag sharing service!"
    );



    while (1) {
        puts("");
        puts("[1] Store flag");
        puts("[2] Retrieve flag");
        puts("[3] List available flags");
        puts("[4] Exit");
        printf("--> ");

        char choice[3];
        fgets(choice, 3, stdin);
        switch (choice[0]) {
            case '1':
                store_flag();
                break;
            case '2':
                retrieve_flag();
                break;
            case '3':
                list_available_flags();
                break;
            case '4':
                return 0;
            default:
                puts("Invalid input");
        }
    }
}
