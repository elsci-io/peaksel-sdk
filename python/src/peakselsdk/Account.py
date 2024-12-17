from enum import EnumType


class AccountType(EnumType):
    """
    Both Users and Orgs are accounts.
    """
    PERSONAL = 0
    ORG = 8