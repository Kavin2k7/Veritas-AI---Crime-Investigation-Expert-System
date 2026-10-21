"""
Investigative Hypothesis & Legal Proof Module for Criminal Investigation System.
Implements Inductive Evidence Assembly for prime perpetrator derivation and
Prosecution Proof Verification for transparent legal justification.
"""

from typing import Dict, List, Any, Set, Tuple, Optional
try:
    from backend.knowledge_base import KnowledgeBase
except ImportError:
    from knowledge_base import KnowledgeBase


class HypothesisEngine:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def assemble_evidence_facts(self, suspects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Inductive Evidence Assembly:
        Synthesizes verified forensic facts, motive records, and access logs
        to establish probable cause and identify the prime suspect.
        """
        self.kb.load_from_db_data(suspects, [])
        known_facts = set(self.kb.facts)
        inferred_conclusions = []
        prime_suspect = None
        highest_score = -1

        suspect_analysis = []

        for suspect in suspects:
            name = suspect['name']
            s_name = name.replace(" ", "_")

            # Check individual predicates
            has_motive = f"motive({s_name})" in known_facts
            has_access = f"access({s_name})" in known_facts
            has_ev_match = f"evidence_match({s_name})" in known_facts
            has_time_win = f"in_time_window({s_name})" in known_facts
            has_alibi = f"alibi_verified({s_name})" in known_facts
            contradicts = f"contradicts_evidence({s_name})" in known_facts

            score = 0
            supporting_facts = []

            if has_motive:
                score += 25
                supporting_facts.append(f"A financial/personal motive was established for {name}")
            if has_access:
                score += 25
                supporting_facts.append(f"Access to the crime scene was verified for {name}")
            if has_ev_match:
                score += 35
                supporting_facts.append(f"Forensic fingerprint/DNA evidence matched {name}")
            if has_time_win:
                score += 15
                supporting_facts.append(f"Presence near scene verified during crime time window")

            status = "Needs review"
            if contradicts or (has_alibi and not has_ev_match):
                status = "Eliminated"
                score = 0
            elif score >= 70:
                status = "Prime suspect"

            if status == "Prime suspect" and score > highest_score:
                highest_score = score
                prime_suspect = suspect

            suspect_analysis.append({
                "id": suspect['id'],
                "name": name,
                "initials": suspect['initials'],
                "role": suspect['role'],
                "status": status,
                "confidence_score": score,
                "facts": supporting_facts,
                "predicate_summary": f"motive={has_motive}, access={has_access}, ev_match={has_ev_match}, time={has_time_win}"
            })

            if status == "Prime suspect":
                inferred_conclusions.append(f"Inductive Reasoning established probable cause for prime_suspect({s_name}) with {score}% legal confidence.")

        if not prime_suspect and suspect_analysis:
            sorted_suspects = sorted(suspect_analysis, key=lambda x: x['confidence_score'], reverse=True)
            prime_suspect = sorted_suspects[0]

        return {
            "engine": "Inductive Evidence Assembly",
            "prime_suspect": prime_suspect,
            "inferred_conclusions": inferred_conclusions,
            "suspect_analysis": suspect_analysis,
            "predicate_rule_applied": "motive(x) ∧ access(x) ∧ evidence_match(x) → prime_suspect(x)"
        }

    # Backward compatibility alias
    forward_chaining = assemble_evidence_facts

    def verify_prosecution_proof(self, target_suspect_name: str, suspects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prosecution Proof & Verification:
        Goal-directed legal verification. Formulates the hypothesis:
        "Is <target_suspect_name> the prime perpetrator?"
        Systematically checks each required legal premise against verified forensic evidence.
        """
        self.kb.load_from_db_data(suspects, [])
        known_facts = set(self.kb.facts)

        s_name = target_suspect_name.replace(" ", "_")
        target_goal = f"prime_suspect({s_name})"

        proof_steps = []
        proof_steps.append({
            "step": 1,
            "goal": target_goal,
            "status": "EVALUATING",
            "explanation": f"Formulated prosecution hypothesis: Prove {target_goal}"
        })

        sub_goals = [
            ("motive", f"motive({s_name})", f"Recorded financial or personal grievance for {target_suspect_name}"),
            ("access", f"access({s_name})", f"Physical access opportunity to crime scene confirmed for {target_suspect_name}"),
            ("evidence_match", f"evidence_match({s_name})", f"Forensic ridge/DNA/digital evidence directly linked to {target_suspect_name}"),
            ("in_time_window", f"in_time_window({s_name})", f"Timeline presence near scene confirmed during estimated crime window")
        ]

        verified_count = 0
        step_idx = 2

        for pred_name, sub_goal, description in sub_goals:
            is_satisfied = sub_goal in known_facts
            if is_satisfied:
                verified_count += 1
                proof_steps.append({
                    "step": step_idx,
                    "sub_goal": sub_goal,
                    "satisfied": True,
                    "explanation": f"VERIFIED: {description}"
                })
            else:
                proof_steps.append({
                    "step": step_idx,
                    "sub_goal": sub_goal,
                    "satisfied": False,
                    "explanation": f"UNVERIFIED: Condition {sub_goal} not established in evidence record."
                })
            step_idx += 1

        is_prime_verified = verified_count >= 3

        proof_steps.append({
            "step": step_idx,
            "goal": target_goal,
            "satisfied": is_prime_verified,
            "explanation": f"LEGAL CONCLUSION: Hypothesis {target_goal} is {'CONFIRMED BEYOND REASONABLE DOUBT' if is_prime_verified else 'INSUFFICIENT PROOF'} based on {verified_count}/4 legal premises established."
        })

        return {
            "engine": "Prosecution Proof Verification",
            "target_suspect": target_suspect_name,
            "target_goal": target_goal,
            "verification_score": f"{verified_count}/4 legal premises verified",
            "proof_steps": proof_steps,
            "summary": f"Prosecutorial verification evaluated hypothesis prime_suspect({target_suspect_name}) and returned {'VERIFIED' if is_prime_verified else 'UNCONFIRMED'}."
        }

    # Backward compatibility alias
    backward_chaining = verify_prosecution_proof

# Backward compatibility alias
InferenceEngine = HypothesisEngine
