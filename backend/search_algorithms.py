"""
Compatibility wrapper for Relationship & Network Link Analysis.
Directs imports to backend.network_link_analyzer.
"""

from backend.network_link_analyzer import (
    NetworkLinkAnalyzer as InvestigationGraph,
    NetworkLinkAnalyzer
)

__all__ = [
    "InvestigationGraph",
    "NetworkLinkAnalyzer"
]
