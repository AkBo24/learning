from enum import Enum

class PermissionDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    MODIFIED = "modified"  # allow but with updatedInput