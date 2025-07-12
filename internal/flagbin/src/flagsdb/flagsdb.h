#pragma once

#define FLAGSPATH "/tmp/flags"

#include <stdint.h>

void flagsdb_store(char *id, char *flag, unsigned size);
int flagsdb_retrieve(char *id, uint64_t offset, uint64_t size, char *buf);
char *flagsdb_get_existing();
