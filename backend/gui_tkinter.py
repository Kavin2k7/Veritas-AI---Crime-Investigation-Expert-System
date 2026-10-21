"""
Tkinter Desktop User Interface for Crime Investigation Expert System.
Provides native Python Desktop GUI for database management, BFS/DFS search,
CSP constraint evaluation, and rule-based inference report generation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import os
import sys

# Ensure backend modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.database import get_db_connection, init_db, seed_database
    from backend.knowledge_base import KnowledgeBase
    from backend.network_link_analyzer import NetworkLinkAnalyzer, InvestigationGraph
    from backend.forensic_filter import ForensicFilter, CSPSolver
    from backend.hypothesis_engine import HypothesisEngine, InferenceEngine
    from backend.report_generator import InvestigationReportGenerator
except ImportError:
    from database import get_db_connection, init_db, seed_database
    from knowledge_base import KnowledgeBase
    from network_link_analyzer import NetworkLinkAnalyzer, InvestigationGraph
    from forensic_filter import ForensicFilter, CSPSolver
    from hypothesis_engine import HypothesisEngine, InferenceEngine
    from report_generator import InvestigationReportGenerator


class CrimeInvestigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VERITAS · Crime Investigation Expert System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0F172A")

        # Initialize DB
        init_db()
        seed_database()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background="#0F172A", foreground="#F8FAFC", font=("Segoe UI", 10))
        self.style.configure("TLabel", background="#0F172A", foreground="#F8FAFC")
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#38BDF8")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 11, "italic"), foreground="#94A3B8")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#0284C7", foreground="#FFFFFF", padding=6)
        self.style.map("TButton", background=[("active", "#0369A1")])
        self.style.configure("Treeview", background="#1E293B", foreground="#F8FAFC", fieldbackground="#1E293B", rowheight=28)
        self.style.configure("Treeview.Heading", background="#334155", foreground="#38BDF8", font=("Segoe UI", 10, "bold"))

        # Main Layout
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0F172A", pady=10, padx=15)
        header_frame.pack(fill="x")

        ttk.Label(header_frame, text="VERITAS · CRIME INVESTIGATION EXPERT SYSTEM", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Foundations of AI · Decision Support & Rule-Based Inference", style="SubHeader.TLabel").pack(anchor="w")

        # Tabs Frame
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab 1: Database & Case Management
        self.tab_data = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_data, text=" 📊 Case Docket & Suspects ")
        self.setup_data_tab()

        # Tab 2: Network Link Analysis
        self.tab_search = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text=" 🔍 Network Link Analysis ")
        self.setup_search_tab()

        # Tab 3: Opportunity & Alibi Filter
        self.tab_csp = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_csp, text=" ⚡ Opportunity & Alibi Filter ")
        self.setup_csp_tab()

        # Tab 4: Hypothesis & Legal Proof
        self.tab_infer = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_infer, text=" 🧠 Hypothesis & Legal Proof ")
        self.setup_infer_tab()

    def setup_data_tab(self):
        top_frame = tk.Frame(self.tab_data, bg="#0F172A", pady=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Registered Suspect Profiles (SQLite Knowledge Base)", font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Button(top_frame, text="🔄 Refresh Data", command=self.load_data).pack(side="right", padx=5)
        ttk.Button(top_frame, text="➕ Add Suspect", command=self.open_add_suspect_dialog).pack(side="right", padx=5)

        # Treeview Table
        columns = ("id", "name", "role", "motive", "access", "ev_match", "status")
        self.suspect_tree = ttk.Treeview(self.tab_data, columns=columns, show="headings", selectmode="browse")
        
        self.suspect_tree.heading("id", text="ID")
        self.suspect_tree.heading("name", text="Suspect Name")
        self.suspect_tree.heading("role", text="Role / Relation")
        self.suspect_tree.heading("motive", text="Motive")
        self.suspect_tree.heading("access", text="Access")
        self.suspect_tree.heading("ev_match", text="Evidence Match")
        self.suspect_tree.heading("status", text="Status")

        self.suspect_tree.column("id", width=40, anchor="center")
        self.suspect_tree.column("name", width=180)
        self.suspect_tree.column("role", width=160)
        self.suspect_tree.column("motive", width=80, anchor="center")
        self.suspect_tree.column("access", width=80, anchor="center")
        self.suspect_tree.column("ev_match", width=120, anchor="center")
        self.suspect_tree.column("status", width=140, anchor="center")

        self.suspect_tree.pack(fill="both", expand=True, pady=5)

    def open_add_suspect_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Suspect")
        dialog.geometry("400x350")
        dialog.configure(bg="#1E293B")

        tk.Label(dialog, text="Full Name:", bg="#1E293B", fg="#F8FAFC").pack(anchor="w", padx=20, pady=(15, 2))
        name_ent = tk.Entry(dialog, width=35)
        name_ent.pack(padx=20, pady=5)

        tk.Label(dialog, text="Role / Relation:", bg="#1E293B", fg="#F8FAFC").pack(anchor="w", padx=20, pady=(10, 2))
        role_ent = tk.Entry(dialog, width=35)
        role_ent.pack(padx=20, pady=5)

        motive_var = tk.BooleanVar()
        tk.Checkbutton(dialog, text="Has Financial/Personal Motive", variable=motive_var, bg="#1E293B", fg="#F8FAFC", selectcolor="#0F172A").pack(anchor="w", padx=20, pady=10)

        access_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dialog, text="Physical Access to Scene", variable=access_var, bg="#1E293B", fg="#F8FAFC", selectcolor="#0F172A").pack(anchor="w", padx=20, pady=5)

        def save():
            name = name_ent.get().strip()
            role = role_ent.get().strip()
            if not name or not role:
                messagebox.showerror("Error", "Name and Role are required!")
                return
            
            initials = "".join([part[0] for part in name.split()]).upper()[:2]
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cases LIMIT 1")
            c = cursor.fetchone()
            case_id = c['id'] if c else 1

            cursor.execute("""
            INSERT INTO suspects (case_id, name, initials, role, color, status, links_info, has_motive, has_access, time_window_passed, physical_access_passed)
            VALUES (?, ?, ?, ?, '#526D63', 'Needs review', 'Not checked', ?, ?, 1, 1)
            """, (case_id, name, initials, role, 1 if motive_var.get() else 0, 1 if access_var.get() else 0))
            conn.commit()
            conn.close()
            dialog.destroy()
            self.load_data()
            messagebox.showinfo("Success", f"Added suspect {name}")

        tk.Button(dialog, text="Save Suspect", command=save, bg="#0284C7", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=20)

    def load_data(self):
        for item in self.suspect_tree.get_children():
            self.suspect_tree.delete(item)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suspects ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            self.suspect_tree.insert("", "end", values=(
                r["id"],
                r["name"],
                r["role"],
                "YES" if r["has_motive"] else "NO",
                "YES" if r["has_access"] else "NO",
                "YES" if r["evidence_matched"] else "NO",
                r["status"]
            ))

    def setup_search_tab(self):
        frame = tk.Frame(self.tab_search, bg="#0F172A", pady=10)
        frame.pack(fill="both", expand=True)

        btn_frame = tk.Frame(frame, bg="#0F172A")
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="▶ Perimeter & Relationship Sweep (BFS)", command=lambda: self.run_search("BFS")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="▶ Deep Evidence Thread (DFS)", command=lambda: self.run_search("DFS")).pack(side="left", padx=5)

        self.search_output = tk.Text(frame, bg="#1E293B", fg="#38BDF8", font=("Consolas", 10), wrap="word")
        self.search_output.pack(fill="both", expand=True, pady=10)

    def run_search(self, algo):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suspects")
        suspects = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence")
        evidence = [dict(r) for r in cursor.fetchall()]
        conn.close()

        graph = InvestigationGraph()
        graph.build_graph(suspects, evidence)

        res = graph.dfs_search() if algo == "DFS" else graph.bfs_search()

        self.search_output.delete("1.0", tk.END)
        self.search_output.insert(tk.END, f"=== ALGORITHM: {res['name']} ({algo}) ===\n")
        self.search_output.insert(tk.END, f"EXPLANATION: {res['explanation']}\n\n")
        self.search_output.insert(tk.END, f"GRAPH TRAVERSAL PATH:\n")
        for node in res["traversal_details"]:
            self.search_output.insert(tk.END, f" -> Node: {node['id']} | Label: {node['label']} | Type: {node['type']}\n")
        
        self.search_output.insert(tk.END, f"\nSUSPECTS FOUND ({len(res['suspects_found'])}):\n")
        for s in res["suspects_found"]:
            self.search_output.insert(tk.END, f" - {s['name']} ({s['role']})\n")

    def setup_csp_tab(self):
        frame = tk.Frame(self.tab_csp, bg="#0F172A", pady=10)
        frame.pack(fill="both", expand=True)

        ttk.Button(frame, text="⚡ Run Forensic Opportunity & Alibi Filter (CSP Backtracking)", command=self.run_csp).pack(anchor="w", pady=5)

        self.csp_output = tk.Text(frame, bg="#1E293B", fg="#4ADE80", font=("Consolas", 10), wrap="word")
        self.csp_output.pack(fill="both", expand=True, pady=10)

    def run_csp(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suspects")
        suspects = [dict(r) for r in cursor.fetchall()]
        conn.close()

        solver = CSPSolver()
        res = solver.solve_backtracking(suspects)

        self.csp_output.delete("1.0", tk.END)
        self.csp_output.insert(tk.END, f"=== CONSTRAINT SATISFACTION PROBLEM (CSP) & BACKTRACKING ===\n")
        self.csp_output.insert(tk.END, f"SUMMARY: {res['summary']}\n\n")
        
        for ev in res["evaluations"]:
            status_symbol = "✔ RETAINED" if ev["final_status"] == "RETAINED" else "✖ ELIMINATED"
            self.csp_output.insert(tk.END, f"Suspect: {ev['name']} ({ev['role']}) -> {status_symbol}\n")
            for c in ev["constraint_results"]:
                check_mark = "[PASS]" if c["passed"] else "[FAIL]"
                self.csp_output.insert(tk.END, f"    {check_mark} {c['constraint_name']}: {c['reason']}\n")
            self.csp_output.insert(tk.END, "-"*60 + "\n")

    def setup_infer_tab(self):
        frame = tk.Frame(self.tab_infer, bg="#0F172A", pady=10)
        frame.pack(fill="both", expand=True)

        ttk.Button(frame, text="🧠 Execute Investigative Hypothesis & Legal Proof Engine", command=self.run_infer).pack(anchor="w", pady=5)

        self.infer_output = tk.Text(frame, bg="#1E293B", fg="#FACC15", font=("Consolas", 10), wrap="word")
        self.infer_output.pack(fill="both", expand=True, pady=10)

    def run_infer(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases LIMIT 1")
        case = dict(cursor.fetchone())
        cursor.execute("SELECT * FROM suspects")
        suspects = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence")
        evidence = [dict(r) for r in cursor.fetchall()]
        conn.close()

        kb = KnowledgeBase()
        kb.load_from_db_data(suspects, evidence)

        engine = InferenceEngine(kb)
        f_res = engine.forward_chaining(suspects)

        prime = f_res.get("prime_suspect")
        prime_name = prime["name"] if prime else "Arjun Rao"

        b_res = engine.backward_chaining(prime_name, suspects)

        self.infer_output.delete("1.0", tk.END)
        self.infer_output.insert(tk.END, f"=== FORWARD CHAINING INFERENCE ENGINE ===\n")
        self.infer_output.insert(tk.END, f"RULE APPLIED: {f_res['predicate_rule_applied']}\n")
        self.infer_output.insert(tk.END, f"IDENTIFIED PRIME SUSPECT: {prime_name}\n\n")

        self.infer_output.insert(tk.END, f"=== BACKWARD CHAINING EXPLANATION PROOF ===\n")
        self.infer_output.insert(tk.END, f"TARGET GOAL: {b_res['target_goal']}\n")
        self.infer_output.insert(tk.END, f"RESULT: {b_res['summary']}\n\n")
        self.infer_output.insert(tk.END, "PROOF STEPS:\n")
        for step in b_res["proof_steps"]:
            self.infer_output.insert(tk.END, f" Step {step['step']}: {step['explanation']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrimeInvestigationApp(root)
    root.mainloop()
