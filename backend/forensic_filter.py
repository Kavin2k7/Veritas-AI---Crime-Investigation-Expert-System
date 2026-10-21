"""
Forensic Opportunity & Alibi Filter Module for Criminal Investigation System.
Evaluates suspects against crime timeline, physical scene access,
contradiction with physical evidence, and verified alibis.
"""

from typing import Dict, List, Any, Tuple, Optional

class ForensicConstraint:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def is_satisfied(self, suspect: Dict[str, Any]) -> Tuple[bool, str]:
        """Returns True if suspect satisfies the investigative constraint, else False with reason."""
        raise NotImplementedError

class TimelineProximityConstraint(ForensicConstraint):
    def __init__(self):
        super().__init__("Timeline Proximity", "Must be present or unaccounted near crime scene during timeframe (21:30–23:15)")

    def is_satisfied(self, suspect: Dict[str, Any]) -> Tuple[bool, str]:
        if suspect.get('time_window_passed'):
            return True, "Presence near scene or unaccounted time window verified."
        return False, "Failed: Suspect was nowhere near the vicinity during crime time window."

class PhysicalAccessFeasibilityConstraint(ForensicConstraint):
    def __init__(self):
        super().__init__("Physical Access Feasibility", "Must have viable access route into the property")

    def is_satisfied(self, suspect: Dict[str, Any]) -> Tuple[bool, str]:
        if suspect.get('physical_access_passed'):
            return True, "Physical access route to crime location confirmed."
        return False, "Failed: No physical access route or key/code available to suspect."

class EvidenceConsistencyConstraint(ForensicConstraint):
    def __init__(self):
        super().__init__("Evidence Consistency", "Must not contradict established physical evidence")

    def is_satisfied(self, suspect: Dict[str, Any]) -> Tuple[bool, str]:
        if not suspect.get('contradicts_evidence'):
            return True, "No contradiction found with physical evidence."
        return False, "Failed: Statements directly contradict physical forensic evidence."

class VerifiedAlibiConstraint(ForensicConstraint):
    def __init__(self):
        super().__init__("Verified Alibi Exemption", "Solid verified alibi eliminates suspect if no fingerprint/DNA evidence exists")

    def is_satisfied(self, suspect: Dict[str, Any]) -> Tuple[bool, str]:
        if suspect.get('alibi_verified') and not suspect.get('evidence_matched'):
            return False, "Eliminated: Verified solid alibi with zero physical evidence match."
        return True, "Alibi inconsistent, unverified, or overridden by physical evidence match."

class ForensicFilter:
    def __init__(self):
        self.constraints: List[ForensicConstraint] = [
            TimelineProximityConstraint(),
            PhysicalAccessFeasibilityConstraint(),
            EvidenceConsistencyConstraint(),
            VerifiedAlibiConstraint()
        ]

    def filter_suspects(self, suspects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates suspects against multi-factor forensic constraints and filters out invalid candidates.
        """
        retained_suspects = []
        eliminated_suspects = []
        detailed_evaluations = []

        for suspect in suspects:
            name = suspect['name']
            suspect_eval = {
                "id": suspect['id'],
                "name": name,
                "initials": suspect['initials'],
                "role": suspect['role'],
                "constraint_results": [],
                "final_status": "RETAINED"
            }

            passed_all = True
            failure_reasons = []

            for constraint in self.constraints:
                passed, reason = constraint.is_satisfied(suspect)
                suspect_eval["constraint_results"].append({
                    "constraint_name": constraint.name,
                    "passed": passed,
                    "reason": reason
                })

                if not passed:
                    passed_all = False
                    failure_reasons.append(f"{constraint.name}: {reason}")
                    break

            if passed_all:
                suspect_eval["final_status"] = "RETAINED"
                retained_suspects.append(suspect)
            else:
                suspect_eval["final_status"] = "ELIMINATED"
                suspect_eval["elimination_reason"] = "; ".join(failure_reasons)
                eliminated_suspects.append(suspect)

            detailed_evaluations.append(suspect_eval)

        total_checks = sum(len(e["constraint_results"]) for e in detailed_evaluations)

        return {
            "total_evaluated": len(suspects),
            "retained_count": len(retained_suspects),
            "eliminated_count": len(eliminated_suspects),
            "total_constraint_checks": total_checks,
            "retained_suspects": retained_suspects,
            "eliminated_suspects": eliminated_suspects,
            "evaluations": detailed_evaluations,
            "summary": f"Forensic Opportunity Filter evaluated {len(suspects)} suspects across timeline and alibi constraints: {len(retained_suspects)} retained for prosecution, {len(eliminated_suspects)} eliminated."
        }

    # Backward compatibility alias
    solve_backtracking = filter_suspects

# Aliases for backward compatibility
CSPConstraint = ForensicConstraint
TimeWindowConstraint = TimelineProximityConstraint
PhysicalAccessConstraint = PhysicalAccessFeasibilityConstraint
CSPSolver = ForensicFilter
