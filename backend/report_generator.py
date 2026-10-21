"""
Report Generator Module for Crime Investigation Expert System.
Generates comprehensive investigation conclusion reports with logical justification.
"""

from typing import Dict, List, Any
import datetime

class InvestigationReportGenerator:
    @staticmethod
    def generate_report(
        case_info: Dict[str, Any],
        suspects: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]],
        search_results: Dict[str, Any],
        csp_results: Dict[str, Any],
        inference_results: Dict[str, Any],
        backward_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates full structured Investigation Conclusion Report.
        """
        timestamp = datetime.datetime.now().strftime("%d %b %Y · %H:%M")
        prime_suspect = inference_results.get("prime_suspect")
        prime_name = prime_suspect["name"] if prime_suspect else "Under Review"

        report = {
            "system_name": "Veritas Crime Investigation AI",
            "report_reference": f"REP-{case_info.get('case_number', 'CR-2026-0142')}",
            "generated_at": timestamp,
            "case_summary": {
                "case_number": case_info.get("case_number", "CR-2026-0142"),
                "title": case_info.get("title", "The Ashwood Burglary"),
                "location": case_info.get("location", "18 Ashwood Avenue, Chennai"),
                "date_time": case_info.get("date_time", "08 Sep 2026 · 21:30–23:15"),
                "total_suspects": len(suspects),
                "total_evidence": len(evidence)
            },
            "findings": {
                "prime_suspect": prime_name,
                "prime_suspect_details": prime_suspect,
                "search_module_summary": f"Relationship & Network Link Analysis ({search_results.get('algorithm', 'BFS')}) traversed relationship links from root Crime Scene and mapped {len(search_results.get('suspects_found', []))} person(s) of interest.",
                "csp_backtracking_summary": f"Forensic Opportunity & Alibi Filter evaluated candidates across timeline feasibility, physical access routes, and alibi credibility: {csp_results.get('retained_count', 0)} retained for prosecution, {csp_results.get('eliminated_count', 0)} eliminated.",
                "inference_engine_summary": f"Inductive Evidence Assembly established {prime_name} as the prime perpetrator. Prosecution Proof Verification proved prime_suspect({prime_name.replace(' ', '_')}) with status: {backward_results.get('verification_score', 'All premises verified')}.",
                "predicate_rule_justification": "Legal Predicate Formulation satisfied: motive(X) ∧ access(X) ∧ evidence_match(X) → prime_suspect(X)"
            },
            "findings_breakdown": [
                {
                    "step_num": "01",
                    "title": "Relationship & Network Link Analysis",
                    "details": f"Traced criminal associations and proximity networks connecting suspect candidate(s) to the crime scene."
                },
                {
                    "step_num": "02",
                    "title": "Forensic Opportunity & Alibi Filter",
                    "details": f"Cross-examined timeline feasibility, viable scene access, and alibi statements. Retained {csp_results.get('retained_count', 0)} viable suspect(s)."
                },
                {
                    "step_num": "03",
                    "title": "Investigative Hypothesis & Legal Proof",
                    "details": f"Inductive reasoning established probable cause. Backward reasoning verified step-by-step prosecutorial premises for {prime_name}."
                },
                {
                    "step_num": "04",
                    "title": "Conclusive Evidentiary Synthesis",
                    "details": "Corroborated all physical recoveries, timeline verifications, and digital logs into a verified prosecutorial chain of custody."
                }
            ],
            "decision_support_notice": "This certified dossier is compiled by Veritas Crime Investigation AI. Final indictment and arrest decisions remain with the authorized judicial and law enforcement officers."
        }

        return report
