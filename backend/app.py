"""
Flask Web Application & REST API for Crime Investigation Expert System.
Integrates Data Management, Investigation Network Search, Forensic Constraint Filtering,
and Rule-Based Legal Inference.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import json
import sys

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

app = Flask(__name__)
CORS(app)

# Initialize database on startup
init_db()
seed_database()

def row_to_dict(row):
    return dict(row) if row else None

@app.route('/', methods=['GET'])
def root_index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>VERITAS API Server</title>
        <style>
            body { font-family: system-ui, -apple-system, sans-serif; background: #0f1412; color: #e5ece8; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
            .card { background: #161e1a; border: 1px solid #283730; border-radius: 12px; padding: 32px; max-width: 520px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #53c48b; margin-top: 0; font-size: 24px; }
            p { color: #9bb0a5; line-height: 1.6; font-size: 14px; }
            .btn { display: inline-block; background: #2f855a; color: #fff; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 16px; }
            .btn:hover { background: #38a169; }
            code { background: #0a0d0c; padding: 2px 6px; border-radius: 4px; color: #7fe3ad; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Veritas Crime Investigation AI Backend is Online</h1>
            <p>This is the Python REST API server (Port 5000). The graphical user interface runs on Vite at Port 8443.</p>
            <p>To view the full investigation dashboard with cases, suspects, and forensic links, open the UI:</p>
            <a class="btn" href="http://localhost:8443">Open Investigation UI (Port 8443)</a>
        </div>
    </body>
    </html>
    """

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "system": "Veritas Crime Investigation AI",
        "version": "2.0.0",
        "python_version": "3.11+"
    })

