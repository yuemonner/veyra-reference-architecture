"""Veyra reference engine.

The package intentionally keeps the first implementation dependency-light so
the architecture can be reviewed, tested and ported before product hardening.
"""

from .models import DecisionEvidencePack, ReviewRequest
from .reconstruction import build_decision_pack

__all__ = ["DecisionEvidencePack", "ReviewRequest", "build_decision_pack"]

