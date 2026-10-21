"""
Master Runner Script for Crime Investigation Expert System.
Usage:
  python backend/run_backend.py          -> Starts Flask REST API Server on http://localhost:5000
  python backend/run_backend.py --gui    -> Launches Native Tkinter Desktop Application
"""

import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import init_db, seed_database

if __name__ == "__main__":
    init_db()
    seed_database()

    if "--gui" in sys.argv:
        print("Launching VERITAS Tkinter Desktop Application...")
        import tkinter as tk
        from backend.gui_tkinter import CrimeInvestigationApp
        root = tk.Tk()
        app = CrimeInvestigationApp(root)
        root.mainloop()
    else:
        print("Launching VERITAS Flask REST API Server on http://0.0.0.0:5000...")
        from backend.app import app
        app.run(host="0.0.0.0", port=5000, debug=True)
