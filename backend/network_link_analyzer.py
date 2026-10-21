"""
Relationship & Network Link Analysis Module for Criminal Investigation System.
Maps connections between the crime scene, suspects, and recovered physical/digital evidence.
"""

from collections import deque
from typing import Dict, List, Any, Set, Tuple

class NetworkLinkAnalyzer:
    def __init__(self):
        # Adjacency list: node_id -> list of connected node_ids
        self.graph: Dict[str, List[str]] = {}
        self.node_details: Dict[str, Dict[str, Any]] = {}

    def build_network(self, suspects: List[Dict[str, Any]], evidence: List[Dict[str, Any]]):
        """
        Builds relationship network from the central Crime Scene (C).
        Root: C (Crime Scene)
        Level 1: Suspect Nodes (persons of interest)
        Level 2: Forensic Evidence Links bound to suspects
        """
        self.graph.clear()
        self.node_details.clear()

        root_id = "CRIME_SCENE_C"
        self.graph[root_id] = []
        self.node_details[root_id] = {
            "id": root_id,
            "label": "Crime Scene (C)",
            "type": "ROOT"
        }

        # Connect root to suspect nodes
        for suspect in suspects:
            s_id = f"SUSPECT_{suspect['initials']}"
            self.graph[root_id].append(s_id)
            if s_id not in self.graph:
                self.graph[s_id] = []

            self.node_details[s_id] = {
                "id": s_id,
                "label": f"{suspect['name']} ({suspect['initials']})",
                "type": "SUSPECT",
                "suspect_data": suspect
            }

            # Connect suspect to evidence nodes if matched
            if suspect.get('evidence_matched'):
                ev_id = f"EV_FORENSIC_{suspect['initials']}"
                self.graph[s_id].append(ev_id)
                self.graph[ev_id] = []
                self.node_details[ev_id] = {
                    "id": ev_id,
                    "label": f"Forensic Match ({suspect['initials']})",
                    "type": "EVIDENCE"
                }

            if suspect.get('has_motive'):
                mot_id = f"EV_MOTIVE_{suspect['initials']}"
                self.graph[s_id].append(mot_id)
                self.graph[mot_id] = []
                self.node_details[mot_id] = {
                    "id": mot_id,
                    "label": f"Motive Record ({suspect['initials']})",
                    "type": "EVIDENCE"
                }

    # Backward compatibility alias
    build_graph = build_network

    def perimeter_sweep(self, start_node: str = "CRIME_SCENE_C") -> Dict[str, Any]:
        """
        Executes Perimeter & Relationship Sweep.
        Explores all direct connections to the crime scene level-by-level before moving to deep evidence chains.
        """
        visited: Set[str] = set()
        queue = deque([start_node])
        traversal_order = []
        visited_nodes_info = []

        visited.add(start_node)

        while queue:
            current = queue.popleft()
            traversal_order.append(current)
            if current in self.node_details:
                visited_nodes_info.append(self.node_details[current])

            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        candidate_suspects = [
            info["suspect_data"]
            for info in visited_nodes_info
            if info.get("type") == "SUSPECT"
        ]

        return {
            "technique": "Perimeter Sweep",
            "algorithm": "Perimeter Sweep",
            "name": "Perimeter & Relationship Sweep",
            "explanation": "Conducted a perimeter sweep, exploring immediate crime scene contacts and associates before examining deep evidence chains.",
            "traversal_order": traversal_order,
            "traversal_details": visited_nodes_info,
            "suspects_found": candidate_suspects
        }

    # Backward compatibility alias
    bfs_search = perimeter_sweep

    def deep_evidence_trace(self, start_node: str = "CRIME_SCENE_C") -> Dict[str, Any]:
        """
        Executes Deep Evidence Thread analysis.
        Traces each suspect's full evidence chain to its conclusion before exploring neighboring candidates.
        """
        visited: Set[str] = set()
        traversal_order = []
        visited_nodes_info = []

        def trace_recursive(node: str):
            visited.add(node)
            traversal_order.append(node)
            if node in self.node_details:
                visited_nodes_info.append(self.node_details[node])

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    trace_recursive(neighbor)

        trace_recursive(start_node)

        candidate_suspects = [
            info["suspect_data"]
            for info in visited_nodes_info
            if info.get("type") == "SUSPECT"
        ]

        return {
            "technique": "Evidence Chain Trace",
            "algorithm": "Evidence Chain Trace",
            "name": "Deep Evidence Thread",
            "explanation": "Traced each suspect's forensic evidence thread to its conclusion before examining the next candidate path.",
            "traversal_order": traversal_order,
            "traversal_details": visited_nodes_info,
            "suspects_found": candidate_suspects
        }

    # Backward compatibility alias
    dfs_search = deep_evidence_trace

# Backward compatibility alias
InvestigationGraph = NetworkLinkAnalyzer
