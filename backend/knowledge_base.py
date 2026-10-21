"""
Knowledge Base & Predicate Logic Module for Crime Investigation Expert System.
Implements Predicate Logic and First-Order Logic (FOL) representation.
"""

from typing import List, Dict, Any, Set

class Fact:
    def __init__(self, predicate: str, entity: str, value: Any = True):
        self.predicate = predicate
        self.entity = entity.replace(" ", "_")
        self.value = value

    def to_fol(self) -> str:
        """Returns standard First-Order Logic predicate representation."""
        if isinstance(self.value, str):
            return f"{self.predicate}({self.entity}, {self.value.replace(' ', '_')})"
        return f"{self.predicate}({self.entity})"

    def __repr__(self):
        return self.to_fol()

class Rule:
    def __init__(self, rule_id: str, name: str, premises: List[str], conclusion: str, description: str = ""):
        self.rule_id = rule_id
        self.name = name
        self.premises = premises  # List of predicate names required
        self.conclusion = conclusion  # Predicate derived
        self.description = description

    def to_fol(self) -> str:
        """Returns First-Order Logic representation of IF-THEN rule."""
        premises_str = " ∧ ".join(self.premises)
        return f"{premises_str} → {self.conclusion}"

class KnowledgeBase:
    def __init__(self):
        self.facts: Set[str] = set()
        self.fact_objects: List[Fact] = []
        self.rules: List[Rule] = []

    def add_fact(self, predicate: str, entity: str, value: Any = True):
        fact = Fact(predicate, entity, value)
        self.fact_objects.append(fact)
        self.facts.add(fact.to_fol())

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def load_from_db_data(self, suspects: List[Dict[str, Any]], evidence: List[Dict[str, Any]]):
        """Converts database suspect and evidence records into Predicate Logic facts."""
        self.facts.clear()
        self.fact_objects.clear()

        for suspect in suspects:
            name = suspect['name']
            if suspect.get('has_motive'):
                self.add_fact("motive", name)
            if suspect.get('has_access') or suspect.get('physical_access_passed'):
                self.add_fact("access", name)
            if suspect.get('evidence_matched'):
                self.add_fact("evidence_match", name)
            if suspect.get('alibi_verified'):
                self.add_fact("alibi_verified", name)
            if suspect.get('time_window_passed'):
                self.add_fact("in_time_window", name)
            if suspect.get('contradicts_evidence'):
                self.add_fact("contradicts_evidence", name)

        for ev in evidence:
            ev_title = ev['title']
            self.add_fact("evidence_exists", ev_title, ev['category'])

        # Standard Forensic & Legal Expert Rules (Investigative Logic)
        self.add_rule(Rule(
            rule_id="R1",
            name="Primary Perpetrator Indictment Rule",
            premises=["motive(X)", "access(X)", "evidence_match(X)", "in_time_window(X)"],
            conclusion="prime_suspect(X)",
            description="If suspect X has recorded motive, viable physical access, matched forensic evidence, and fits the crime window, X is established as Prime Suspect."
        ))

        self.add_rule(Rule(
            rule_id="R2",
            name="Alibi-Based Forensic Exemption Rule",
            premises=["alibi_verified(X)", "NOT evidence_match(X)"],
            conclusion="eliminated(X)",
            description="If suspect X possesses a verified external alibi with zero direct forensic link, eliminate X from the suspect lineup."
        ))

        self.add_rule(Rule(
            rule_id="R3",
            name="Testimony Contradiction Exclusion Rule",
            premises=["contradicts_evidence(X)"],
            conclusion="eliminated(X)",
            description="If suspect X's statements or timeline directly contradict physical evidence, eliminate X as an active viable perpetrator."
        ))

        self.add_rule(Rule(
            rule_id="R4",
            name="Opportunity Feasibility Rule",
            premises=["in_time_window(X)", "access(X)"],
            conclusion="has_opportunity(X)",
            description="If suspect X was verified within the time window and had access routes into the scene, X has viable crime opportunity."
        ))

    def get_all_fol_facts(self) -> List[str]:
        return sorted(list(self.facts))

    def get_rules_fol(self) -> List[Dict[str, str]]:
        return [
            {
                "rule_id": r.rule_id,
                "name": r.name,
                "fol": r.to_fol(),
                "description": r.description
            }
            for r in self.rules
        ]
