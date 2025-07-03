#include <stdio.h>
#include <string.h>
#include <sys/random.h>
#include <stdlib.h>
#include <sys/signal.h>
#include <unistd.h>


typedef struct {
    int hp;
    int shd;
    int atk;
} BattleBot;

BattleBot battlebots[5];


long long read_int() {
    char buf[16];
    fgets(buf, 16, stdin);

    long long res;
    sscanf(buf, "%lld", &res);

    return res;
}


void view_battlebot(int id) {
    if (id >= 5) {
        puts("The free version of the battlebot simulator only allows for 5 battlebots. Buy the advanced battles dlc to increase the limit.");
        return;
    }

    BattleBot bot = battlebots[id];

    printf("Battlebot %d:\nHP: %d\nSHD: %d\nATK: %d\n", id, bot.hp, bot.shd, bot.atk);
}

void edit_battlebot(int id) {
    if (id >= 5) {
        puts("The free version of the battlebot simulator only allows for 5 battlebots. Buy the advanced battles dlc to increase the limit.");
        return;
    }
    printf("Editing battlebot %d\n", id);


    BattleBot *pbot = battlebots + id;
    printf("HP > ");
    pbot->hp = read_int();
    printf("SHD > ");
    pbot->shd = read_int();
    printf("ATK > ");
    pbot->atk = read_int();
}

void battle() {
    puts("Let the battle begin!");
    int alive = 0b11111;
    for (int i = 0; i < 5; ++i) {
        if (!(alive & (0b1 << i)))
            continue;
        for (int j = 0; j < 5; ++j) {
            if (i == j)
                continue;
            if (!(alive & (0b1 << j)))
                continue;

            if ((battlebots[i].hp + battlebots[i].shd) * battlebots[i].atk > (battlebots[j].hp + battlebots[j].shd) * battlebots[j].atk) {
                alive &= ~(0b1 << j);
                printf("Battlebot %d is cooked!\n", j);
            } else {
                alive &= ~(0b1 << i);
                printf("Battlebot %d is cooked!\n", i);
                break;
            }
        }
    }
}

void leave_feedback() {
    char buf[16];
    do {
        printf("Do you have a chat id? [y/n] > ");
        fgets(buf, 16, stdin);
    } while (buf[0] != 'y' && buf[0] != 'n');


    char path[64];
    char feedback[2048];

    if (buf[0] == 'n') {
        long long chat_id = random();
        sprintf(path, "/tmp/chats/%llx.txt", chat_id);

        printf("Enter your feedback > ");
        fgets(feedback, 512, stdin);
        strcat(feedback, "\n Thank you for your feedback! Our team is really busy right now but we will try to review your feedback as soon as we can!");

        FILE *pfchat = fopen(path, "w");
        fprintf(pfchat, "%s", feedback);
        fclose(pfchat);

        printf("Your feedback was saved! You can chat with our developers using this chad id: %lld\n", chat_id);
    } else {
        printf("Chat id > ");
        long long chat_id = read_int();
        sprintf(path, "/tmp/chats/%llx.txt", chat_id);

        if (access(path, F_OK) != 0) {
            printf("We couldnt find a chat with id %lld\n", chat_id);
            return;
        }

        puts("Chat history:");
        FILE *pfchat = fopen(path, "r");
        while (fgets(feedback, 512, pfchat))
            printf("%s", feedback);
        fclose(pfchat);

        printf("Enter your message > ");
        fgets(feedback, 512, stdin);
        pfchat = fopen(path, "a");
        fprintf(pfchat, "%s", feedback);
        fclose(pfchat);
    }
}


void alarm_handler(int sig) {
    puts("You can wage battles only for 30 seconds! Buy the advanced battles dlc to increase the limit.");
    exit(0);
}


void init() {
    unsigned seed;
    getrandom(&seed, sizeof(seed), 0);
    srandom(seed);

    signal(SIGALRM, alarm_handler);
    alarm(30);

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int menu() {
    puts("\n");
    printf("| [1] View battlebot\n"
         "| [2] Edit battlebot\n"
         "| [3] Battle\n"
         "| [4] Leave feedback\n"
         "| [5] Exit\n"
         "\\\n"
         "  --> "
    );

    long long choice = read_int();
    int inp;
    switch (choice) {
        case 1:
            printf("Battlebot ID > ");
            inp = read_int();
            inp >= 0 ? view_battlebot(inp) : puts("?");
            break;
        case 2:
            printf("Battlebot ID > ");
            inp = read_int();
            inp >= 0 ? edit_battlebot(inp) : puts("?");
            break;
        case 3:
            battle();
            break;
        case 4:
            leave_feedback();
            break;
        case 5:
            return 1;
        default:
            puts("?");
    }

    return 0;
}

int main() {
    puts("   █████                █████     █████    ████           █████               █████           \n"
         "  ░░███                ░░███     ░░███    ░░███          ░░███               ░░███            \n"
         "   ░███████   ██████   ███████   ███████   ░███   ██████  ░███████   ██████  ███████    █████ \n"
         "   ░███░░███ ░░░░░███ ░░░███░   ░░░███░    ░███  ███░░███ ░███░░███ ███░░███░░░███░    ███░░  \n"
         "   ░███ ░███  ███████   ░███      ░███     ░███ ░███████  ░███ ░███░███ ░███  ░███    ░░█████ \n"
         "   ░███ ░███ ███░░███   ░███ ███  ░███ ███ ░███ ░███░░░   ░███ ░███░███ ░███  ░███ ███ ░░░░███\n"
         "   ████████ ░░████████  ░░█████   ░░█████  █████░░██████  ████████ ░░██████   ░░█████  ██████ \n"
         "  ░░░░░░░░   ░░░░░░░░    ░░░░░     ░░░░░  ░░░░░  ░░░░░░  ░░░░░░░░   ░░░░░░     ░░░░░  ░░░░░░  \n"
         "                                                                                              \n"
    );
    while (!menu());
    return 0;
}