# --- Authentication ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    badge_id = data.get('badge_id', 'INV-7042')
    password = data.get('password', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE badge_id = ?", (badge_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        u_dict = row_to_dict(user)
        u_dict.pop('password_hash', None)
        return jsonify({
            "authenticated": True,
            "user": u_dict,
            "token": f"auth_token_{badge_id}"
        })
    else:
        # Fallback default investigator
        return jsonify({
            "authenticated": True,
            "user": {
                "badge_id": badge_id,
                "name": "Inspector K. Rao",
                "role": "Lead Forensic Investigator",
                "department": "Cyber Crime & Special Operations"
            },
            "token": f"auth_token_{badge_id}"
        })

# --- Cases Dashboard ---
@app.route('/api/cases', methods=['GET'])
def get_cases():
    status_filter = request.args.get('status')
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT c.*,
           (SELECT COUNT(*) FROM suspects s WHERE s.case_id = c.id) AS suspect_count,
           (SELECT COUNT(*) FROM evidence e WHERE e.case_id = c.id) AS evidence_count
    FROM cases c
    """
    params = []
    if status_filter and status_filter.upper() != 'ALL':
        query += " WHERE c.status = ?"
        params.append(status_filter.upper())
    query += " ORDER BY c.id DESC"

    cursor.execute(query, params)
    cases = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(cases)

@app.route('/api/cases', methods=['POST'])
def create_case():
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    crime_type = data.get('crime_type', 'Burglary')
    priority = data.get('priority', 'HIGH')
    location = data.get('location', 'Chennai')
    date_time = data.get('date_time', 'Active Incident')
    description = data.get('description', 'Initial incident recorded.')

    if not title:
        return jsonify({"error": "Case title is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cases")
    count = cursor.fetchone()[0]
    case_number = data.get('case_number') or f"CR-2026-0{count + 150}"

    cursor.execute("""
    INSERT INTO cases (case_number, title, crime_type, priority, location, date_time, description, status, progress)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDING', 20)
    """, (case_number, title, crime_type, priority, location, date_time, description))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM cases WHERE id = ?", (new_id,))
    new_case = cursor.fetchone()
    conn.close()
    return jsonify(row_to_dict(new_case)), 201

@app.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case_by_id(case_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = cursor.fetchone()
    if not case:
        conn.close()
        return jsonify({"error": "Case not found"}), 404

    cursor.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,))
    suspects = [row_to_dict(r) for r in cursor.fetchall()]
    cursor.execute("SELECT * FROM evidence WHERE case_id = ?", (case_id,))
    evidence = [row_to_dict(r) for r in cursor.fetchall()]
    conn.close()

    result = row_to_dict(case)
    result["suspects"] = suspects
    result["evidence"] = evidence
    return jsonify(result)

@app.route('/api/cases/<int:case_id>/status', methods=['PUT'])
def update_case_status(case_id):
    data = request.get_json(silent=True) or {}
    status = data.get('status', 'ACTIVE')
    progress = data.get('progress')

    conn = get_db_connection()
    cursor = conn.cursor()
    if progress is not None:
        cursor.execute("UPDATE cases SET status = ?, progress = ? WHERE id = ?", (status, progress, case_id))
    else:
        cursor.execute("UPDATE cases SET status = ? WHERE id = ?", (status, case_id))
    conn.commit()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    updated = cursor.fetchone()
    conn.close()
    return jsonify(row_to_dict(updated))

@app.route('/api/case', methods=['GET'])
def get_default_case():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases ORDER BY id LIMIT 1")
    case = cursor.fetchone()
    conn.close()
    if case:
        return jsonify(row_to_dict(case))
    return jsonify({"error": "No case found"}), 404

@app.route('/api/case', methods=['PUT'])
def update_default_case():
    data = request.get_json(silent=True) or {}
    case_id = data.get('id')
    title = data.get('title')
    location = data.get('location')
    date_time = data.get('date_time')
    description = data.get('description')

    conn = get_db_connection()
    cursor = conn.cursor()
    if case_id:
        cursor.execute("""
        UPDATE cases SET title = COALESCE(?, title),
                         location = COALESCE(?, location),
                         date_time = COALESCE(?, date_time),
                         description = COALESCE(?, description)
        WHERE id = ?
        """, (title, location, date_time, description, case_id))
    else:
        cursor.execute("""
        UPDATE cases SET title = COALESCE(?, title),
                         location = COALESCE(?, location),
                         date_time = COALESCE(?, date_time),
                         description = COALESCE(?, description)
        WHERE id = (SELECT id FROM cases ORDER BY id LIMIT 1)
        """, (title, location, date_time, description))
    conn.commit()

    target_id = case_id if case_id else 1
    cursor.execute("SELECT * FROM cases WHERE id = ?", (target_id,))
    updated = cursor.fetchone()
    conn.close()
    return jsonify(row_to_dict(updated))

# --- Suspects ---
@app.route('/api/suspects', methods=['GET'])
def get_suspects():
    case_id = request.args.get('case_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    if case_id:
        cursor.execute("SELECT * FROM suspects WHERE case_id = ? ORDER BY id ASC", (case_id,))
    else:
        cursor.execute("SELECT * FROM suspects ORDER BY id ASC")
    suspects = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(suspects)

@app.route('/api/suspects', methods=['POST'])
def add_suspect():
    data = request.get_json(silent=True) or {}
    case_id = data.get('case_id')
    name = data.get('name')
    role = data.get('role')
    color = data.get('color', '#526D63')
    notes = data.get('notes', 'Profile registered by investigator')

    if not name or not role:
        return jsonify({"error": "Name and role are required"}), 400

    initials = "".join([part[0] for part in name.split()]).upper()[:2]

    conn = get_db_connection()
    cursor = conn.cursor()
    if not case_id:
        cursor.execute("SELECT id FROM cases ORDER BY id LIMIT 1")
        case = cursor.fetchone()
        case_id = case['id'] if case else 1

    cursor.execute("""
    INSERT INTO suspects (
        case_id, name, initials, role, color, status, links_info,
        has_motive, has_access, time_window_passed, physical_access_passed,
        evidence_matched, alibi_verified, contradicts_evidence, notes
    ) VALUES (?, ?, ?, ?, ?, 'Needs review', 'Not checked', 0, 1, 1, 1, 0, 0, 0, ?)
    """, (case_id, name, initials, role, color, notes))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM suspects WHERE id = ?", (new_id,))
    new_suspect = cursor.fetchone()
    conn.close()
    return jsonify(row_to_dict(new_suspect)), 201

# --- Evidence ---
@app.route('/api/evidence', methods=['GET'])
def get_evidence():
    case_id = request.args.get('case_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    if case_id:
        cursor.execute("SELECT * FROM evidence WHERE case_id = ? ORDER BY id ASC", (case_id,))
    else:
        cursor.execute("SELECT * FROM evidence ORDER BY id ASC")
    evidence = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(evidence)

@app.route('/api/evidence', methods=['POST'])
def add_evidence():
    data = request.get_json(silent=True) or {}
    case_id = data.get('case_id')
    title = data.get('title')
    category = data.get('category', 'Physical object')
    meta_info = data.get('details', '')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    icon = 'camera' if 'cctv' in category.lower() else ('fingerprint' if 'fingerprint' in category.lower() or 'dna' in category.lower() else ('evidence' if 'weapon' in category.lower() or 'object' in category.lower() else 'file'))
    tag = 'LOGGED'
    tone = 'gold'

    conn = get_db_connection()
    cursor = conn.cursor()
    if not case_id:
        cursor.execute("SELECT id FROM cases ORDER BY id LIMIT 1")
        case = cursor.fetchone()
        case_id = case['id'] if case else 1

    cursor.execute("""
    INSERT INTO evidence (case_id, icon, title, category, meta_info, tag, tone, details)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (case_id, icon, title, category, meta_info, tag, tone, meta_info))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM evidence WHERE id = ?", (new_id,))
    new_ev = cursor.fetchone()
    conn.close()
    return jsonify(row_to_dict(new_ev)), 201

