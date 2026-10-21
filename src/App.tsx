import { FormEvent, useMemo, useState, useEffect } from "react";

type IconName =
  | "grid"
  | "case"
  | "people"
  | "evidence"
  | "logic"
  | "report"
  | "settings"
  | "search"
  | "bell"
  | "chevron"
  | "pin"
  | "clock"
  | "fingerprint"
  | "camera"
  | "file"
  | "check"
  | "close"
  | "arrow"
  | "download"
  | "plus"
  | "refresh"
  | "back"
  | "logout";

const iconPaths: Record<IconName, React.ReactNode> = {
  grid: <><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>,
  case: <><path d="M9 6V4h6v2" /><rect x="3" y="6" width="18" height="14" rx="2" /><path d="M3 11h18M10 11v2h4v-2" /></>,
  people: <><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></>,
  evidence: <><path d="M9 3h6l1 3h3v15H5V6h3l1-3Z" /><path d="M9 12h6M9 16h4" /></>,
  logic: <><circle cx="6" cy="6" r="3" /><circle cx="18" cy="6" r="3" /><circle cx="12" cy="18" r="3" /><path d="m8.6 7.5 2 7.5m4.8-7.5-2 7.5M9 6h6" /></>,
  report: <><path d="M6 2h9l4 4v16H6z" /><path d="M14 2v5h5M9 12h6M9 16h6" /></>,
  settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-2.83 2.83-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1.03 1.56V21h-4v-.08A1.7 1.7 0 0 0 9 19.36a1.7 1.7 0 0 0-1.88.34l-.06.06-2.83-2.83.06-.06A1.7 1.7 0 0 0 4.63 15 1.7 1.7 0 0 0 3.08 14H3v-4h.08A1.7 1.7 0 0 0 4.64 9a1.7 1.7 0 0 0-.34-1.88l-.06-.06 2.83-2.83.06.06A1.7 1.7 0 0 0 9 4.63h.01A1.7 1.7 0 0 0 10 3.08V3h4v.08A1.7 1.7 0 0 0 15 4.64a1.7 1.7 0 0 0 1.88-.34l.06-.06 2.83 2.83-.06.06A1.7 1.7 0 0 0 19.37 9v.01A1.7 1.7 0 0 0 20.92 10H21v4h-.08A1.7 1.7 0 0 0 19.4 15Z" /></>,
  search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
  bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4" /></>,
  chevron: <path d="m9 18 6-6-6-6" />,
  pin: <><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z" /><circle cx="12" cy="10" r="2.5" /></>,
  clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  fingerprint: <><path d="M12 11a3 3 0 0 1 3 3c0 3-1 5-2 7M9 21c1-2 1-4 1-7a2 2 0 0 1 4 0M5 17c.5-1 .5-2 .5-3a6.5 6.5 0 0 1 13 0c0 2-.3 4-1 6M4 10a9 9 0 0 1 16-2M4 21c1-2 1.5-4 1.5-7" /></>,
  camera: <><path d="M8 5h8l1.5 3H21v11H3V8h3.5L8 5Z" /><circle cx="12" cy="13" r="3.5" /></>,
  file: <><path d="M6 2h9l4 4v16H6z" /><path d="M14 2v5h5" /></>,
  check: <path d="m5 12 4 4L19 6" />,
  close: <path d="m6 6 12 12M18 6 6 18" />,
  arrow: <path d="M5 12h14m-5-5 5 5-5 5" />,
  download: <><path d="M12 3v12m-5-5 5 5 5-5M5 21h14" /></>,
  plus: <path d="M12 5v14M5 12h14" />,
  refresh: <><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" /><path d="M3 21v-5h5" /></>,
  back: <path d="m15 18-6-6 6-6" />,
  logout: <><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></>,
};

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {iconPaths[name]}
    </svg>
  );
}

const API_BASE =
  typeof window !== "undefined" &&
  window.location.hostname &&
  window.location.hostname !== "localhost" &&
  window.location.hostname !== "127.0.0.1"
    ? `http://${window.location.hostname}:5000/api`
    : "http://localhost:5000/api";

interface UserProfile {
  badge_id: string;
  name: string;
  role: string;
  department: string;
}

interface CaseItem {
  id: number;
  case_number: string;
  title: string;
  crime_type: string;
  priority: "CRITICAL" | "HIGH" | "MEDIUM";
  location: string;
  date_time: string;
  description: string;
  status: "PENDING" | "ACTIVE" | "COMPLETED";
  progress: number;
  prime_suspect?: string | null;
  suspect_count?: number;
  evidence_count?: number;
}

