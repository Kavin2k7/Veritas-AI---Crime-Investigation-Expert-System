import sqlite3
import json
import os
from typing import Dict, List, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "crime_investigation.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database tables for the Crime Investigation Expert System."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table for investigator authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        badge_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        department TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    # Create Cases table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        crime_type TEXT DEFAULT 'Burglary',
        priority TEXT DEFAULT 'HIGH',
        location TEXT NOT NULL,
        date_time TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'PENDING',  -- PENDING, ACTIVE, COMPLETED
        progress INTEGER DEFAULT 25,
        prime_suspect TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Suspects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suspects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        initials TEXT NOT NULL,
        role TEXT NOT NULL,
        color TEXT DEFAULT '#65786D',
        status TEXT DEFAULT 'Needs review',
        links_info TEXT DEFAULT '0 evidence links',
        has_motive INTEGER DEFAULT 0,
        has_access INTEGER DEFAULT 0,
        time_window_passed INTEGER DEFAULT 0,
        physical_access_passed INTEGER DEFAULT 0,
        evidence_matched INTEGER DEFAULT 0,
        alibi_verified INTEGER DEFAULT 0,
        contradicts_evidence INTEGER DEFAULT 0,
        notes TEXT,
        FOREIGN KEY (case_id) REFERENCES cases (id) ON DELETE CASCADE
    )
    """)

    # Create Evidence table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        icon TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        meta_info TEXT NOT NULL,
        tag TEXT NOT NULL,
        tone TEXT DEFAULT 'gold',
        details TEXT,
        FOREIGN KEY (case_id) REFERENCES cases (id) ON DELETE CASCADE
    )
    """)

    # Create Logic Rules table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        rule_name TEXT NOT NULL,
        premise TEXT NOT NULL,
        conclusion TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (case_id) REFERENCES cases (id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

def seed_database():
    """Populates the database with default Kaggle-curated crime investigation dataset."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Seed default investigators if none exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("INV-7042", "Inspector K. Rao", "Lead Forensic Investigator", "Cyber Crime & Special Operations", "investigator123"),
            ("CSI-3081", "Detective Priya Nair", "Forensic Logic Specialist", "Digital Forensics & Ballistics", "detective123"),
            ("DIR-1001", "Commissioner S. Varma", "Chief of Intelligence", "Directorate of Criminal Investigation", "admin123")
        ]
        cursor.executemany("""
        INSERT INTO users (badge_id, name, role, department, password_hash)
        VALUES (?, ?, ?, ?, ?)
        """, users)

    cursor.execute("SELECT COUNT(*) FROM cases")
    count = cursor.fetchone()[0]

    if count == 0:
        # Case 1: The Ashwood Burglary (Active)
        cursor.execute("""
        INSERT INTO cases (case_number, title, crime_type, priority, location, date_time, description, status, progress, prime_suspect)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "CR-2026-0142",
            "The Ashwood Burglary",
            "High-Value Residence Burglary",
            "HIGH",
            "18 Ashwood Avenue, Chennai",
            "08 Sep 2026 · 21:30–23:15",
            "High-value residence burglary involving forced study window entry and missing bearer bonds.",
            "ACTIVE",
            75,
            "Arjun Rao"
        ))
        case1_id = cursor.lastrowid

        # Suspects for Case 1
        suspects_case1 = [
            (case1_id, "Arjun Rao", "AR", "Former employee", "#C36A49", "Prime suspect", "3 evidence links", 1, 1, 1, 1, 1, 0, 0, "Financial dispute recorded, matched fingerprint at study window"),
            (case1_id, "Nila Menon", "NM", "Business associate", "#65786D", "Needs review", "2 evidence links", 1, 0, 1, 0, 0, 0, 0, "Stated alibi unverified, business motive present"),
            (case1_id, "Vikram Kumar", "VK", "Security guard", "#8B7765", "Needs review", "1 evidence link", 0, 1, 1, 1, 0, 1, 0, "Had access, partial alibi verified by guard log"),
            (case1_id, "Dev Sharma", "DS", "Neighbor", "#776C8D", "Eliminated", "No valid links", 0, 0, 0, 0, 0, 1, 1, "Alibi fully verified by camera footage outside area")
        ]
        cursor.executemany("""
        INSERT INTO suspects (case_id, name, initials, role, color, status, links_info, has_motive, has_access, time_window_passed, physical_access_passed, evidence_matched, alibi_verified, contradicts_evidence, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, suspects_case1)

        # Evidence for Case 1
        evidence_case1 = [
            (case1_id, "fingerprint", "Partial fingerprint", "Fingerprint", "Study window frame", "MATCH", "red", "Forensic ridge analysis matched suspect Arjun Rao"),
            (case1_id, "camera", "CCTV gate footage", "CCTV footage", "East gate · 22:14", "VERIFIED", "green", "Shows hooded individual of matching height exiting premises"),
            (case1_id, "file", "Forensic audit statement", "Witness statement", "Recorded · 09 Sep 2026", "VALIDATED", "green", "Confirming unresolved financial grudge against victim"),
            (case1_id, "evidence", "Recovered pry tool", "Weapon / object", "Tool bag E-07", "STORED", "gold", "Tool marks consistent with window frame splintering")
        ]
        cursor.executemany("""
        INSERT INTO evidence (case_id, icon, title, category, meta_info, tag, tone, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, evidence_case1)

        # Case 2: Marina Cyber Financial Embezzlement (Pending)
        cursor.execute("""
        INSERT INTO cases (case_number, title, crime_type, priority, location, date_time, description, status, progress, prime_suspect)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "CR-2026-0219",
            "Marina Bay Embezzlement",
            "Cyber Financial Fraud",
            "CRITICAL",
            "Tech Hub Towers, OMR, Chennai",
            "14 Sep 2026 · 02:15–03:40",
            "Unauthorized wire transfer of $1.4M routed through overseas proxy VPN nodes during system maintenance.",
            "PENDING",
            30,
            None
        ))
        case2_id = cursor.lastrowid

        suspects_case2 = [
            (case2_id, "Rohan Mehra", "RM", "Lead Systems Architect", "#4F46E5", "Needs review", "3 evidence links", 1, 1, 1, 1, 1, 0, 0, "Authorized root credentials used during maintenance window"),
            (case2_id, "Kavita Sen", "KS", "Senior Financial Officer", "#EC4899", "Needs review", "2 evidence links", 1, 0, 1, 0, 0, 0, 0, "Secondary authorization key approved wire request"),
            (case2_id, "Tariq Siddiqui", "TS", "Contract IT Specialist", "#10B981", "Needs review", "1 evidence link", 0, 1, 1, 1, 0, 1, 0, "Physical badge logged in server facility at 02:30")
        ]
        cursor.executemany("""
        INSERT INTO suspects (case_id, name, initials, role, color, status, links_info, has_motive, has_access, time_window_passed, physical_access_passed, evidence_matched, alibi_verified, contradicts_evidence, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, suspects_case2)

        evidence_case2 = [
            (case2_id, "file", "SSH Server Auth Logs", "Digital evidence", "Server Node Alpha-04", "LOGGED", "red", "Root session opened from terminal 192.168.1.104"),
            (case2_id, "camera", "Server Room Access Cam", "CCTV footage", "Datacenter Door B", "VERIFIED", "green", "Timestamp matches biometric swipe 02:18"),
            (case2_id, "evidence", "Seized Encrypted USB", "Hardware object", "Desk drawer 3B", "STORED", "gold", "Encrypted partition contains routing scripts")
        ]
        cursor.executemany("""
        INSERT INTO evidence (case_id, icon, title, category, meta_info, tag, tone, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, evidence_case2)

        # Case 3: Victoria Diamond Vault Heist (Completed / Closed)
        cursor.execute("""
        INSERT INTO cases (case_number, title, crime_type, priority, location, date_time, description, status, progress, prime_suspect)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "CR-2026-0088",
            "Victoria Diamond Vault Heist",
            "Commercial Vault Heist",
            "HIGH",
            "Emerald Plaza, T. Nagar, Chennai",
            "22 Aug 2026 · 23:45–01:10",
            "Safe deposit vault breached through laser bypass; certified gems valued at 4.2 Cr recovered.",
            "COMPLETED",
            100,
            "Marcus Fernandes"
        ))
        case3_id = cursor.lastrowid

        suspects_case3 = [
            (case3_id, "Marcus Fernandes", "MF", "Ex-Vault Technician", "#DC2626", "Prime suspect", "4 evidence links", 1, 1, 1, 1, 1, 0, 0, "DNA on laser glass cutter, confessed under legal deposition"),
            (case3_id, "Rajesh Pillai", "RP", "Night Shift Guard", "#059669", "Eliminated", "No valid links", 0, 0, 0, 0, 0, 1, 0, "Sedated by perpetrator, alibi confirmed by toxicological screen")
        ]
        cursor.executemany("""
        INSERT INTO suspects (case_id, name, initials, role, color, status, links_info, has_motive, has_access, time_window_passed, physical_access_passed, evidence_matched, alibi_verified, contradicts_evidence, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, suspects_case3)

        evidence_case3 = [
            (case3_id, "fingerprint", "DNA swabs on cutter", "Forensic DNA", "Laser emitter casing", "MATCH", "red", "Direct match with offender criminal database"),
            (case3_id, "evidence", "Diamond inventory manifest", "Documentation", "Locker 14-B", "VERIFIED", "green", "All 18 missing gems accounted for upon seizure")
        ]
        cursor.executemany("""
        INSERT INTO evidence (case_id, icon, title, category, meta_info, tag, tone, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, evidence_case3)

        # Case 4: Royal Palms Suspicious Homicide (Pending)
        cursor.execute("""
        INSERT INTO cases (case_number, title, crime_type, priority, location, date_time, description, status, progress, prime_suspect)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "CR-2026-0305",
            "Royal Palms Estate Homicide",
            "Homicide Investigation",
            "CRITICAL",
            "Bungalow 4, Royal Palms, ECR",
            "28 Sep 2026 · 20:00–22:00",
            "Victim found deceased in private study with blunt force trauma. Ongoing timeline reconstruction.",
            "PENDING",
            45,
            None
        ))
        case4_id = cursor.lastrowid

        suspects_case4 = [
            (case4_id, "Harish Varma", "HV", "Primary Heir", "#B45309", "Needs review", "2 evidence links", 1, 1, 1, 1, 0, 0, 0, "Inheritance dispute under litigation"),
            (case4_id, "Sunita Rao", "SR", "Personal Physician", "#047857", "Needs review", "1 evidence link", 0, 1, 1, 1, 0, 1, 0, "Had prescription access; verified clinic log")
        ]
        cursor.executemany("""
        INSERT INTO suspects (case_id, name, initials, role, color, status, links_info, has_motive, has_access, time_window_passed, physical_access_passed, evidence_matched, alibi_verified, contradicts_evidence, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, suspects_case4)

        evidence_case4 = [
            (case4_id, "evidence", "Antique Bronze Paperweight", "Murder weapon", "Study floor", "STORED", "red", "Blood typing consistent with victim"),
            (case4_id, "file", "Coroner Initial Inquest", "Medical Report", "Forensic Lab", "VALIDATED", "green", "Time of death pinpointed between 20:30 and 21:15")
        ]
        cursor.executemany("""
        INSERT INTO evidence (case_id, icon, title, category, meta_info, tag, tone, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, evidence_case4)

        conn.commit()

    conn.close()

if __name__ == "__main__":
    init_db()
    seed_database()
    print(f"Database initialized and seeded at {DB_PATH}")