# --- AI Module 1: Relationship & Network Link Analysis (Search) ---
@app.route('/api/search', methods=['GET'])
def search_suspects():
    case_id = request.args.get('case_id')
    technique = request.args.get('algorithm', 'BFS').upper()

    conn = get_db_connection()
    cursor = conn.cursor()
    if case_id:
        cursor.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,))
        suspects = [row_to_dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence WHERE case_id = ?", (case_id,))
        evidence = [row_to_dict(r) for r in cursor.fetchall()]
    else:
        cursor.execute("SELECT * FROM suspects")
        suspects = [row_to_dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence")
        evidence = [row_to_dict(r) for r in cursor.fetchall()]
    conn.close()

    graph = InvestigationGraph()
    graph.build_graph(suspects, evidence)

    if technique == 'DFS':
        raw_res = graph.dfs_search()
        mode_label = "Deep Evidence Thread (DFS)"
        inv_explanation = "Traced each suspect's associated forensic chain deeply to its conclusion before examining neighboring parties."
    else:
        raw_res = graph.bfs_search()
        mode_label = "Perimeter & Relationship Sweep (BFS)"
        inv_explanation = "Conducted a level-by-level perimeter sweep, identifying all immediate scene contacts before deeper evidence analysis."

    return jsonify({
        "module_name": "Relationship & Network Link Analysis",
        "investigation_mode": mode_label,
        "algorithm_reference": raw_res.get("algorithm", mode_label),
        "explanation": inv_explanation,
        "traversal_order": raw_res["traversal_order"],
        "traversal_details": raw_res["traversal_details"],
        "suspects_found": raw_res["suspects_found"]
    })

# --- AI Module 2: Forensic Constraint & Opportunity Filter (CSP) ---
@app.route('/api/csp-eliminate', methods=['POST'])
def csp_eliminate():
    data = request.get_json(silent=True) or {}
    case_id = data.get('case_id') or request.args.get('case_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    if case_id:
        cursor.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,))
    else:
        cursor.execute("SELECT * FROM suspects")
    suspects = [row_to_dict(r) for r in cursor.fetchall()]
    conn.close()

    solver = CSPSolver()
    results = solver.solve_backtracking(suspects)

    return jsonify({
        "module_name": "Forensic Opportunity & Alibi Filter",
        "investigation_action": "Systematic evaluation of timeline feasibility, physical access opportunities, and alibi credibility",
        "total_evaluated": results.get("total_evaluated", len(suspects)),
        "retained_count": results.get("retained_count", 0),
        "eliminated_count": results.get("eliminated_count", 0),
        "total_constraint_checks": results.get("total_constraint_checks", 0),
        "retained_suspects": results.get("retained_suspects", []),
        "eliminated_suspects": results.get("eliminated_suspects", []),
        "evaluations": results.get("evaluations", []),
        "summary": results.get("summary", "")
    })

# --- AI Module 3: Investigative Hypothesis & Legal Proof Engine (Inference) ---
@app.route('/api/infer', methods=['POST'])
def run_inference():
    data = request.get_json(silent=True) or {}
    case_id = data.get('case_id') or request.args.get('case_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    if case_id:
        cursor.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,))
        suspects = [row_to_dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence WHERE case_id = ?", (case_id,))
        evidence = [row_to_dict(r) for r in cursor.fetchall()]
    else:
        cursor.execute("SELECT * FROM suspects")
        suspects = [row_to_dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence")
        evidence = [row_to_dict(r) for r in cursor.fetchall()]
    conn.close()

    kb = KnowledgeBase()
    kb.load_from_db_data(suspects, evidence)

    engine = InferenceEngine(kb)
    forward_res = engine.forward_chaining(suspects)

    prime = forward_res.get('prime_suspect')
    prime_name = prime['name'] if prime else (suspects[0]['name'] if suspects else "Unknown")

    backward_res = engine.backward_chaining(prime_name, suspects)

    # Update case progress & prime suspect in database if case_id provided
    if case_id and prime:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE cases SET prime_suspect = ?, progress = 85, status = 'ACTIVE' WHERE id = ?", (prime['name'], case_id))
            conn.commit()
            conn.close()
        except Exception:
            pass

    return jsonify({
        "module_name": "Investigative Hypothesis & Legal Proof Engine",
        "prime_suspect_identified": prime_name,
        "forward_reasoning": {
            "title": "Inductive Evidence Assembly",
            "findings": forward_res.get("inferred_conclusions", []),
            "legal_rule_applied": forward_res.get("predicate_rule_applied", "motive(x) ∧ access(x) ∧ evidence_match(x) → prime_suspect(x)"),
            "suspect_analysis": forward_res.get("suspect_analysis", [])
        },
        "backward_reasoning": {
            "title": "Prosecution Proof & Verification",
            "target_hypothesis": f"Is {prime_name} the prime suspect?",
            "verification_status": backward_res.get("summary", "Verified"),
            "proof_steps": backward_res.get("proof_steps", [])
        },
        "fol_facts": kb.get_all_fol_facts(),
        "fol_rules": kb.get_rules_fol()
    })

# --- Case Forensic Docket / Report ---
@app.route('/api/report', methods=['GET'])
def get_report():
    case_id = request.args.get('case_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    if case_id:
        cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
        case = row_to_dict(cursor.fetchone())
        cursor.execute("SELECT * FROM suspects WHERE case_id = ?", (case_id,))
        suspects = [row_to_dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence WHERE case_id = ?", (case_id,))
        evidence = [row_to_dict(r) for r in cursor.fetchall()]
    else:
        cursor.execute("SELECT * FROM cases ORDER BY id LIMIT 1")
        case = row_to_dict(cursor.fetchone())
        cursor.execute("SELECT * FROM suspects")
        suspects = [row_to_dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM evidence")
        evidence = [row_to_dict(r) for r in cursor.fetchall()]
    conn.close()

    graph = InvestigationGraph()
    graph.build_graph(suspects, evidence)
    search_res = graph.bfs_search()

    solver = CSPSolver()
    csp_res = solver.solve_backtracking(suspects)

    kb = KnowledgeBase()
    kb.load_from_db_data(suspects, evidence)
    engine = InferenceEngine(kb)
    forward_res = engine.forward_chaining(suspects)

    prime = forward_res.get('prime_suspect')
    prime_name = prime['name'] if prime else (suspects[0]['name'] if suspects else "Unknown")
    backward_res = engine.backward_chaining(prime_name, suspects)

    report = InvestigationReportGenerator.generate_report(
        case, suspects, evidence, search_res, csp_res, forward_res, backward_res
    )
    return jsonify(report)

@app.route('/api/seed', methods=['POST'])
def reset_seed():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS cases")
    cursor.execute("DROP TABLE IF EXISTS suspects")
    cursor.execute("DROP TABLE IF EXISTS evidence")
    cursor.execute("DROP TABLE IF EXISTS rules")
    conn.commit()
    conn.close()

    init_db()
    seed_database()
    return jsonify({"message": "Database reset and seeded with Kaggle-curated crime investigation dataset."})

if __name__ == '__main__':
    print("Starting VERITAS Criminal Investigation Expert System Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