export default function App() {
  // Authentication State
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(() => {
    const saved = localStorage.getItem("veritas_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [loginBadge, setLoginBadge] = useState("INV-7042");
  const [loginPassword, setLoginPassword] = useState("investigator123");

  // Navigation State: 'dashboard' | 'investigation'
  const [activeView, setActiveView] = useState<"dashboard" | "investigation">("dashboard");
  const [activeNav, setActiveNav] = useState("Cases");
  const [backendConnected, setBackendConnected] = useState(false);

  // Cases List State
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [caseFilter, setCaseFilter] = useState<"ALL" | "PENDING" | "COMPLETED">("ALL");
  const [searchFilter, setSearchFilter] = useState("");

  // Active Selected Case State for Investigation
  const [activeCase, setActiveCase] = useState<CaseItem | null>(null);
  const [suspects, setSuspects] = useState<any[]>([]);
  const [evidence, setEvidence] = useState<any[]>([]);
  const [activeSuspectId, setActiveSuspectId] = useState<number | null>(null);

  // AI Investigation Results State
  const [investigationTechnique, setInvestigationTechnique] = useState<"BFS" | "DFS">("BFS");
  const [linkAnalysisResult, setLinkAnalysisResult] = useState<any>(null);
  const [filterResult, setFilterResult] = useState<any>(null);
  const [hypothesisResult, setHypothesisResult] = useState<any>(null);
  const [investigationExecuted, setInvestigationExecuted] = useState(false);
  const [loadingAction, setLoadingAction] = useState<string | null>(null);

  // Modals State
  const [reportOpen, setReportOpen] = useState(false);
  const [reportData, setReportData] = useState<any>(null);
  const [createCaseModal, setCreateCaseModal] = useState(false);
  const [addEvidenceModal, setAddEvidenceModal] = useState(false);
  const [addSuspectModal, setAddSuspectModal] = useState(false);

  const FALLBACK_CASES: CaseItem[] = [
    {
      id: 1,
      case_number: "CR-2026-0142",
      title: "The Ashwood Burglary",
      crime_type: "High-Value Residence Burglary",
      priority: "HIGH",
      location: "18 Ashwood Avenue, Chennai",
      date_time: "08 Sep 2026 · 21:30–23:15",
      description: "High-value residence burglary involving forced study window entry and missing bearer bonds.",
      status: "ACTIVE",
      progress: 85,
      prime_suspect: "Arjun Rao",
      suspect_count: 4,
      evidence_count: 4,
    },
    {
      id: 2,
      case_number: "CR-2026-0219",
      title: "Marina Bay Embezzlement",
      crime_type: "Cyber Financial Fraud",
      priority: "CRITICAL",
      location: "Tech Hub Towers, OMR, Chennai",
      date_time: "14 Sep 2026 · 02:15–03:40",
      description: "Unauthorized wire transfer of $1.4M routed through overseas proxy VPN nodes during system maintenance.",
      status: "ACTIVE",
      progress: 85,
      prime_suspect: "Rohan Mehra",
      suspect_count: 3,
      evidence_count: 3,
    },
    {
      id: 3,
      case_number: "CR-2026-0088",
      title: "Victoria Diamond Vault Heist",
      crime_type: "Commercial Vault Heist",
      priority: "HIGH",
      location: "Emerald Plaza, T. Nagar, Chennai",
      date_time: "22 Aug 2026 · 23:45–01:10",
      description: "Safe deposit vault breached through laser bypass; certified gems valued at 4.2 Cr recovered.",
      status: "COMPLETED",
      progress: 100,
      prime_suspect: "Marcus Fernandes",
      suspect_count: 2,
      evidence_count: 2,
    },
    {
      id: 4,
      case_number: "CR-2026-0305",
      title: "Royal Palms Estate Homicide",
      crime_type: "Homicide Investigation",
      priority: "CRITICAL",
      location: "Bungalow 4, Royal Palms, ECR",
      date_time: "28 Sep 2026 · 20:00–22:00",
      description: "Victim found deceased in private study with blunt force trauma. Ongoing timeline reconstruction.",
      status: "PENDING",
      progress: 45,
      prime_suspect: null,
      suspect_count: 2,
      evidence_count: 2,
    },
  ];

  // Initial load
  useEffect(() => {
    loadCases();
    fetch(`${API_BASE}/health`)
      .then((res) => res.json())
      .then((h) => {
        if (h.status === "online") {
          setBackendConnected(true);
          loadCases();
        }
      })
      .catch(() => setBackendConnected(false));
  }, []);

  const loadCases = () => {
    fetch(`${API_BASE}/cases`)
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setCases(data);
          setBackendConnected(true);
          if (!activeCase) {
            setActiveCase(data[0]);
          }
        } else {
          setCases((prev) => (prev.length > 0 ? prev : FALLBACK_CASES));
        }
      })
      .catch(() => {
        setCases((prev) => (prev.length > 0 ? prev : FALLBACK_CASES));
      });
  };

  const handleLogin = (userToLogin?: UserProfile) => {
    if (userToLogin) {
      setCurrentUser(userToLogin);
      localStorage.setItem("veritas_user", JSON.stringify(userToLogin));
      loadCases();
      return;
    }
    fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ badge_id: loginBadge, password: loginPassword }),
    })
      .then((r) => r.json())
      .then((res) => {
        const u = res.user || {
          badge_id: loginBadge,
          name: "Inspector K. Rao",
          role: "Lead Forensic Investigator",
          department: "Cyber Crime & Special Operations",
        };
        setCurrentUser(u);
        localStorage.setItem("veritas_user", JSON.stringify(u));
        loadCases();
      })
      .catch(() => {
        const fallback = {
          badge_id: loginBadge,
          name: "Inspector K. Rao",
          role: "Lead Forensic Investigator",
          department: "Cyber Crime & Special Operations",
        };
        setCurrentUser(fallback);
        localStorage.setItem("veritas_user", JSON.stringify(fallback));
        loadCases();
      });
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem("veritas_user");
    setActiveView("dashboard");
  };

  const openCaseInvestigation = (c: CaseItem) => {
    setActiveCase(c);
    setActiveView("investigation");
    loadCaseDetails(c.id);
  };

  const loadCaseDetails = (caseId: number) => {
    setLoadingAction("load_case");
    fetch(`${API_BASE}/cases/${caseId}`)
      .then((r) => r.json())
      .then((c) => {
        setActiveCase(c);
        setSuspects(c.suspects || []);
        setEvidence(c.evidence || []);
        if (c.suspects && c.suspects.length > 0) {
          setActiveSuspectId(c.suspects[0].id);
        }
        setInvestigationExecuted(false);
        setHypothesisResult(null);

        // Fetch link analysis for this case
        fetch(`${API_BASE}/search?case_id=${caseId}&algorithm=${investigationTechnique}`)
          .then((r) => r.json())
          .then((res) => setLinkAnalysisResult(res))
          .catch(() => {});

        // Fetch CSP filter for this case
        fetch(`${API_BASE}/csp-eliminate?case_id=${caseId}`, { method: "POST" })
          .then((r) => r.json())
          .then((res) => setFilterResult(res))
          .catch(() => {});

        setLoadingAction(null);
      })
      .catch(() => setLoadingAction(null));
  };

  // Re-run Link Analysis when technique changes
  const switchTechnique = (tech: "BFS" | "DFS") => {
    setInvestigationTechnique(tech);
    if (!activeCase) return;
    fetch(`${API_BASE}/search?case_id=${activeCase.id}&algorithm=${tech}`)
      .then((r) => r.json())
      .then((res) => setLinkAnalysisResult(res))
      .catch(() => {});
  };

  // Run the core AI investigation workflow for the selected case
  const executeCaseInvestigation = () => {
    if (!activeCase) return;
    setLoadingAction("investigating");
    fetch(`${API_BASE}/infer?case_id=${activeCase.id}`, { method: "POST" })
      .then((r) => r.json())
      .then((res) => {
        setHypothesisResult(res);
        setInvestigationExecuted(true);
        // Refresh case status and progress
        loadCases();
        if (activeCase) {
          setActiveCase({
            ...activeCase,
            prime_suspect: res.prime_suspect_identified,
            progress: 85,
            status: "ACTIVE",
          });
        }
        setLoadingAction(null);
      })
      .catch(() => {
        setInvestigationExecuted(true);
        setLoadingAction(null);
      });
  };

  const toggleCaseStatus = (newStatus: "PENDING" | "ACTIVE" | "COMPLETED") => {
    if (!activeCase) return;
    const newProgress = newStatus === "COMPLETED" ? 100 : newStatus === "ACTIVE" ? 85 : 30;
    fetch(`${API_BASE}/cases/${activeCase.id}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus, progress: newProgress }),
    })
      .then((r) => r.json())
      .then((updated) => {
        setActiveCase(updated);
        loadCases();
      })
      .catch(() => {});
  };

  const handleOpenReport = () => {
    setReportOpen(true);
    const caseId = activeCase ? activeCase.id : 1;
    fetch(`${API_BASE}/report?case_id=${caseId}`)
      .then((r) => r.json())
      .then((rep) => setReportData(rep))
      .catch(() => {});
  };

  const handleCreateCase = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const payload = {
      title: String(data.get("title")),
      crime_type: String(data.get("crime_type")),
      priority: String(data.get("priority")),
      location: String(data.get("location")),
      date_time: String(data.get("date_time")),
      description: String(data.get("description")),
    };

    fetch(`${API_BASE}/cases`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((r) => r.json())
      .then((newC) => {
        loadCases();
        setCreateCaseModal(false);
        openCaseInvestigation(newC);
      })
      .catch(() => setCreateCaseModal(false));
  };

  const handleAddEvidence = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!activeCase) return;
    const data = new FormData(e.currentTarget);
    const payload = {
      case_id: activeCase.id,
      title: String(data.get("title")),
      category: String(data.get("category")),
      details: String(data.get("details")),
    };

    fetch(`${API_BASE}/evidence`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((r) => r.json())
      .then(() => {
        loadCaseDetails(activeCase.id);
        setAddEvidenceModal(false);
      })
      .catch(() => setAddEvidenceModal(false));
  };

  const handleAddSuspect = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!activeCase) return;
    const data = new FormData(e.currentTarget);
    const payload = {
      case_id: activeCase.id,
      name: String(data.get("name")),
      role: String(data.get("role")),
      notes: String(data.get("notes")),
    };

    fetch(`${API_BASE}/suspects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((r) => r.json())
      .then(() => {
        loadCaseDetails(activeCase.id);
        setAddSuspectModal(false);
      })
      .catch(() => setAddSuspectModal(false));
  };

  // Filtered cases for dashboard
  const displayedCases = useMemo(() => {
    return cases.filter((c) => {
      const matchesSearch =
        c.title.toLowerCase().includes(searchFilter.toLowerCase()) ||
        c.location.toLowerCase().includes(searchFilter.toLowerCase()) ||
        c.case_number.toLowerCase().includes(searchFilter.toLowerCase());
      if (caseFilter === "ALL") return matchesSearch;
      if (caseFilter === "PENDING") return matchesSearch && (c.status === "PENDING" || c.status === "ACTIVE");
      if (caseFilter === "COMPLETED") return matchesSearch && c.status === "COMPLETED";
      return matchesSearch;
    });
  }, [cases, caseFilter, searchFilter]);

  // Selected suspect details
  const selectedSuspect = suspects.find((s) => s.id === activeSuspectId) ?? suspects[0];

  // ==========================================
  // VIEW 1: AUTHENTICATION / LOGIN SCREEN
  // ==========================================
  if (!currentUser) {
    return (
      <div className="login-screen">
        <div className="login-box">
          <div className="login-emblem">
            <div className="brand-mark">
              <span /><span /><span /><span />
            </div>
            <div>
              <h1>VERITAS</h1>
              <span>CRIME INVESTIGATION AI</span>
            </div>
          </div>

          <p style={{ margin: "0 0 16px", fontSize: "11px", color: "#95a59e", lineHeight: 1.6 }}>
            Authorized law enforcement decision-support environment. Sign in with your official investigator badge or choose a registered profile below.
          </p>

          <div className="login-quick-profiles">
            <p>One-Click Investigator Access (Kaggle Dataset Credentials)</p>
            <button
              className="quick-profile-btn"
              onClick={() =>
                handleLogin({
                  badge_id: "INV-7042",
                  name: "Inspector K. Rao",
                  role: "Lead Forensic Investigator",
                  department: "Cyber Crime & Special Operations",
                })
              }
            >
              <div>
                <strong>Inspector K. Rao</strong> — <small>Lead Investigator</small>
              </div>
              <span>INV-7042</span>
            </button>
            <button
              className="quick-profile-btn"
              onClick={() =>
                handleLogin({
                  badge_id: "CSI-3081",
                  name: "Detective Priya Nair",
                  role: "Forensic Logic Specialist",
                  department: "Digital Forensics & Ballistics",
                })
              }
            >
              <div>
                <strong>Detective Priya Nair</strong> — <small>Forensics & CSP Lead</small>
              </div>
              <span>CSI-3081</span>
            </button>
            <button
              className="quick-profile-btn"
              onClick={() =>
                handleLogin({
                  badge_id: "DIR-1001",
                  name: "Commissioner S. Varma",
                  role: "Chief of Intelligence",
                  department: "Directorate of Criminal Investigation",
                })
              }
            >
              <div>
                <strong>Commissioner S. Varma</strong> — <small>Chief Directorate</small>
              </div>
              <span>DIR-1001</span>
            </button>
          </div>

          <div className="login-divider">OR ENTER OFFICIAL CREDENTIALS</div>

          <form
            className="login-form"
            onSubmit={(e) => {
              e.preventDefault();
              handleLogin();
            }}
          >
            <label>
              Investigator Badge ID
              <input value={loginBadge} onChange={(e) => setLoginBadge(e.target.value)} required />
            </label>
            <label>
              Security Passcode
              <input
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                required
              />
            </label>
            <button type="submit" className="login-submit-btn">
              Authenticate & Access Investigation Terminal →
            </button>
          </form>

          <div style={{ marginTop: "16px", textAlign: "center", fontSize: "9px", color: "#64776e", letterSpacing: "0.08em", textTransform: "uppercase" }}>
            Veritas Crime Investigation AI · Authorized Law Enforcement Terminal
          </div>
        </div>
      </div>
    );
  }

  // ==========================================
  // VIEW 2: MAIN DASHBOARD & INVESTIGATION APP
  // ==========================================
  return (
    <div className="app-shell">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><span /><span /><span /><span /></div>
          <div><strong>Veritas</strong><small>INVESTIGATION AI</small></div>
        </div>

        <nav className="main-nav" aria-label="Main navigation">
          <p>WORKSPACE</p>
          {[
            ["Cases", "grid"],
            ["Investigation", "case"],
            ["Evidence Locker", "evidence"],
            ["Suspect Lineup", "people"],
            ["Case Docket", "report"],
          ].map(([label, icon]) => (
            <button
              key={label}
              className={
                (activeView === "dashboard" && label === "Cases") ||
                (activeView === "investigation" && label === activeNav)
                  ? "active"
                  : ""
              }
              onClick={() => {
                setActiveNav(label);
                if (label === "Cases") {
                  setActiveView("dashboard");
                } else if (label === "Case Docket") {
                  handleOpenReport();
                } else {
                  setActiveView("investigation");
                }
              }}
            >
              <Icon name={icon as IconName} />
              <span>{label}</span>
              {label === "Cases" && <b>{cases.length}</b>}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <button
            onClick={() => {
              fetch(`${API_BASE}/seed`, { method: "POST" })
                .then(() => loadCases())
                .catch(() => {});
            }}
            title="Reset Kaggle Crime Dataset"
          >
            <Icon name="refresh" />
            <span>Reset Dataset</span>
          </button>
          <div className="user-card">
            <div className="avatar">
              {currentUser.name
                .split(" ")
                .map((n) => n[0])
                .join("")
                .slice(0, 2)}
            </div>
            <div>
              <strong>{currentUser.name}</strong>
              <small>{currentUser.role}</small>
            </div>
            <button onClick={handleLogout} title="Log Out" aria-label="Log Out">
              <Icon name="logout" size={14} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main>
        <header className="topbar">
          <div className="breadcrumbs">
            <button
              onClick={() => setActiveView("dashboard")}
              style={{ background: "transparent", border: 0, padding: 0, color: "#6b7a74", fontWeight: 600, display: "flex", alignItems: "center", gap: "4px" }}
            >
              Criminal Docket
            </button>
            <Icon name="chevron" size={14} />
            <strong>
              {activeView === "dashboard"
                ? "Case Records Overview"
                : `${activeCase?.case_number || "CR-2026-0142"} · ${activeCase?.title || ""}`}
            </strong>
          </div>
          <div className="top-actions">
            <label className="global-search">
              <Icon name="search" size={17} />
              <input
                aria-label="Global search"
                placeholder="Search docket or crime scene..."
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
              />
            </label>
            <button className="primary small" onClick={() => setCreateCaseModal(true)}>
              <Icon name="plus" size={15} /> Register New Case
            </button>
          </div>
        </header>

        <div className="workspace">
          {/* ==================================================== */}
          {/* SUB-VIEW A: CASES DASHBOARD (PENDING / COMPLETED)     */}
          {/* ==================================================== */}
          {activeView === "dashboard" && (
            <div>
              <div className="dashboard-top">
                <div className="dashboard-title">
                  <h1>Investigation Docket & Case Index</h1>
                  <p>
                    Curated law enforcement registry. Access pending cases, track investigation progress, or register new incident reports.
                  </p>
                </div>
                <div className="dashboard-actions">
                  <span
                    style={{
                      color: backendConnected ? "#15803d" : "#b45309",
                      fontWeight: 700,
                      fontSize: "0.75rem",
                      padding: "4px 10px",
                      background: backendConnected ? "#dcfce7" : "#fef3c7",
                      borderRadius: "6px",
                      border: "1px solid rgba(0,0,0,0.05)",
                    }}
                  >
                    {backendConnected ? "🟢 SQLite KNOWLEDGE BASE ONLINE" : "🟡 STANDALONE MODE"}
                  </span>
                </div>
              </div>

              {/* Metrics Summary Row */}
              <div className="metrics-row">
                <div className="metric-tile">
                  <span>Total Docketed Cases</span>
                  <strong>{String(cases.length).padStart(2, "0")}</strong>
                  <small>Recorded in police knowledge base</small>
                </div>
                <div className="metric-tile">
                  <span>Active Investigations</span>
                  <strong>
                    {String(cases.filter((c) => c.status === "ACTIVE").length).padStart(2, "0")}
                  </strong>
                  <small>Under multi-module AI analysis</small>
                </div>
                <div className="metric-tile">
                  <span>Pending Analysis</span>
                  <strong>
                    {String(cases.filter((c) => c.status === "PENDING").length).padStart(2, "0")}
                  </strong>
                  <small>Awaiting evidence & alibi filtering</small>
                </div>
                <div className="metric-tile">
                  <span>Solved & Closed</span>
                  <strong style={{ color: "#3730a3" }}>
                    {String(cases.filter((c) => c.status === "COMPLETED").length).padStart(2, "0")}
                  </strong>
                  <small>Final forensic docket submitted</small>
                </div>
              </div>

              {/* Case Filters Bar */}
              <div className="case-filter-bar">
                <div className="filter-tabs">
                  <button
                    className={`filter-tab ${caseFilter === "ALL" ? "active" : ""}`}
                    onClick={() => setCaseFilter("ALL")}
                  >
                    All Cases ({cases.length})
                  </button>
                  <button
                    className={`filter-tab ${caseFilter === "PENDING" ? "active" : ""}`}
                    onClick={() => setCaseFilter("PENDING")}
                  >
                    Pending & Active ({cases.filter((c) => c.status !== "COMPLETED").length})
                  </button>
                  <button
                    className={`filter-tab ${caseFilter === "COMPLETED" ? "active" : ""}`}
                    onClick={() => setCaseFilter("COMPLETED")}
                  >
                    Completed / Solved ({cases.filter((c) => c.status === "COMPLETED").length})
                  </button>
                </div>
              </div>

              {/* Cases Grid */}
              <div className="cases-grid">
                {displayedCases.map((c) => (
                  <div className="case-card" key={c.id}>
                    <div className="case-card-header">
                      <span className="case-num-badge">{c.case_number}</span>
                      <div className="case-badge-group">
                        <span className={`priority-pill ${c.priority}`}>{c.priority}</span>
                        <span className={`status-pill ${c.status}`}>{c.status}</span>
                      </div>
                    </div>

                    <h2>{c.title}</h2>
                    <span className="case-type-tag">{c.crime_type}</span>
                    <p className="case-card-desc">{c.description}</p>

                    <div className="case-card-meta">
                      <span><Icon name="pin" size={13} /> {c.location}</span>
                      <span><Icon name="clock" size={13} /> {c.date_time}</span>
                    </div>

                    <div className="case-progress-wrap">
                      <div className="case-progress-info">
                        <span>Investigation Progress</span>
                        <strong>{c.progress}%</strong>
                      </div>
                      <div className="case-progress-bar">
                        <div className="case-progress-fill" style={{ width: `${c.progress}%` }} />
                      </div>
                    </div>

                    <div className="case-card-footer">
                      <div className="case-counts">
                        <span><strong>{c.suspect_count || 0}</strong> Suspects</span>
                        <span><strong>{c.evidence_count || 0}</strong> Evidence Items</span>
                      </div>
                      <button className="investigate-btn" onClick={() => openCaseInvestigation(c)}>
                        Conduct Investigation <Icon name="arrow" size={13} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ==================================================== */}
          {/* SUB-VIEW B: DETAILED INVESTIGATION VIEW              */}
          {/* ==================================================== */}
          {activeView === "investigation" && activeCase && (
            <div>
              {/* Back Bar */}
              <div className="back-nav-bar">
                <button className="back-btn" onClick={() => setActiveView("dashboard")}>
                  <Icon name="back" size={14} /> Back to Docket Dashboard
                </button>
                <div style={{ display: "flex", gap: "8px" }}>
                  <button
                    className="secondary"
                    style={{ fontSize: "10px", padding: "6px 12px" }}
                    onClick={() =>
                      toggleCaseStatus(activeCase.status === "COMPLETED" ? "ACTIVE" : "COMPLETED")
                    }
                  >
                    {activeCase.status === "COMPLETED"
                      ? "Re-open Case"
                      : "Mark Case as Solved & Completed"}
                  </button>
                  <button
                    className="primary"
                    style={{ fontSize: "10px", padding: "6px 14px" }}
                    onClick={handleOpenReport}
                  >
                    <Icon name="report" size={14} /> View Case Docket
                  </button>
                </div>
              </div>

              {/* Case Dossier Header */}
              <section className="case-heading" id="case-overview">
                <div>
                  <div className="eyebrow-row">
                    <span className="status-dot">CASE {activeCase.case_number}</span>
                    <span className={`status-pill ${activeCase.status}`}>{activeCase.status}</span>
                    <span className={`priority-pill ${activeCase.priority}`}>
                      PRIORITY: {activeCase.priority}
                    </span>
                    {activeCase.prime_suspect && (
                      <span style={{ color: "#b91c1c", fontWeight: 700, fontSize: "0.8rem", background: "#fee2e2", padding: "2px 8px", borderRadius: "4px" }}>
                        PRIME SUSPECT IDENTIFIED: {activeCase.prime_suspect}
                      </span>
                    )}
                  </div>
                  <h1>{activeCase.title}</h1>
                  <p className="case-meta">
                    <span><Icon name="pin" size={15} /> {activeCase.location}</span>
                    <span><Icon name="clock" size={15} /> {activeCase.date_time}</span>
                  </p>
                  <p style={{ margin: "8px 0 0", fontSize: "10px", color: "#5d6d66", maxWidth: "700px" }}>
                    {activeCase.description}
                  </p>
                </div>
                <div className="case-stats">
                  <div>
                    <strong>{String(suspects.length).padStart(2, "0")}</strong>
                    <span>Suspects Lineup</span>
                  </div>
                  <div>
                    <strong>{String(evidence.length).padStart(2, "0")}</strong>
                    <span>Forensic Evidence</span>
                  </div>
                  <div>
                    <strong style={{ color: "#047857" }}>{activeCase.progress}%</strong>
                    <span>Investigation Solved</span>
                  </div>
                </div>
              </section>

              {/* Workflow Stepper Bar (Investigation Perspective) */}
              <section className="workflow-guide" id="workflow">
                <div className="workflow-title">
                  <span>Structured Criminal Investigation Lifecycle</span>
                  <p>
                    Follow the five-stage investigative sequence. Intelligent AI reasoning works automatically beneath each stage.
                  </p>
                </div>
                <div className="workflow-steps">
                  {[
                    ["1", "Crime Scene Catalog", "Evidence Registry"],
                    ["2", "Network Link Analysis", "Perimeter / Chain Sweep"],
                    ["3", "Opportunity & Alibi Filter", "Timeline & Access Checks"],
                    ["4", "Hypothesis & Legal Proof", "Forward / Backward Reasoning"],
                    ["5", "Official Docket Summary", "Warrant & Prosecutorial Report"],
                  ].map(([number, label, detail], index) => (
                    <div className="workflow-step" key={label}>
                      <span>{number}</span>
                      <div>
                        <strong>{label}</strong>
                        <small>{detail}</small>
                      </div>
                      {index < 4 && <Icon name="chevron" size={14} />}
                    </div>
                  ))}
                </div>
              </section>

              {/* 2-Column Investigation Workboard */}
              <div className="content-grid">
                {/* Left Column: Evidence & Link Analysis & Alibi Filter */}
                <div className="left-column">
                  {/* Module 1: Evidence Catalog */}
                  <section className="panel evidence-panel" id="evidence">
                    <div className="panel-heading">
                      <div>
                        <span className="step">01</span>
                        <div>
                          <h2>Crime Scene Evidence Catalog</h2>
                          <p>Forensic artifacts, ballistic evidence, digital logs, and statements</p>
                        </div>
                      </div>
                      <button className="text-button" onClick={() => setAddEvidenceModal(true)}>
                        <Icon name="plus" size={14} /> Add Evidence
                      </button>
                    </div>
                    <div className="evidence-list">
                      {evidence.map((item) => (
                        <div className="evidence-item" key={item.id || item.title}>
                          <span className="evidence-icon">
                            <Icon
                              name={
                                item.category?.toLowerCase().includes("cctv")
                                  ? "camera"
                                  : item.category?.toLowerCase().includes("fingerprint") || item.category?.toLowerCase().includes("dna")
                                  ? "fingerprint"
                                  : item.category?.toLowerCase().includes("digital") || item.category?.toLowerCase().includes("statement")
                                  ? "file"
                                  : "evidence"
                              }
                              size={20}
                            />
                          </span>
                          <span>
                            <strong>{item.title}</strong>
                            <small>{item.meta_info || item.details}</small>
                          </span>
                          <em className={item.tone || "green"}>{item.tag || "LOGGED"}</em>
                        </div>
                      ))}
                    </div>
                    <div className="data-flow">
                      <div>
                        <span><Icon name="check" size={13} /></span>
                        <p><strong>Chain of Custody</strong>Evidence logged into forensic SQLite database.</p>
                      </div>
                      <Icon name="arrow" size={15} />
                      <div>
                        <span><Icon name="logic" size={13} /></span>
                        <p><strong>Predicate Transformation</strong>Converted to facts for legal rule processing.</p>
                      </div>
                      <Icon name="arrow" size={15} />
                      <div>
                        <span><Icon name="evidence" size={13} /></span>
                        <p><strong>Graph Node Binding</strong>Linked to suspects and crime scene root.</p>
                      </div>
                    </div>
                  </section>

                  {/* Module 2: Relationship & Network Link Analysis */}
                  <section className="panel search-panel">
                    <div className="panel-heading">
                      <div>
                        <span className="step">02</span>
                        <div>
                          <h2>Relationship & Network Link Analysis</h2>
                          <p>
                            Examines connections between crime scene, suspects, and recovered evidence
                          </p>
                        </div>
                      </div>
                      <div className="algorithm-toggle">
                        <button
                          onClick={() => switchTechnique("BFS")}
                          className={investigationTechnique === "BFS" ? "active" : ""}
                          title="Perimeter Sweep (BFS)"
                        >
                          SWEEP
                        </button>
                        <button
                          onClick={() => switchTechnique("DFS")}
                          className={investigationTechnique === "DFS" ? "active" : ""}
                          title="Deep Thread (DFS)"
                        >
                          THREAD
                        </button>
                      </div>
                    </div>
                    <div className="search-explainer">
                      <div className="graph">
                        <span className="node root">C</span>
                        <i className="line l1" /><i className="line l2" /><i className="line l3" />
                        <span className={`node n1 ${investigationTechnique === "BFS" ? "found" : ""}`}>
                          {suspects[0]?.initials || "S1"}
                        </span>
                        <span className="node n2">{suspects[1]?.initials || "S2"}</span>
                        <span className="node n3">{suspects[2]?.initials || "S3"}</span>
                      </div>
                      <div>
                        <span className="logic-label">
                          {investigationTechnique === "BFS"
                            ? "PERIMETER & RELATIONSHIP SWEEP (BFS)"
                            : "DEEP EVIDENCE THREAD (DFS)"}
                        </span>
                        <h3>
                          {investigationTechnique === "BFS"
                            ? "Exploring immediate crime scene contacts first"
                            : "Pursuing each suspect's full evidence chain"}
                        </h3>
                        <p>
                          {linkAnalysisResult?.explanation ||
                            "Analyzing suspect-to-evidence network links to map viable perpetrators."}
                        </p>
                        {linkAnalysisResult?.traversal_order && (
                          <div style={{ marginTop: "8px", fontSize: "0.75rem", color: "#64748b", fontFamily: "monospace" }}>
                            <strong>Investigative Traversal:</strong>{" "}
                            {linkAnalysisResult.traversal_order.slice(0, 6).join(" ➔ ")}...
                          </div>
                        )}
                      </div>
                    </div>
                  </section>

                  {/* Module 3: Forensic Opportunity & Alibi Filter */}
                  <section className="panel constraint-panel">
                    <div className="panel-heading">
                      <div>
                        <span className="step">03</span>
                        <div>
                          <h2>Forensic Opportunity & Alibi Filter</h2>
                          <p>Systematic elimination of candidates using timeline and opportunity constraints</p>
                        </div>
                      </div>
                      <span className="validated">
                        <Icon name="check" size={14} />{" "}
                        {filterResult ? `${filterResult.total_constraint_checks || 8} checks conducted` : "Constraint Filter Ready"}
                      </span>
                    </div>
                    <div className="constraint-row">
                      <div>
                        <span className="rule-icon"><Icon name="clock" /></span>
                        <strong>Timeline & Crime Window Proximity</strong>
                        <small>Presence near scene between estimated incident window</small>
                      </div>
                      <span className="pass"><Icon name="check" size={15} /> Evaluated</span>
                    </div>
                    <div className="constraint-row">
                      <div>
                        <span className="rule-icon"><Icon name="pin" /></span>
                        <strong>Physical Access & Route Feasibility</strong>
                        <small>Viable entry points, keys, codes, or forced access opportunities</small>
                      </div>
                      <span className="pass"><Icon name="check" size={15} /> Evaluated</span>
                    </div>
                    <div className="constraint-row">
                      <div>
                        <span className="rule-icon"><Icon name="fingerprint" /></span>
                        <strong>Alibi Credibility & Evidence Consistency</strong>
                        <small>Eliminates individuals with verified alibis and no forensic link</small>
                      </div>
                      <span className="fail">
                        <Icon name="close" size={15} />{" "}
                        {filterResult ? `Eliminated ${filterResult.eliminated_count}` : "Eliminated candidates"}
                      </span>
                    </div>
                  </section>
                </div>

                {/* Right Column: Suspect Lineup & Hypothesis Legal Proof */}
                <div className="right-column">
                  {/* Suspect Lineup */}
                  <section className="panel suspect-panel" id="suspects">
                    <div className="panel-heading compact">
                      <div>
                        <h2>Suspect Lineup & Person of Interest Index</h2>
                        <p>Subjected to link analysis and opportunity filter</p>
                      </div>
                      <button className="icon-button subtle" onClick={() => setAddSuspectModal(true)} title="Add Suspect">
                        <Icon name="plus" size={17} />
                      </button>
                    </div>
                    <div className="suspect-list">
                      {suspects.map((s, index) => (
                        <button
                          key={s.id}
                          className={`suspect ${activeSuspectId === s.id ? "active" : ""}`}
                          onClick={() => setActiveSuspectId(s.id)}
                        >
                          <span className="rank">0{index + 1}</span>
                          <span className="suspect-avatar" style={{ background: s.color || "#526D63" }}>
                            {s.initials}
                          </span>
                          <span className="suspect-name">
                            <strong>{s.name}</strong>
                            <small>{s.role}</small>
                          </span>
                          <span className={`suspect-result ${s.status === "Eliminated" ? "eliminated" : ""}`}>
                            {s.status}
                          </span>
                        </button>
                      ))}
                    </div>
                  </section>

                  {/* Module 4: Hypothesis & Legal Proof Engine */}
                  {selectedSuspect && (
                    <section
                      className={`panel inference-panel ${investigationExecuted ? "analysed" : ""}`}
                      id="knowledge-base"
                    >
                      <div className="inference-top">
                        <span className="logic-icon"><Icon name="logic" size={22} /></span>
                        <div>
                          <span>INVESTIGATIVE HYPOTHESIS & LEGAL PROOF</span>
                          <h2>{selectedSuspect.name}</h2>
                        </div>
                        <span className={`confidence ${selectedSuspect.status === "Prime suspect" ? "critical" : ""}`}>
                          {selectedSuspect.status}
                        </span>
                      </div>

                      {/* Inductive Evidence Assembly (Forward Reasoning) */}
                      <div className="reasoning">
                        <h3>Inductive Evidence Assembly (Forward Reasoning)</h3>
                        <div className="reason-step">
                          <span><Icon name="check" size={13} /></span>
                          <div>
                            <small>MOTIVE RECORD</small>
                            <strong>{selectedSuspect.has_motive ? "Financial / Personal motive verified" : "No recorded motive"}</strong>
                          </div>
                        </div>
                        <div className="reason-step">
                          <span><Icon name="check" size={13} /></span>
                          <div>
                            <small>SCENE ACCESS</small>
                            <strong>{selectedSuspect.has_access ? "Viable access opportunity established" : "Physical access unverified"}</strong>
                          </div>
                        </div>
                        <div className="reason-step">
                          <span><Icon name="check" size={13} /></span>
                          <div>
                            <small>FORENSIC MATCH</small>
                            <strong>{selectedSuspect.evidence_matched ? "Physical/Digital evidence match confirmed" : "No direct evidence match"}</strong>
                          </div>
                        </div>
                      </div>

                      {/* Prosecution Proof & Verification (Backward Reasoning) */}
                      {hypothesisResult?.backward_reasoning?.proof_steps && (
                        <div style={{ margin: "10px 17px", padding: "10px", background: "rgba(255,255,255,0.03)", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.06)" }}>
                          <small style={{ color: "#e2e8f0", fontWeight: 700, letterSpacing: "0.08em", display: "block", marginBottom: "6px" }}>
                            PROSECUTION PROOF & VERIFICATION STEPS
                          </small>
                          <div style={{ display: "grid", gap: "4px" }}>
                            {hypothesisResult.backward_reasoning.proof_steps.slice(0, 4).map((st: any) => (
                              <div key={st.step} style={{ fontSize: "0.75rem", color: st.satisfied ? "#86efac" : "#fca5a5", display: "flex", gap: "6px" }}>
                                <span>Step {st.step}:</span> <span>{st.explanation}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="backward-check">
                        <span><Icon name="search" size={16} /></span>
                        <div>
                          <strong>Legal Hypothesis Justification</strong>
                          <p>
                            Tests whether {selectedSuspect.name} satisfies all prosecutorial criteria required for criminal indictment.
                          </p>
                        </div>
                      </div>

                      <div className="predicate">
                        <span>PREDICATE LOGIC LEGAL FORMULATION</span>
                        <code>
                          {hypothesisResult?.forward_reasoning?.legal_rule_applied ||
                            "motive(x) ∧ access(x) ∧ evidence_match(x) → prime_suspect(x)"}
                        </code>
                      </div>

                      {/* Prominent Action Button: Run Investigation */}
                      <button
                        className="primary full"
                        onClick={executeCaseInvestigation}
                        disabled={loadingAction === "investigating"}
                      >
                        {loadingAction === "investigating"
                          ? "Executing Multi-Algorithm Investigation..."
                          : investigationExecuted
                          ? "Investigation Analysis Complete (Re-run)"
                          : "Execute AI Investigation & Establish Prime Suspect"}
                        <Icon name={investigationExecuted ? "check" : "arrow"} size={17} />
                      </button>
                    </section>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* ==================================================== */}
      {/* MODAL 1: OFFICIAL FORENSIC REPORT / CASE DOCKET      */}
      {/* ==================================================== */}
      {reportOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setReportOpen(false)}>
          <section className="report-modal" role="dialog" aria-modal="true" onMouseDown={(e) => e.stopPropagation()}>
            <div className="report-header">
              <div className="report-seal"><Icon name="report" size={26} /></div>
              <div className="report-titles">
                <span className="report-eyebrow">OFFICIAL LAW ENFORCEMENT DOSSIER</span>
                <h1 className="report-main-title">VERITAS CRIME INVESTIGATION AI</h1>
                <p className="report-subtitle">Forensic Investigation Docket & Evidentiary Proof</p>
              </div>
              <button className="icon-button no-print" onClick={() => setReportOpen(false)} aria-label="Close report">
                <Icon name="close" />
              </button>
            </div>

            <div className="report-body">
              {/* Official Case Meta Banner */}
              <div className="docket-meta-grid">
                <div className="docket-meta-item">
                  <span>CASE REFERENCE</span>
                  <strong>{reportData?.case_summary?.case_number || activeCase?.case_number || "CR-2026-0142"}</strong>
                </div>
                <div className="docket-meta-item">
                  <span>INCIDENT CLASSIFICATION</span>
                  <strong>{activeCase?.crime_type || "Criminal Investigation"}</strong>
                </div>
                <div className="docket-meta-item">
                  <span>CRIME SCENE LOCATION</span>
                  <strong>{activeCase?.location || "Designated Crime Scene"}</strong>
                </div>
                <div className="docket-meta-item">
                  <span>INCIDENT DATE & TIME</span>
                  <strong>{activeCase?.date_time || "Recorded Incident Timeline"}</strong>
                </div>
                <div className="docket-meta-item">
                  <span>LEAD INVESTIGATOR</span>
                  <strong>{currentUser?.name || "Inspector K. Rao"} ({currentUser?.badge_id || "INV-7042"})</strong>
                </div>
                <div className="docket-meta-item">
                  <span>DOCKET GENERATED</span>
                  <strong>{reportData?.generated_at || new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" })}</strong>
                </div>
              </div>

              {/* Case Title Headline */}
              <div className="docket-case-headline">
                <span className="docket-tag">CASE DOSSIER</span>
                <h2>{activeCase?.title || "Active Forensic Case"}</h2>
                <p>{activeCase?.description || "Forensic investigation proceedings and physical evidence assembly."}</p>
              </div>

              {/* Primary Investigative Finding */}
              <div className="docket-prime-finding">
                <div className="finding-badge">PRIME SUSPECT IDENTIFIED</div>
                <h3>
                  {reportData?.findings?.prime_suspect || activeCase?.prime_suspect || "Under Forensic Evaluation"}
                </h3>
                <p>
                  Probable cause established through convergence of physical evidence matching, verified opportunity window, physical ingress validation, and inductive legal reasoning.
                </p>
              </div>

              {/* Step-by-Step AI & Forensic Methodology */}
              <h3 className="docket-section-title">Forensic Methodology & Legal Evidence Assembly</h3>
              <div className="report-findings">
                <div>
                  <span>01</span>
                  <p>
                    <strong>Relationship & Network Link Analysis</strong>
                    {reportData?.findings?.search_module_summary ||
                      `Traced relationship links from root crime scene and mapped persons of interest using graph traversal.`}
                  </p>
                </div>
                <div>
                  <span>02</span>
                  <p>
                    <strong>Forensic Opportunity & Constraint Filter (CSP)</strong>
                    {reportData?.findings?.csp_backtracking_summary ||
                      `Cross-examined timeline feasibility, viable scene access routes, and validated alibis. Eliminated candidates with verifiable conflicting timelines.`}
                  </p>
                </div>
                <div>
                  <span>03</span>
                  <p>
                    <strong>Inductive Hypothesis Formulation & Backward Verification</strong>
                    {reportData?.findings?.inference_engine_summary ||
                      `Formulated prosecutorial hypothesis from physical evidence and verified all predicate conditions through backward chaining inference.`}
                  </p>
                </div>
                <div>
                  <span>04</span>
                  <p>
                    <strong>Conclusive Evidentiary Synthesis</strong>
                    Corroborated all physical recoveries, timeline verifications, and digital logs into a verified prosecutorial chain of custody.
                  </p>
                </div>
              </div>

              {/* Evidence Inventory Summary */}
              {evidence.length > 0 && (
                <div className="docket-evidence-summary">
                  <h3 className="docket-section-title">Logged Crime Scene Evidence</h3>
                  <div className="docket-evidence-table">
                    {evidence.map((ev, idx) => (
                      <div key={ev.id || idx} className="docket-evidence-row">
                        <span className="ev-num">EV-{String(idx + 1).padStart(2, "0")}</span>
                        <div className="ev-info">
                          <strong>{ev.title}</strong>
                          <small>{ev.category} · {ev.meta_info || ev.location}</small>
                        </div>
                        <span className="ev-status">{ev.tag || "VERIFIED"}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Endorsement and Sign-off */}
              <div className="docket-signatures">
                <div className="sig-block">
                  <div className="sig-line" />
                  <strong>{currentUser?.name || "Inspector K. Rao"}</strong>
                  <span>Lead Forensic Investigator</span>
                </div>
                <div className="sig-block">
                  <div className="sig-line" />
                  <strong>Commissioner of Police</strong>
                  <span>Directorate of Criminal Investigation</span>
                </div>
                <div className="sig-seal-box">
                  <span>FORENSIC LAB</span>
                  <strong>SEAL CERTIFIED</strong>
                </div>
              </div>

              {/* Official Disclaimer */}
              <div className="report-note">
                <strong>Official Decision Support Notice</strong>
                <p>
                  This document is generated by Veritas Crime Investigation AI. All probabilistic analyses, graph linkages, and logical deductions serve as explainable decision-support for authorized law enforcement and judicial authorities.
                </p>
              </div>
            </div>

            <div className="report-footer no-print">
              <button className="secondary" onClick={() => setReportOpen(false)}>
                Close Docket
              </button>
              <button
                className="primary"
                onClick={() => {
                  window.print();
                }}
              >
                <Icon name="download" size={16} /> Print / Export PDF Docket
              </button>
            </div>
          </section>
        </div>
      )}

      {/* ==================================================== */}
      {/* MODAL 2: REGISTER NEW CASE                           */}
      {/* ==================================================== */}
      {createCaseModal && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setCreateCaseModal(false)}>
          <section className="entry-modal" role="dialog" aria-modal="true" onMouseDown={(e) => e.stopPropagation()}>
            <div className="entry-header">
              <div>
                <span>LAW ENFORCEMENT REGISTRY</span>
                <h2>Register New Crime Case</h2>
              </div>
              <button className="icon-button" onClick={() => setCreateCaseModal(false)}>
                <Icon name="close" />
              </button>
            </div>
            <form onSubmit={handleCreateCase}>
              <label>
                Case Title
                <input name="title" placeholder="e.g. Phoenix Diamond Vault Breach" required />
              </label>
              <label>
                Crime Classification
                <select name="crime_type" required defaultValue="Burglary">
                  <option value="High-Value Residence Burglary">High-Value Residence Burglary</option>
                  <option value="Commercial Vault Heist">Commercial Vault Heist</option>
                  <option value="Cyber Financial Fraud">Cyber Financial Fraud</option>
                  <option value="Homicide Investigation">Homicide Investigation</option>
                  <option value="Corporate Embezzlement">Corporate Embezzlement</option>
                  <option value="Industrial Arson">Industrial Arson</option>
                </select>
              </label>
              <label>
                Priority Level
                <select name="priority" required defaultValue="HIGH">
                  <option value="CRITICAL">CRITICAL (Immediate Action)</option>
                  <option value="HIGH">HIGH (Standard Priority)</option>
                  <option value="MEDIUM">MEDIUM (In Review)</option>
                </select>
              </label>
              <label>
                Crime Scene Location
                <input name="location" placeholder="e.g. 42 Harbor Way, Chennai" required />
              </label>
              <label>
                Incident Date & Estimated Time
                <input name="date_time" placeholder="e.g. 15 Oct 2026 · 22:30–01:00" required />
              </label>
              <label>
                Initial Incident Brief
                <textarea name="description" placeholder="Summarize initial findings, forced entry details, or missing assets..." required />
              </label>
              <div className="entry-actions">
                <button type="button" className="secondary" onClick={() => setCreateCaseModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="primary">
                  Register Case Docket <Icon name="check" size={16} />
                </button>
              </div>
            </form>
          </section>
        </div>
      )}

      {/* ==================================================== */}
      {/* MODAL 3: ADD EVIDENCE                                */}
      {/* ==================================================== */}
      {addEvidenceModal && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setAddEvidenceModal(false)}>
          <section className="entry-modal" role="dialog" aria-modal="true" onMouseDown={(e) => e.stopPropagation()}>
            <div className="entry-header">
              <div>
                <span>CHAIN OF CUSTODY</span>
                <h2>Catalog Crime Scene Evidence</h2>
              </div>
              <button className="icon-button" onClick={() => setAddEvidenceModal(false)}>
                <Icon name="close" />
              </button>
            </div>
            <form onSubmit={handleAddEvidence}>
              <label>
                Evidence Category
                <select name="category" required defaultValue="Physical object">
                  <option value="Fingerprint">Fingerprint / Latent Print</option>
                  <option value="Forensic DNA">Forensic DNA / Biological</option>
                  <option value="CCTV footage">CCTV Video Footage</option>
                  <option value="Weapon / object">Weapon / Tool Mark Object</option>
                  <option value="Digital evidence">Digital Logs / Server Record</option>
                  <option value="Witness statement">Witness Deposition</option>
                </select>
              </label>
              <label>
                Evidence Label
                <input name="title" placeholder="e.g. Latent print on safe dial" required />
              </label>
              <label>
                Recovery Location & Custody Notes
                <textarea name="details" placeholder="Record precise recovery location and tag numbers..." required />
              </label>
              <div className="entry-actions">
                <button type="button" className="secondary" onClick={() => setAddEvidenceModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="primary">
                  Save Evidence Item <Icon name="check" size={16} />
                </button>
              </div>
            </form>
          </section>
        </div>
      )}

      {/* ==================================================== */}
      {/* MODAL 4: ADD SUSPECT                                 */}
      {/* ==================================================== */}
      {addSuspectModal && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setAddSuspectModal(false)}>
          <section className="entry-modal" role="dialog" aria-modal="true" onMouseDown={(e) => e.stopPropagation()}>
            <div className="entry-header">
              <div>
                <span>PERSON OF INTEREST</span>
                <h2>Register Possible Suspect</h2>
              </div>
              <button className="icon-button" onClick={() => setAddSuspectModal(false)}>
                <Icon name="close" />
              </button>
            </div>
            <form onSubmit={handleAddSuspect}>
              <label>
                Full Legal Name
                <input name="name" placeholder="e.g. Rajesh Khurana" required />
              </label>
              <label>
                Role or Connection to Scene
                <input name="role" placeholder="e.g. Former Vault Contractor" required />
              </label>
              <label>
                Investigative Notes & Motive Summary
                <textarea name="notes" placeholder="Detail any financial dispute, access knowledge, or conflicting statements..." required />
              </label>
              <div className="form-guidance">
                <Icon name="logic" size={17} />
                <p>
                  The suspect profile will immediately enter the Opportunity Filter and be tested against timeline, physical access, and forensic matching rules.
                </p>
              </div>
              <div className="entry-actions">
                <button type="button" className="secondary" onClick={() => setAddSuspectModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="primary">
                  Register Suspect <Icon name="check" size={16} />
                </button>
              </div>
            </form>
          </section>
        </div>
      )}
    </div>
  );
}
