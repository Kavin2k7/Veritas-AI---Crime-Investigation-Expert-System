"""
Compatibility wrapper for Investigative Hypothesis & Legal Proof.
Directs imports to backend.hypothesis_engine.
"""

from backend.hypothesis_engine import (
    HypothesisEngine as InferenceEngine,
    HypothesisEngine
)

__all__ = [
    "InferenceEngine",
    "HypothesisEngine"
]
