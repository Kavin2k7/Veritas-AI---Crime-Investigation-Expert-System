"""
Compatibility wrapper for Forensic Opportunity & Alibi Filter.
Directs imports to backend.forensic_filter.
"""

from backend.forensic_filter import (
    ForensicConstraint as CSPConstraint,
    TimelineProximityConstraint as TimeWindowConstraint,
    PhysicalAccessFeasibilityConstraint as PhysicalAccessConstraint,
    EvidenceConsistencyConstraint,
    VerifiedAlibiConstraint,
    ForensicFilter as CSPSolver,
    ForensicFilter
)

__all__ = [
    "CSPConstraint",
    "TimeWindowConstraint",
    "PhysicalAccessConstraint",
    "EvidenceConsistencyConstraint",
    "VerifiedAlibiConstraint",
    "CSPSolver",
    "ForensicFilter"
]
