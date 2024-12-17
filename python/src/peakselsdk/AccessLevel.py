from enum import EnumType


class AccessLevel(EnumType):
    NONE = 0
    FIND = 2
    READ = 4
    CREATE = 64
    WRITE = 128
    ADMIN = 4096