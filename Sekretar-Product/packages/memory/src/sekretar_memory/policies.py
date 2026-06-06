"""Memory domain policy placeholders.

Policies will protect Memory invariants in the implementation phase. They are
declared here as architectural placeholders only.
"""


class AccountOwnershipPolicy:
    """Ensures Memory belongs to Account."""


class ProvenanceRequiredPolicy:
    """Ensures stable knowledge has provenance."""


class ModelDoesNotOwnMemoryPolicy:
    """Ensures model output cannot become a Memory owner."""


class RawSourceDumpPreventionPolicy:
    """Prevents raw source content from becoming Memory directly."""


class LifecycleTransitionPolicy:
    """Ensures knowledge lifecycle transitions are allowed."""


class ContextLifecyclePolicy:
    """Ensures context respects confidence and lifecycle."""


class ContradictionPolicy:
    """Ensures contradictions are explicit and not silent overwrites."""


class ForgettingPolicy:
    """Ensures deleted or forgotten knowledge is not reused as active context."""
