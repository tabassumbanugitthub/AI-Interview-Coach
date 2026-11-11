import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import random
import re
import os
from datetime import datetime
import statistics


# ============================================================
# AI INTERVIEW COACH
# Single-file Tkinter + SQLite application
# No external libraries required
# ============================================================

APP_NAME = "AI INTERVIEW COACH"
DB_NAME = "ai_interview_coach.db"


# ============================================================
# COLORS
# ============================================================

BG = "#0B1020"
SIDEBAR = "#11182D"
CARD = "#151E35"
CARD2 = "#1B2742"
ACCENT = "#6C63FF"
ACCENT2 = "#8B83FF"
TEXT = "#F5F7FF"
MUTED = "#9AA6C2"
GREEN = "#32D583"
YELLOW = "#FBBF24"
RED = "#F97068"
BLUE = "#38BDF8"
WHITE = "#FFFFFF"


# ============================================================
# ROLE DATA
# ============================================================

ROLE_DATA = {
    "SOC Analyst": {
        "skills": [
            "SIEM", "Networking", "Linux", "Windows Logs",
            "Incident Response", "Threat Detection",
            "Cybersecurity", "MITRE ATT&CK", "Python"
        ],
        "topics": [
            ("Cybersecurity Fundamentals", "Learn the basic concepts of threats, vulnerabilities, attacks and security controls."),
            ("SIEM Fundamentals", "SIEM platforms collect and correlate logs from systems, applications and security devices."),
            ("Incident Response", "Incident response involves preparation, detection, containment, eradication, recovery and lessons learned."),
            ("Network Monitoring", "Network monitoring helps analysts identify unusual traffic, suspicious connections and possible attacks."),
            ("MITRE ATT&CK", "MITRE ATT&CK provides a knowledge base of adversary tactics and techniques."),
            ("Windows Logs", "Windows event logs provide useful information about authentication, processes and system activity."),
            ("DNS Tunneling", "DNS tunneling can abuse DNS queries and responses to secretly transfer information.")
        ],
        "questions": [
            {
                "q": "What is a SIEM and why is it useful to a SOC analyst?",
                "keywords": ["siem", "logs", "correlation", "alert", "security", "monitor"],
                "model": "A strong answer should explain that SIEM collects and centralizes security logs, correlates events, generates alerts and helps analysts investigate suspicious activity."
            },
            {
                "q": "What would you do if you detected multiple failed login attempts from the same IP address?",
                "keywords": ["logs", "ip", "investigate", "brute", "siem", "block", "account"],
                "model": "A strong answer should mention investigating logs, checking the source IP, identifying whether the activity is brute force, correlating events, containing the threat and documenting the incident."
            },
            {
                "q": "Explain the difference between an event, an alert and an incident.",
                "keywords": ["event", "alert", "incident", "suspicious", "investigate"],
                "model": "An event is an observable activity. An alert is a notification generated when activity meets a rule or threshold. An incident is a confirmed security event requiring investigation or response."
            },
            {
                "q": "What is DNS tunneling?",
                "keywords": ["dns", "tunnel", "data", "exfiltration", "query", "domain"],
                "model": "DNS tunneling abuses DNS queries or responses to encode and transfer data, sometimes allowing attackers to communicate with command-and-control infrastructure or exfiltrate information."
            },
            {
                "q": "What steps would you take after receiving a malware alert?",
                "keywords": ["investigate", "isolate", "malware", "logs", "contain", "endpoint", "incident"],
                "model": "A strong response includes validating the alert, investigating the endpoint and logs, isolating the affected system, identifying the malware, containing the incident, removing the threat and documenting the response."
            },
            {
                "q": "What is the principle of least privilege?",
                "keywords": ["least", "privilege", "access", "minimum", "permission", "security"],
                "model": "Least privilege means giving users and systems only the minimum permissions required to perform their legitimate tasks."
            }
        ]
    },

    "Python Developer": {
        "skills": [
            "Python", "OOP", "Data Structures", "SQL",
            "Git", "APIs", "Exception Handling", "Debugging"
        ],
        "topics": [
            ("Python Fundamentals", "Variables, data types, operators, conditions, loops and functions."),
            ("Object Oriented Programming", "Classes, objects, inheritance, encapsulation and polymorphism."),
            ("Exception Handling", "Python uses try, except, else and finally to handle runtime errors."),
            ("Data Structures", "Lists, tuples, sets and dictionaries are common Python data structures."),
            ("SQL Basics", "SQL is used to store, retrieve and manipulate structured data."),
            ("API Fundamentals", "APIs allow different software systems to communicate with one another."),
            ("Debugging", "Debugging involves identifying, isolating and fixing problems in a program.")
        ],
        "questions": [
            {
                "q": "What is the difference between a list and a tuple in Python?",
                "keywords": ["list", "tuple", "mutable", "immutable", "change"],
                "model": "Lists are mutable and can be modified after creation, while tuples are immutable. Both can store ordered collections."
            },
            {
                "q": "Explain object-oriented programming in Python.",
                "keywords": ["class", "object", "inheritance", "encapsulation", "polymorphism"],
                "model": "A strong answer should discuss classes and objects and may explain inheritance, encapsulation, abstraction and polymorphism."
            },
            {
                "q": "How does exception handling work in Python?",
                "keywords": ["try", "except", "error", "exception", "finally"],
                "model": "Python uses try and except to handle exceptions. else can execute when no exception occurs and finally can execute regardless of the result."
            },
            {
                "q": "What is a dictionary in Python?",
                "keywords": ["dictionary", "key", "value", "mapping"],
                "model": "A dictionary stores key-value pairs and allows values to be retrieved using their associated keys."
            },
            {
                "q": "How would you debug a Python program that is producing incorrect output?",
                "keywords": ["debug", "print", "error", "test", "logic", "trace"],
                "model": "A good answer should mention reproducing the issue, checking assumptions, tracing program flow, inspecting variables, testing smaller sections and fixing the root cause."
            }
        ]
    },

    "Software Developer": {
        "skills": [
            "Programming", "OOP", "Data Structures", "Algorithms",
            "SQL", "Git", "Debugging", "Software Engineering"
        ],
        "topics": [
            ("Data Structures", "Learn arrays, lists, stacks, queues, trees, graphs and hash tables."),
            ("Algorithms", "Algorithms provide systematic methods for solving computational problems."),
            ("OOP", "Object-oriented programming organizes software around objects and classes."),
            ("Database Fundamentals", "Databases store and organize application data efficiently."),
            ("Version Control", "Git tracks changes and helps developers collaborate safely."),
            ("Software Testing", "Testing verifies whether software behaves according to requirements."),
            ("Debugging", "Debugging helps locate and fix defects in software.")
        ],
        "questions": [
            {
                "q": "What is object-oriented programming?",
                "keywords": ["class", "object", "inheritance", "encapsulation", "polymorphism"],
                "model": "OOP organizes software using classes and objects and commonly uses encapsulation, inheritance, abstraction and polymorphism."
            },
            {
                "q": "What is the purpose of Git?",
                "keywords": ["git", "version", "control", "repository", "commit", "branch"],
                "model": "Git is a version control system used to track changes, maintain history, create branches and collaborate with other developers."
            },
            {
                "q": "What is the difference between a stack and a queue?",
                "keywords": ["stack", "queue", "lifo", "fifo", "push", "pop"],
                "model": "A stack follows LIFO, while a queue follows FIFO."
            },
            {
                "q": "How do you approach debugging?",
                "keywords": ["debug", "reproduce", "error", "test", "logs", "root"],
                "model": "A good debugging process reproduces the problem, identifies the location, examines logs or variables, isolates the root cause, applies a fix and tests again."
            }
        ]
    },

    "Data Analyst": {
        "skills": [
            "Python", "SQL", "Excel", "Statistics",
            "Data Visualization", "Data Cleaning", "Analysis"
        ],
        "topics": [
            ("Data Analysis Fundamentals", "Understand the process of collecting, cleaning, analyzing and interpreting data."),
            ("SQL", "Learn SELECT, WHERE, GROUP BY, JOIN, aggregate functions and subqueries."),
            ("Statistics", "Understand mean, median, variance, standard deviation and probability."),
            ("Data Cleaning", "Data cleaning removes errors, duplicates and inconsistencies."),
            ("Data Visualization", "Charts help communicate patterns and trends in data."),
            ("Analytical Thinking", "Analytical thinking involves breaking complex problems into measurable components.")
        ],
        "questions": [
            {
                "q": "What is data cleaning and why is it important?",
                "keywords": ["data", "clean", "missing", "duplicate", "error", "quality"],
                "model": "Data cleaning identifies and corrects missing, duplicate, incorrect or inconsistent data so analysis becomes more reliable."
            },
            {
                "q": "What is the difference between mean and median?",
                "keywords": ["mean", "median", "average", "outlier", "middle"],
                "model": "Mean is the arithmetic average. Median is the middle value after sorting the data and is generally less affected by extreme outliers."
            },
            {
                "q": "What is a SQL JOIN?",
                "keywords": ["sql", "join", "table", "matching", "rows", "key"],
                "model": "A JOIN combines rows from two or more tables using related columns or keys."
            },
            {
                "q": "How would you present an analytical finding to a non-technical person?",
                "keywords": ["simple", "visual", "business", "explain", "insight", "recommend"],
                "model": "A strong answer should avoid unnecessary technical terminology, focus on the business impact, use simple visuals and clearly state the insight and recommendation."
            }
        ]
    },

    "Network Security Engineer": {
        "skills": [
            "Networking", "TCP/IP", "Firewalls", "VPN",
            "IDS", "IPS", "Cybersecurity", "Network Monitoring"
        ],
        "topics": [
            ("TCP/IP", "Understand networking layers, protocols, addressing and communication."),
            ("Firewalls", "Firewalls control network traffic based on security rules."),
            ("IDS and IPS", "IDS detects suspicious traffic while IPS can actively block it."),
            ("VPN", "VPNs provide encrypted communication across untrusted networks."),
            ("Network Attacks", "Learn about scanning, spoofing, DoS, MITM and other attacks."),
            ("Network Monitoring", "Monitoring helps identify unusual traffic and security events.")
        ],
        "questions": [
            {
                "q": "What is the difference between an IDS and an IPS?",
                "keywords": ["ids", "ips", "detect", "prevent", "block", "traffic"],
                "model": "An IDS detects and alerts on suspicious traffic, while an IPS can actively prevent or block malicious traffic."
            },
            {
                "q": "What is a firewall?",
                "keywords": ["firewall", "traffic", "rule", "network", "allow", "block"],
                "model": "A firewall monitors and controls network traffic according to predefined security rules."
            },
            {
                "q": "What is a VPN?",
                "keywords": ["vpn", "encrypted", "tunnel", "network", "secure"],
                "model": "A VPN creates a protected communication tunnel, commonly using encryption, over an untrusted network."
            }
        ]
    }
}


# ============================================================
# GENERIC FALLBACK ROLE
# ============================================================

GENERIC_TOPICS = [
    ("Role Fundamentals", "Review the core concepts, terminology and responsibilities associated with your target role."),
    ("Communication", "Practice explaining technical concepts clearly and confidently."),
    ("Problem Solving", "Develop a structured approach to analyzing problems and explaining solutions."),
    ("Behavioral Questions", "Prepare examples that demonstrate teamwork, leadership, adaptability and learning."),
    ("Technical Fundamentals", "Review the technical concepts most frequently associated with your selected role."),
    ("Industry Awareness", "Understand common tools, technologies and challenges in your chosen career area.")
]

GENERIC_QUESTIONS = [
    {
        "q": "Tell me about yourself and your technical background.",
        "keywords": ["education", "skills", "project", "experience", "role", "goal"],
        "model": "A strong answer should briefly cover education, relevant skills, projects or experience and explain why the candidate is interested in the role."
    },
    {
        "q": "Describe a technical project you have worked on.",
        "keywords": ["project", "problem", "solution", "technology", "result"],
        "model": "Explain the problem, your approach, technologies used, your contribution and the result."
    },
    {
        "q": "How do you approach learning a new technology?",
        "keywords": ["learn", "documentation", "practice", "project", "research"],
        "model": "A good answer should mention understanding fundamentals, using documentation, practicing and applying the technology in a project."
    },
    {
        "q": "Describe a difficult problem you solved.",
        "keywords": ["problem", "solution", "approach", "result", "learn"],
        "model": "Use a structured explanation: problem, analysis, solution, result and lesson learned."
    }
]


# ============================================================
# DATABASE
# ============================================================

class Database:
    def __init__(self, filename=DB_NAME):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT,
                email TEXT,
                phone TEXT,
                college TEXT,
                degree TEXT,
                year TEXT,
                location TEXT,
                target_role TEXT,
                objective TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill TEXT UNIQUE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS profile_skills (
                profile_id INTEGER,
                skill_id INTEGER,
                UNIQUE(profile_id, skill_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS certifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                organization TEXT,
                issue_date TEXT,
                credential_id TEXT,
                credential_url TEXT,
                skills TEXT,
                status TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER,
                summary TEXT,
                linkedin TEXT,
                github TEXT,
                updated_at TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                name TEXT,
                description TEXT,
                technologies TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                company TEXT,
                role TEXT,
                description TEXT,
                duration TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS learning_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                topic TEXT,
                material TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,
                completed INTEGER DEFAULT 0,
                UNIQUE(topic_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                interview_type TEXT,
                difficulty TEXT,
                date TEXT,
                total_score REAL,
                communication REAL,
                technical REAL,
                relevance REAL,
                completeness REAL,
                confidence REAL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS interview_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER,
                question TEXT,
                answer TEXT,
                score REAL,
                technical REAL,
                relevance REAL,
                completeness REAL,
                confidence REAL,
                feedback TEXT,
                missing_keywords TEXT
            )
        """)

        self.conn.commit()

    def seed_data(self):
        cur = self.conn.cursor()

        count = cur.execute(
            "SELECT COUNT(*) FROM learning_topics"
        ).fetchone()[0]

        if count == 0:
            for role, data in ROLE_DATA.items():
                for topic, material in data["topics"]:
                    cur.execute(
                        "INSERT INTO learning_topics(role, topic, material) VALUES (?, ?, ?)",
                        (role, topic, material)
                    )

            self.conn.commit()

    def execute(self, query, params=(), fetch=False, many=False):
        cur = self.conn.cursor()

        if many:
            cur.executemany(query, params)
        else:
            cur.execute(query, params)

        self.conn.commit()

        if fetch:
            return cur.fetchall()

        return cur

    def close(self):
        self.conn.close()


# ============================================================
# MAIN APPLICATION
# ============================================================

class InterviewCoach(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1280x760")
        self.minsize(1100, 680)
        self.configure(bg=BG)

        self.db = Database()

        self.current_page = None
        self.current_role = "SOC Analyst"

        self.interview_questions = []
        self.current_question_index = 0
        self.current_interview_answers = []
        self.interview_start_time = None

        self.setup_style()
        self.load_profile_role()
        self.create_layout()
        self.show_dashboard()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):
        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=CARD2,
            background=CARD2,
            foreground=TEXT,
            arrowcolor=TEXT,
            borderwidth=0
        )

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=32,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=CARD2,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold")
        )

    # ========================================================
    # PROFILE ROLE
    # ========================================================

    def load_profile_role(self):
        row = self.db.execute(
            "SELECT target_role FROM profile WHERE id=1",
            fetch=True
        )

        if row and row[0]["target_role"]:
            self.current_role = row[0]["target_role"]

    # ========================================================
    # LAYOUT
    # ========================================================

    def create_layout(self):

        self.sidebar = tk.Frame(
            self,
            bg=SIDEBAR,
            width=235
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self,
            bg=BG
        )
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        logo_frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )
        logo_frame.pack(
            fill="x",
            pady=(28, 25),
            padx=20
        )

        tk.Label(
            logo_frame,
            text="AI",
            font=("Segoe UI", 22, "bold"),
            bg=ACCENT,
            fg=WHITE,
            width=3
        ).pack(
            side="left"
        )

        title_frame = tk.Frame(
            logo_frame,
            bg=SIDEBAR
        )
        title_frame.pack(
            side="left",
            padx=10
        )

        tk.Label(
            title_frame,
            text="INTERVIEW",
            font=("Segoe UI", 11, "bold"),
            bg=SIDEBAR,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="COACH",
            font=("Segoe UI", 11, "bold"),
            bg=SIDEBAR,
            fg=ACCENT2
        ).pack(anchor="w")

        self.nav_buttons = {}

        items = [
            ("🏠", "Dashboard", self.show_dashboard),
            ("👤", "Profile", self.show_profile),
            ("📄", "Resume Builder", self.show_resume),
            ("🎤", "Mock Interview", self.show_interview),
            ("🏆", "Certifications", self.show_certifications),
            ("📚", "Learning Hub", self.show_learning),
            ("📊", "Analytics", self.show_analytics)
        ]

        for icon, name, command in items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {icon}   {name}",
                command=command,
                bg=SIDEBAR,
                fg=MUTED,
                activebackground=CARD2,
                activeforeground=WHITE,
                relief="flat",
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                bd=0,
                cursor="hand2",
                padx=20,
                pady=12
            )
            btn.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.nav_buttons[name] = btn

        spacer = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )
        spacer.pack(
            fill="both",
            expand=True
        )

        role_card = tk.Frame(
            self.sidebar,
            bg=CARD,
            padx=15,
            pady=15
        )
        role_card.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            role_card,
            text="TARGET ROLE",
            font=("Segoe UI", 8, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        self.sidebar_role = tk.Label(
            role_card,
            text=self.current_role,
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=ACCENT2,
            wraplength=180
        )
        self.sidebar_role.pack(
            anchor="w",
            pady=(5, 0)
        )

        tk.Label(
            self.sidebar,
            text="v1.0 • Intelligent Career Assistant",
            font=("Segoe UI", 8),
            bg=SIDEBAR,
            fg="#65718E"
        ).pack(
            pady=(0, 15)
        )

    # ========================================================
    # UTILITIES
    # ========================================================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_header(self, title, subtitle=""):
        frame = tk.Frame(
            self.content,
            bg=BG
        )
        frame.pack(
            fill="x",
            padx=35,
            pady=(28, 15)
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 25, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                frame,
                text=subtitle,
                font=("Segoe UI", 10),
                bg=BG,
                fg=MUTED
            ).pack(anchor="w", pady=(4, 0))

        return frame

    def card(self, parent, width=None, height=None):
        frame = tk.Frame(
            parent,
            bg=CARD,
            highlightthickness=1,
            highlightbackground="#202C49"
        )

        if width:
            frame.config(width=width)

        if height:
            frame.config(height=height)

        return frame

    def button(self, parent, text, command, primary=True):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT if primary else CARD2,
            fg=WHITE,
            activebackground=ACCENT2,
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        )

    def label(self, parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            bg=parent.cget("bg"),
            fg=color
        )

    def entry(self, parent, value="", width=30):
        e = tk.Entry(
            parent,
            bg=CARD2,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            font=("Segoe UI", 10),
            width=width
        )
        if value:
            e.insert(0, value)
        return e

    def get_profile(self):
        rows = self.db.execute(
            "SELECT * FROM profile WHERE id=1",
            fetch=True
        )
        if rows:
            return rows[0]

        return None

    def get_profile_skills(self):
        rows = self.db.execute("""
            SELECT s.skill
            FROM skills s
            JOIN profile_skills ps ON s.id = ps.skill_id
            WHERE ps.profile_id = 1
        """, fetch=True)

        return [r["skill"] for r in rows]

    def set_active_nav(self, name):
        for key, btn in self.nav_buttons.items():
            if key == name:
                btn.config(
                    bg=ACCENT,
                    fg=WHITE
                )
            else:
                btn.config(
                    bg=SIDEBAR,
                    fg=MUTED
                )

    def progress_bar(self, parent, value, maximum=100, width=300):
        canvas = tk.Canvas(
            parent,
            width=width,
            height=12,
            bg=CARD,
            highlightthickness=0
        )

        canvas.create_rectangle(
            0, 2, width, 12,
            fill="#263451",
            outline=""
        )

        fill_width = max(0, min(width, width * value / maximum))

        canvas.create_rectangle(
            0, 2, fill_width, 12,
            fill=ACCENT,
            outline=""
        )

        return canvas

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):
        self.current_page = "Dashboard"
        self.set_active_nav("Dashboard")
        self.clear_content()

        profile = self.get_profile()

        name = profile["name"] if profile and profile["name"] else "Candidate"
        role = profile["target_role"] if profile and profile["target_role"] else "Select your target role"

        self.sidebar_role.config(text=role)

        self.page_header(
            f"Good to see you, {name} 👋",
            "Your personalized interview preparation command center."
        )

        main = tk.Frame(
            self.content,
            bg=BG
        )
        main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=5
        )

        # Readiness
        readiness = self.calculate_readiness()

        top = tk.Frame(main, bg=BG)
        top.pack(fill="x")

        readiness_card = self.card(top)
        readiness_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        left = tk.Frame(
            readiness_card,
            bg=CARD
        )
        left.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        tk.Label(
            left,
            text="CAREER READINESS",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        readiness_line = tk.Frame(left, bg=CARD)
        readiness_line.pack(fill="x", pady=(10, 5))

        tk.Label(
            readiness_line,
            text=f"{readiness:.0f}%",
            font=("Segoe UI", 32, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(side="left")

        status = self.readiness_status(readiness)

        tk.Label(
            readiness_line,
            text=status,
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=GREEN if readiness >= 70 else YELLOW if readiness >= 45 else RED
        ).pack(
            side="left",
            padx=15,
            pady=(10, 0)
        )

        self.progress_bar(
            left,
            readiness,
            width=400
        ).pack(
            anchor="w",
            pady=8
        )

        tk.Label(
            left,
            text="Calculated from interview performance, resume completeness, certifications and learning progress.",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED,
            wraplength=500,
            justify="left"
        ).pack(anchor="w")

        # Start interview card
        action = self.card(top, width=280)
        action.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        tk.Label(
            action,
            text="READY TO PRACTICE?",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 5)
        )

        tk.Label(
            action,
            text="Take a new mock interview and improve your score.",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT,
            wraplength=240,
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=8
        )

        self.button(
            action,
            "🎤  START INTERVIEW",
            self.show_interview
        ).pack(
            fill="x",
            padx=22,
            pady=(8, 22)
        )

        # Statistics
        stats_frame = tk.Frame(main, bg=BG)
        stats_frame.pack(
            fill="x",
            pady=15
        )

        stats = self.get_dashboard_stats()

        self.stat_card(
            stats_frame,
            "INTERVIEWS",
            str(stats["interviews"]),
            "Total completed",
            BLUE
        )

        self.stat_card(
            stats_frame,
            "AVERAGE SCORE",
            f"{stats['average']:.0f}%",
            "Interview average",
            GREEN
        )

        self.stat_card(
            stats_frame,
            "SKILLS",
            str(stats["skills"]),
            "Profile skills",
            ACCENT2
        )

        self.stat_card(
            stats_frame,
            "CERTIFICATIONS",
            str(stats["certifications"]),
            "Added to profile",
            YELLOW
        )

        # Bottom
        bottom = tk.Frame(main, bg=BG)
        bottom.pack(
            fill="both",
            expand=True
        )

        self.create_performance_card(bottom)
        self.create_recommendation_card(bottom)

    def stat_card(self, parent, title, value, subtitle, color):
        frame = self.card(parent)
        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Frame(
            frame,
            bg=color,
            width=4
        ).pack(
            side="left",
            fill="y"
        )

        inner = tk.Frame(frame, bg=CARD)
        inner.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=value,
            font=("Segoe UI", 23, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=subtitle,
            font=("Segoe UI", 8),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

    def create_performance_card(self, parent):
        frame = self.card(parent)
        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        tk.Label(
            frame,
            text="INTERVIEW PERFORMANCE",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        tk.Label(
            frame,
            text="Your latest interview scores",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=20
        )

        canvas = tk.Canvas(
            frame,
            bg=CARD,
            highlightthickness=0,
            height=170
        )
        canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        rows = self.db.execute("""
            SELECT total_score
            FROM interviews
            ORDER BY id ASC
            LIMIT 12
        """, fetch=True)

        values = [float(r["total_score"]) for r in rows]

        if not values:
            canvas.create_text(
                250, 75,
                text="Complete your first mock interview\n\nto see your performance graph.",
                fill=MUTED,
                font=("Segoe UI", 10),
                justify="center"
            )
            return

        self.draw_chart(canvas, values)

    def draw_chart(self, canvas, values):
        canvas.delete("all")

        width = max(canvas.winfo_width(), 400)
        height = max(canvas.winfo_height(), 160)

        margin_left = 40
        margin_right = 20
        margin_top = 15
        margin_bottom = 30

        chart_w = width - margin_left - margin_right
        chart_h = height - margin_top - margin_bottom

        for score in [0, 25, 50, 75, 100]:
            y = margin_top + chart_h - (score / 100) * chart_h

            canvas.create_line(
                margin_left,
                y,
                width - margin_right,
                y,
                fill="#25314D"
            )

            canvas.create_text(
                22,
                y,
                text=str(score),
                fill=MUTED,
                font=("Segoe UI", 7)
            )

        if len(values) == 1:
            xs = [margin_left + chart_w / 2]
        else:
            xs = [
                margin_left + i * chart_w / (len(values) - 1)
                for i in range(len(values))
            ]

        points = []

        for i, value in enumerate(values):
            x = xs[i]
            y = margin_top + chart_h - (value / 100) * chart_h
            points.append((x, y))

        for i in range(len(points) - 1):
            canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill=ACCENT2,
                width=3
            )

        for i, (x, y) in enumerate(points):
            canvas.create_oval(
                x - 4,
                y - 4,
                x + 4,
                y + 4,
                fill=ACCENT,
                outline=""
            )

            canvas.create_text(
                x,
                y - 15,
                text=f"{values[i]:.0f}",
                fill=TEXT,
                font=("Segoe UI", 8, "bold")
            )

    def create_recommendation_card(self, parent):
        frame = self.card(parent)
        frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            frame,
            text="COACH RECOMMENDATIONS",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        tk.Label(
            frame,
            text="Personalized actions based on your data",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=20
        )

        recommendations = self.get_recommendations()

        for rec in recommendations[:4]:
            row = tk.Frame(frame, bg=CARD)
            row.pack(
                fill="x",
                padx=20,
                pady=9
            )

            tk.Label(
                row,
                text="●",
                font=("Segoe UI", 10),
                bg=CARD,
                fg=ACCENT2
            ).pack(side="left")

            tk.Label(
                row,
                text=rec,
                font=("Segoe UI", 9),
                bg=CARD,
                fg=TEXT,
                wraplength=350,
                justify="left"
            ).pack(
                side="left",
                padx=8
            )

    # ========================================================
    # PROFILE
    # ========================================================

    def show_profile(self):
        self.current_page = "Profile"
        self.set_active_nav("Profile")
        self.clear_content()

        self.page_header(
            "Candidate Profile",
            "Your profile powers your resume, learning recommendations and mock interviews."
        )

        container = tk.Frame(self.content, bg=BG)
        container.pack(
            fill="both",
            expand=True,
            padx=35
        )

        left = self.card(container)
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        right = self.card(container)
        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        profile = self.get_profile()

        fields = [
            ("Full Name", "name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("College / University", "college"),
            ("Degree", "degree"),
            ("Academic Year", "year"),
            ("Location", "location"),
            ("Career Objective", "objective")
        ]

        entries = {}

        tk.Label(
            left,
            text="PERSONAL INFORMATION",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 15)
        )

        form = tk.Frame(left, bg=CARD)
        form.pack(
            fill="x",
            padx=25
        )

        for i, (display, key) in enumerate(fields):
            tk.Label(
                form,
                text=display,
                font=("Segoe UI", 9, "bold"),
                bg=CARD,
                fg=MUTED
            ).grid(
                row=i,
                column=0,
                sticky="w",
                pady=7
            )

            value = ""
            if profile and key in profile.keys() and profile[key]:
                value = profile[key]

            e = self.entry(form, value, 32)
            e.grid(
                row=i,
                column=1,
                sticky="ew",
                padx=(20, 0),
                pady=7
            )

            entries[key] = e

        form.columnconfigure(1, weight=1)

        self.button(
            left,
            "💾  SAVE PROFILE",
            lambda: self.save_profile(entries)
        ).pack(
            anchor="e",
            padx=25,
            pady=20
        )

        # Skills section
        tk.Label(
            right,
            text="SKILLS & TARGET ROLE",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 15)
        )

        tk.Label(
            right,
            text="Target Career Role",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=25
        )

        roles = list(ROLE_DATA.keys())

        if self.current_role not in roles:
            roles.append(self.current_role)

        role_var = tk.StringVar(value=self.current_role)

        role_box = ttk.Combobox(
            right,
            textvariable=role_var,
            values=roles,
            state="readonly",
            font=("Segoe UI", 10)
        )
        role_box.pack(
            fill="x",
            padx=25,
            pady=(7, 15)
        )

        skill_frame = tk.Frame(right, bg=CARD)
        skill_frame.pack(
            fill="both",
            expand=True,
            padx=25
        )

        tk.Label(
            skill_frame,
            text="Your Current Skills",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        skill_text = tk.Text(
            skill_frame,
            height=8,
            bg=CARD2,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=10
        )
        skill_text.pack(
            fill="both",
            expand=True,
            pady=8
        )

        existing_skills = self.get_profile_skills()

        if existing_skills:
            skill_text.insert(
                "1.0",
                ", ".join(existing_skills)
            )

        tk.Label(
            skill_frame,
            text="Tip: separate skills with commas.",
            font=("Segoe UI", 8),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        def save_all():
            self.save_profile(
                entries,
                role_var.get(),
                skill_text.get("1.0", "end").strip()
            )

        self.button(
            right,
            "✨  SAVE PROFILE & UPDATE COACH",
            save_all
        ).pack(
            anchor="e",
            padx=25,
            pady=20
        )

    def save_profile(self, entries, role=None, skills_text=None):

        data = {
            key: entries[key].get().strip()
            for key in entries
        }

        if role:
            data["target_role"] = role
        else:
            data["target_role"] = self.current_role

        self.db.execute("""
            INSERT OR REPLACE INTO profile
            (id, name, email, phone, college, degree, year, location, target_role, objective)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["email"],
            data["phone"],
            data["college"],
            data["degree"],
            data["year"],
            data["location"],
            data["target_role"],
            data["objective"]
        ))

        self.current_role = data["target_role"]
        self.sidebar_role.config(text=self.current_role)

        if skills_text is not None:
            skill_list = [
                x.strip()
                for x in re.split(r",|\n", skills_text)
                if x.strip()
            ]

            self.db.execute(
                "DELETE FROM profile_skills WHERE profile_id=1"
            )

            for skill in skill_list:
                self.db.execute(
                    "INSERT OR IGNORE INTO skills(skill) VALUES (?)",
                    (skill,)
                )

                row = self.db.execute(
                    "SELECT id FROM skills WHERE skill=?",
                    (skill,),
                    fetch=True
                )

                if row:
                    self.db.execute(
                        "INSERT OR IGNORE INTO profile_skills(profile_id, skill_id) VALUES (?, ?)",
                        (1, row[0]["id"])
                    )

        # Add recommended role skills if none exist
        if skills_text is None or not skills_text.strip():
            if self.current_role in ROLE_DATA:
                self.db.execute(
                    "DELETE FROM profile_skills WHERE profile_id=1"
                )

                for skill in ROLE_DATA[self.current_role]["skills"]:
                    self.db.execute(
                        "INSERT OR IGNORE INTO skills(skill) VALUES (?)",
                        (skill,)
                    )

                    row = self.db.execute(
                        "SELECT id FROM skills WHERE skill=?",
                        (skill,),
                        fetch=True
                    )

                    if row:
                        self.db.execute(
                            "INSERT OR IGNORE INTO profile_skills(profile_id, skill_id) VALUES (?, ?)",
                            (1, row[0]["id"])
                        )

        messagebox.showinfo(
            "Profile Saved",
            "Your profile has been saved successfully.\n\n"
            "Your target role will now influence interviews, learning and recommendations."
        )

        self.show_dashboard()

    # ========================================================
    # RESUME BUILDER
    # ========================================================

    def show_resume(self):
        self.current_page = "Resume Builder"
        self.set_active_nav("Resume Builder")
        self.clear_content()

        self.page_header(
            "Resume Builder",
            "Build a role-focused resume using information already stored in your profile."
        )

        container = tk.Frame(self.content, bg=BG)
        container.pack(
            fill="both",
            expand=True,
            padx=35
        )

        left = self.card(container)
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        right = self.card(container)
        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        profile = self.get_profile()

        # LEFT
        tk.Label(
            left,
            text="RESUME INFORMATION",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 10)
        )

        form = tk.Frame(left, bg=CARD)
        form.pack(
            fill="x",
            padx=22
        )

        fields = [
            ("LinkedIn", "linkedin"),
            ("GitHub", "github")
        ]

        existing = self.db.execute(
            "SELECT * FROM resumes ORDER BY id DESC LIMIT 1",
            fetch=True
        )

        resume = existing[0] if existing else None

        entries = {}

        for display, key in fields:
            tk.Label(
                form,
                text=display,
                font=("Segoe UI", 9, "bold"),
                bg=CARD,
                fg=MUTED
            ).pack(anchor="w", pady=(5, 3))

            value = resume[key] if resume and resume[key] else ""

            e = self.entry(form, value, 35)
            e.pack(
                fill="x",
                pady=(0, 7)
            )

            entries[key] = e

        tk.Label(
            form,
            text="Professional Summary",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 3))

        summary = tk.Text(
            form,
            height=6,
            bg=CARD2,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            font=("Segoe UI", 9),
            padx=10,
            pady=8
        )
        summary.pack(
            fill="x",
            pady=(0, 10)
        )

        if resume and resume["summary"]:
            summary.insert("1.0", resume["summary"])
        elif profile:
            summary.insert(
                "1.0",
                f"{profile['name'] or 'Candidate'} is a {profile['degree'] or 'student'} "
                f"interested in building a career as a {profile['target_role'] or 'technology professional'}. "
                f"{profile['objective'] or ''}"
            )

        tk.Label(
            form,
            text="Projects",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 3))

        project_text = tk.Text(
            form,
            height=7,
            bg=CARD2,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            font=("Segoe UI", 9),
            padx=10,
            pady=8
        )
        project_text.pack(
            fill="both",
            expand=True
        )

        projects = []

        if resume:
            projects = self.db.execute(
                "SELECT * FROM projects WHERE resume_id=?",
                (resume["id"],),
                fetch=True
            )

        for p in projects:
            project_text.insert(
                "end",
                f"{p['name']} | {p['technologies']}\n{p['description']}\n\n"
            )

        tk.Label(
            form,
            text="Format: Project Name | Technologies, then description.",
            font=("Segoe UI", 8),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=4)

        self.button(
            left,
            "💾 SAVE RESUME",
            lambda: self.save_resume(
                entries,
                summary,
                project_text
            )
        ).pack(
            anchor="e",
            padx=22,
            pady=15
        )

        # RIGHT PREVIEW
        tk.Label(
            right,
            text="LIVE RESUME PREVIEW",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 10)
        )

        preview = tk.Text(
            right,
            bg="#F7F8FC",
            fg="#1A2030",
            font=("Segoe UI", 9),
            relief="flat",
            padx=25,
            pady=20,
            wrap="word"
        )
        preview.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 20)
        )

        preview.insert(
            "1.0",
            self.generate_resume_text(
                profile,
                resume,
                projects
            )
        )

        preview.config(state="disabled")

    def generate_resume_text(self, profile, resume, projects):
        if not profile:
            return (
                "PROFILE NOT CREATED\n\n"
                "Go to Profile and enter your information."
            )

        name = profile["name"] or "YOUR NAME"
        role = profile["target_role"] or "Technology Professional"

        skills = self.get_profile_skills()

        certs = self.db.execute(
            "SELECT * FROM certifications ORDER BY id DESC",
            fetch=True
        )

        summary = ""

        if resume and resume["summary"]:
            summary = resume["summary"]
        else:
            summary = (
                f"{name} is a motivated technology student pursuing a career "
                f"as a {role}. Interested in developing practical skills, "
                f"solving technical problems and continuously learning new technologies."
            )

        text = f"""
{name.upper()}
{role}

{profile['email'] or ''} | {profile['phone'] or ''}
{resume['linkedin'] if resume else ''}
{resume['github'] if resume else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY

{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SKILLS

{', '.join(skills) if skills else 'Add skills from the Profile section.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EDUCATION

{profile['degree'] or 'Degree'}
{profile['college'] or 'College / University'}
Year: {profile['year'] or '—'}
Location: {profile['location'] or '—'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECTS

"""

        if projects:
            for p in projects:
                text += (
                    f"{p['name']}\n"
                    f"{p['description']}\n"
                    f"Technologies: {p['technologies']}\n\n"
                )
        else:
            text += "Add projects in the Resume Builder.\n\n"

        text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nCERTIFICATIONS\n\n"

        if certs:
            for cert in certs:
                text += (
                    f"{cert['name']} — {cert['organization']}\n"
                    f"{cert['status']}\n\n"
                )
        else:
            text += "Add certifications in the Certifications section.\n"

        return text.strip()

    def save_resume(self, entries, summary, project_text):

        existing = self.db.execute(
            "SELECT id FROM resumes ORDER BY id DESC LIMIT 1",
            fetch=True
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing:
            resume_id = existing[0]["id"]

            self.db.execute("""
                UPDATE resumes
                SET summary=?, linkedin=?, github=?, updated_at=?
                WHERE id=?
            """, (
                summary.get("1.0", "end").strip(),
                entries["linkedin"].get().strip(),
                entries["github"].get().strip(),
                now,
                resume_id
            ))

            self.db.execute(
                "DELETE FROM projects WHERE resume_id=?",
                (resume_id,)
            )
        else:
            cur = self.db.execute("""
                INSERT INTO resumes
                (profile_id, summary, linkedin, github, updated_at)
                VALUES (1, ?, ?, ?, ?)
            """, (
                summary.get("1.0", "end").strip(),
                entries["linkedin"].get().strip(),
                entries["github"].get().strip(),
                now
            ))

            resume_id = cur.lastrowid

        blocks = [
            b.strip()
            for b in project_text.get("1.0", "end").split("\n\n")
            if b.strip()
        ]

        for block in blocks:
            lines = block.splitlines()

            if not lines:
                continue

            first = lines[0]

            if "|" in first:
                name, technologies = first.split("|", 1)
                description = "\n".join(lines[1:]).strip()
            else:
                name = first
                technologies = ""
                description = "\n".join(lines[1:]).strip()

            self.db.execute("""
                INSERT INTO projects
                (resume_id, name, description, technologies)
                VALUES (?, ?, ?, ?)
            """, (
                resume_id,
                name.strip(),
                description,
                technologies.strip()
            ))

        messagebox.showinfo(
            "Resume Saved",
            "Your resume has been saved successfully."
        )

        self.show_resume()

    # ========================================================
    # CERTIFICATIONS
    # ========================================================

    def show_certifications(self):
        self.current_page = "Certifications"
        self.set_active_nav("Certifications")
        self.clear_content()

        self.page_header(
            "Certifications",
            "Track your professional certifications and connect them to your career profile."
        )

        container = tk.Frame(self.content, bg=BG)
        container.pack(
            fill="both",
            expand=True,
            padx=35
        )

        form_card = self.card(container, width=380)
        form_card.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        list_card = self.card(container)
        list_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            form_card,
            text="ADD CERTIFICATION",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 15)
        )

        fields = [
            ("Certification Name", "name"),
            ("Organization", "organization"),
            ("Issue Date", "issue_date"),
            ("Credential ID", "credential_id"),
            ("Credential URL", "credential_url"),
            ("Skills Covered", "skills")
        ]

        entries = {}

        for display, key in fields:
            tk.Label(
                form_card,
                text=display,
                font=("Segoe UI", 8, "bold"),
                bg=CARD,
                fg=MUTED
            ).pack(
                anchor="w",
                padx=22,
                pady=(4, 3)
            )

            e = self.entry(form_card, "", 32)
            e.pack(
                fill="x",
                padx=22,
                pady=(0, 7)
            )

            entries[key] = e

        tk.Label(
            form_card,
            text="Status",
            font=("Segoe UI", 8, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=22,
            pady=(4, 3)
        )

        status_var = tk.StringVar(value="Completed")

        status_box = ttk.Combobox(
            form_card,
            textvariable=status_var,
            values=["Completed", "In Progress", "Planned"],
            state="readonly"
        )
        status_box.pack(
            fill="x",
            padx=22
        )

        self.button(
            form_card,
            "🏆  ADD CERTIFICATION",
            lambda: self.add_certification(entries, status_var)
        ).pack(
            fill="x",
            padx=22,
            pady=20
        )

        # List
        tk.Label(
            list_card,
            text="MY CERTIFICATIONS",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 10)
        )

        rows = self.db.execute(
            "SELECT * FROM certifications ORDER BY id DESC",
            fetch=True
        )

        tree_frame = tk.Frame(list_card, bg=CARD)
        tree_frame.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 20)
        )

        columns = (
            "name",
            "organization",
            "date",
            "status"
        )

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings"
        )

        tree.heading("name", text="Certification")
        tree.heading("organization", text="Organization")
        tree.heading("date", text="Issue Date")
        tree.heading("status", text="Status")

        tree.column("name", width=230)
        tree.column("organization", width=160)
        tree.column("date", width=100)
        tree.column("status", width=100)

        scroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scroll.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["name"],
                    row["organization"],
                    row["issue_date"],
                    row["status"]
                )
            )

    def add_certification(self, entries, status_var):

        name = entries["name"].get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the certification name."
            )
            return

        self.db.execute("""
            INSERT INTO certifications
            (name, organization, issue_date, credential_id,
             credential_url, skills, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            entries["organization"].get().strip(),
            entries["issue_date"].get().strip(),
            entries["credential_id"].get().strip(),
            entries["credential_url"].get().strip(),
            entries["skills"].get().strip(),
            status_var.get()
        ))

        # Automatically add certification skills
        skill_text = entries["skills"].get().strip()

        if skill_text:
            skills = [
                x.strip()
                for x in re.split(r",|\n", skill_text)
                if x.strip()
            ]

            for skill in skills:
                self.db.execute(
                    "INSERT OR IGNORE INTO skills(skill) VALUES (?)",
                    (skill,)
                )

                row = self.db.execute(
                    "SELECT id FROM skills WHERE skill=?",
                    (skill,),
                    fetch=True
                )

                if row:
                    self.db.execute("""
                        INSERT OR IGNORE INTO profile_skills
                        (profile_id, skill_id)
                        VALUES (1, ?)
                    """, (row[0]["id"],))

        messagebox.showinfo(
            "Certification Added",
            "Certification added successfully.\n"
            "Covered skills were also connected to your profile."
        )

        self.show_certifications()

    # ========================================================
    # LEARNING HUB
    # ========================================================

    def show_learning(self):
        self.current_page = "Learning Hub"
        self.set_active_nav("Learning Hub")
        self.clear_content()

        self.page_header(
            "Learning Hub",
            f"Short role-focused learning material for {self.current_role}."
        )

        role = self.current_role

        rows = self.db.execute("""
            SELECT lt.*, COALESCE(lp.completed, 0) AS completed
            FROM learning_topics lt
            LEFT JOIN learning_progress lp
            ON lt.id = lp.topic_id
            WHERE lt.role=?
            ORDER BY lt.id
        """, (role,), fetch=True)

        # If custom role
        if not rows:
            for topic, material in GENERIC_TOPICS:
                self.db.execute("""
                    INSERT INTO learning_topics(role, topic, material)
                    VALUES (?, ?, ?)
                """, (
                    role,
                    topic,
                    material
                ))

            rows = self.db.execute("""
                SELECT lt.*, COALESCE(lp.completed, 0) AS completed
                FROM learning_topics lt
                LEFT JOIN learning_progress lp
                ON lt.id = lp.topic_id
                WHERE lt.role=?
                ORDER BY lt.id
            """, (role,), fetch=True)

        completed = sum(
            1 for r in rows if r["completed"]
        )

        header = self.card(self.content)
        header.pack(
            fill="x",
            padx=35,
            pady=(0, 15)
        )

        hinner = tk.Frame(header, bg=CARD)
        hinner.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Label(
            hinner,
            text=f"{completed}/{len(rows)} topics completed",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(side="left")

        percent = (
            completed / len(rows) * 100
            if rows else 0
        )

        self.progress_bar(
            hinner,
            percent,
            width=300
        ).pack(
            side="left",
            padx=20
        )

        tk.Label(
            hinner,
            text=f"{percent:.0f}%",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=ACCENT2
        ).pack(side="left")

        # Scrollable
        outer = tk.Frame(self.content, bg=BG)
        outer.pack(
            fill="both",
            expand=True,
            padx=35
        )

        canvas = tk.Canvas(
            outer,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = tk.Frame(
            canvas,
            bg=BG
        )

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for row in rows:
            self.create_learning_card(
                scroll_frame,
                row
            )

    def create_learning_card(self, parent, row):

        frame = self.card(parent)
        frame.pack(
            fill="x",
            pady=6
        )

        icon = "✓" if row["completed"] else "📚"

        tk.Label(
            frame,
            text=icon,
            font=("Segoe UI", 18),
            bg=CARD,
            fg=GREEN if row["completed"] else ACCENT2
        ).pack(
            side="left",
            padx=18,
            pady=15
        )

        info = tk.Frame(frame, bg=CARD)
        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=15
        )

        tk.Label(
            info,
            text=row["topic"],
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            info,
            text=row["material"],
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED,
            wraplength=650,
            justify="left"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        if row["completed"]:
            btn_text = "✓ COMPLETED"
        else:
            btn_text = "READ & COMPLETE"

        self.button(
            frame,
            btn_text,
            lambda r=row: self.open_learning(r),
            primary=not bool(row["completed"])
        ).pack(
            side="right",
            padx=18
        )

    def open_learning(self, row):

        popup = tk.Toplevel(self)
        popup.title(row["topic"])
        popup.geometry("650x500")
        popup.configure(bg=BG)
        popup.transient(self)

        tk.Label(
            popup,
            text=row["topic"],
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        tk.Label(
            popup,
            text=f"Role: {row['role']}",
            font=("Segoe UI", 9),
            bg=BG,
            fg=ACCENT2
        ).pack(
            anchor="w",
            padx=30
        )

        material = scrolledtext.ScrolledText(
            popup,
            bg=CARD,
            fg=TEXT,
            insertbackground=WHITE,
            font=("Segoe UI", 11),
            relief="flat",
            wrap="word",
            padx=20,
            pady=20
        )
        material.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        material.insert(
            "1.0",
            f"""
{row['topic']}

WHAT YOU SHOULD KNOW

{row['material']}

INTERVIEW TIP

When answering an interview question about this topic:

• Start with a simple definition.
• Explain the important concept.
• Give a practical example.
• Explain why it matters.
• Connect it to the role of {row['role']}.

PRACTICE

After completing this topic, return to Mock Interview and
practice questions related to your target role.
"""
        )

        material.config(state="disabled")

        def complete():
            self.db.execute("""
                INSERT OR REPLACE INTO learning_progress
                (topic_id, completed)
                VALUES (?, 1)
            """, (row["id"],))

            popup.destroy()
            self.show_learning()

        self.button(
            popup,
            "✓ MARK AS COMPLETED",
            complete
        ).pack(
            pady=(0, 25)
        )

    # ========================================================
    # MOCK INTERVIEW
    # ========================================================

    def show_interview(self):
        self.current_page = "Mock Interview"
        self.set_active_nav("Mock Interview")
        self.clear_content()

        self.page_header(
            "Mock Interview",
            "Practice role-specific questions and receive instant response analysis."
        )

        setup = self.card(self.content)
        setup.pack(
            fill="x",
            padx=35,
            pady=5
        )

        inner = tk.Frame(setup, bg=CARD)
        inner.pack(
            fill="x",
            padx=30,
            pady=25
        )

        tk.Label(
            inner,
            text="CONFIGURE YOUR INTERVIEW",
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=TEXT
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 20)
        )

        # Role
        tk.Label(
            inner,
            text="Target Role",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).grid(row=1, column=0, sticky="w")

        role_var = tk.StringVar(value=self.current_role)

        roles = list(ROLE_DATA.keys())

        if self.current_role not in roles:
            roles.append(self.current_role)

        role_box = ttk.Combobox(
            inner,
            textvariable=role_var,
            values=roles,
            state="readonly",
            width=25
        )
        role_box.grid(
            row=2,
            column=0,
            padx=(0, 15),
            pady=6
        )

        # Type
        tk.Label(
            inner,
            text="Interview Type",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).grid(row=1, column=1, sticky="w")

        type_var = tk.StringVar(value="Mixed")

        type_box = ttk.Combobox(
            inner,
            textvariable=type_var,
            values=[
                "Mixed",
                "Technical",
                "Behavioral",
                "Scenario Based",
                "HR"
            ],
            state="readonly",
            width=20
        )
        type_box.grid(
            row=2,
            column=1,
            padx=(0, 15),
            pady=6
        )

        # Difficulty
        tk.Label(
            inner,
            text="Difficulty",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).grid(row=1, column=2, sticky="w")

        difficulty_var = tk.StringVar(value="Intermediate")

        difficulty_box = ttk.Combobox(
            inner,
            textvariable=difficulty_var,
            values=[
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            state="readonly",
            width=18
        )
        difficulty_box.grid(
            row=2,
            column=2,
            padx=(0, 15),
            pady=6
        )

        # Number
        tk.Label(
            inner,
            text="Questions",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        ).grid(row=1, column=3, sticky="w")

        count_var = tk.StringVar(value="5")

        count_box = ttk.Combobox(
            inner,
            textvariable=count_var,
            values=["3", "5", "7", "10"],
            state="readonly",
            width=10
        )
        count_box.grid(
            row=2,
            column=3,
            pady=6
        )

        for i in range(4):
            inner.columnconfigure(i, weight=1)

        self.button(
            setup,
            "🎤  START MOCK INTERVIEW",
            lambda: self.start_interview(
                role_var.get(),
                type_var.get(),
                difficulty_var.get(),
                int(count_var.get())
            )
        ).pack(
            anchor="e",
            padx=30,
            pady=(0, 25)
        )

        # Previous interviews
        history = self.card(self.content)
        history.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        tk.Label(
            history,
            text="RECENT INTERVIEWS",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 10)
        )

        rows = self.db.execute("""
            SELECT role, interview_type, difficulty, date, total_score
            FROM interviews
            ORDER BY id DESC
            LIMIT 8
        """, fetch=True)

        if not rows:
            tk.Label(
                history,
                text="No interviews completed yet. Start your first interview above.",
                font=("Segoe UI", 10),
                bg=CARD,
                fg=MUTED
            ).pack(
                anchor="w",
                padx=22
            )
        else:
            tree = ttk.Treeview(
                history,
                columns=("role", "type", "difficulty", "date", "score"),
                show="headings"
            )

            for col, title in [
                ("role", "Role"),
                ("type", "Type"),
                ("difficulty", "Difficulty"),
                ("date", "Date"),
                ("score", "Score")
            ]:
                tree.heading(col, text=title)

            tree.column("role", width=180)
            tree.column("type", width=120)
            tree.column("difficulty", width=110)
            tree.column("date", width=160)
            tree.column("score", width=80)

            tree.pack(
                fill="both",
                expand=True,
                padx=22,
                pady=(0, 20)
            )

            for row in rows:
                tree.insert(
                    "",
                    "end",
                    values=(
                        row["role"],
                        row["interview_type"],
                        row["difficulty"],
                        row["date"],
                        f"{row['total_score']:.0f}%"
                    )
                )

    def start_interview(self, role, interview_type, difficulty, count):

        self.current_role = role
        self.interview_role = role
        self.interview_type = interview_type
        self.interview_difficulty = difficulty

        if role in ROLE_DATA:
            questions = ROLE_DATA[role]["questions"].copy()
        else:
            questions = GENERIC_QUESTIONS.copy()

        random.shuffle(questions)

        self.interview_questions = questions[:count]
        self.current_question_index = 0
        self.current_interview_answers = []
        self.interview_start_time = datetime.now()

        self.show_interview_question()

    def show_interview_question(self):

        self.clear_content()

        number = self.current_question_index + 1
        total = len(self.interview_questions)

        self.page_header(
            f"Mock Interview • {self.interview_role}",
            f"{self.interview_type} interview • {self.interview_difficulty} • Question {number} of {total}"
        )

        container = tk.Frame(
            self.content,
            bg=BG
        )
        container.pack(
            fill="both",
            expand=True,
            padx=35
        )

        card = self.card(container)
        card.pack(
            fill="both",
            expand=True
        )

        top = tk.Frame(card, bg=CARD)
        top.pack(
            fill="x",
            padx=30,
            pady=25
        )

        tk.Label(
            top,
            text=f"QUESTION {number}/{total}",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=ACCENT2
        ).pack(anchor="w")

        question = self.interview_questions[
            self.current_question_index
        ]

        tk.Label(
            top,
            text=question["q"],
            font=("Segoe UI", 19, "bold"),
            bg=CARD,
            fg=TEXT,
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            pady=(12, 0)
        )

        answer_label = tk.Label(
            card,
            text="YOUR RESPONSE",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        )
        answer_label.pack(
            anchor="w",
            padx=30
        )

        answer = tk.Text(
            card,
            bg=CARD2,
            fg=TEXT,
            insertbackground=WHITE,
            font=("Segoe UI", 11),
            relief="flat",
            wrap="word",
            padx=15,
            pady=15
        )
        answer.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        answer.focus_set()

        bottom = tk.Frame(card, bg=CARD)
        bottom.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        tk.Label(
            bottom,
            text="Tip: explain your reasoning, use relevant technical terms and provide a practical example.",
            font=("Segoe UI", 8),
            bg=CARD,
            fg=MUTED
        ).pack(side="left")

        self.button(
            bottom,
            "SUBMIT ANSWER  →",
            lambda: self.submit_answer(answer.get("1.0", "end").strip())
        ).pack(side="right")

    def submit_answer(self, answer):

        if not answer.strip():
            messagebox.showwarning(
                "Empty Answer",
                "Please provide an answer before submitting."
            )
            return

        question = self.interview_questions[
            self.current_question_index
        ]

        analysis = self.analyze_answer(
            answer,
            question
        )

        self.current_interview_answers.append({
            "question": question["q"],
            "answer": answer,
            **analysis
        })

        self.show_answer_feedback(analysis, question)

    # ========================================================
    # ANSWER ANALYSIS
    # ========================================================

    def analyze_answer(self, answer, question):

        clean = answer.lower()

        keywords = question["keywords"]

        found = []
        missing = []

        for keyword in keywords:
            if re.search(
                r"\b" + re.escape(keyword.lower()) + r"\b",
                clean
            ):
                found.append(keyword)
            else:
                missing.append(keyword)

        keyword_score = (
            len(found) / len(keywords) * 100
            if keywords else 60
        )

        word_count = len(re.findall(r"\b\w+\b", answer))

        if word_count < 15:
            completeness = 35
        elif word_count < 35:
            completeness = 60
        elif word_count < 80:
            completeness = 85
        elif word_count < 140:
            completeness = 92
        else:
            completeness = 78

        structure_words = [
            "first", "then", "finally",
            "because", "therefore",
            "however", "for example",
            "such as", "step"
        ]

        structure_count = sum(
            1 for x in structure_words
            if x in clean
        )

        relevance = min(
            100,
            40 + keyword_score * 0.6
        )

        technical = min(
            100,
            keyword_score * 0.8 + structure_count * 5
        )

        if structure_count >= 2:
            confidence = 85
        elif structure_count == 1:
            confidence = 72
        else:
            confidence = 60

        filler_words = [
            "maybe",
            "i think",
            "basically",
            "like",
            "probably",
            "not sure"
        ]

        filler_count = sum(
            clean.count(x)
            for x in filler_words
        )

        confidence -= min(
            25,
            filler_count * 5
        )

        confidence = max(20, min(100, confidence))

        score = (
            technical * 0.35 +
            relevance * 0.25 +
            completeness * 0.20 +
            confidence * 0.20
        )

        feedback = []

        if technical >= 75:
            feedback.append(
                "You included several relevant technical concepts."
            )
        else:
            feedback.append(
                "Add more role-specific technical concepts."
            )

        if completeness >= 75:
            feedback.append(
                "Your response provides reasonable detail."
            )
        else:
            feedback.append(
                "Your answer is short. Explain the reasoning and steps."
            )

        if confidence < 65:
            feedback.append(
                "Avoid uncertain or filler phrases and answer more directly."
            )
        else:
            feedback.append(
                "Your response has a reasonably confident tone."
            )

        if structure_count == 0:
            feedback.append(
                "Try using a clear structure such as first, then, finally."
            )

        feedback_text = " ".join(feedback)

        return {
            "score": score,
            "technical": technical,
            "relevance": relevance,
            "completeness": completeness,
            "confidence": confidence,
            "feedback": feedback_text,
            "found_keywords": found,
            "missing_keywords": missing
        }

    def show_answer_feedback(self, analysis, question):

        popup = tk.Toplevel(self)
        popup.title("AI Response Analysis")
        popup.geometry("720x650")
        popup.configure(bg=BG)
        popup.transient(self)
        popup.grab_set()

        tk.Label(
            popup,
            text="AI RESPONSE ANALYSIS",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 3)
        )

        tk.Label(
            popup,
            text=f"Question {self.current_question_index + 1}",
            font=("Segoe UI", 9),
            bg=BG,
            fg=ACCENT2
        ).pack(
            anchor="w",
            padx=30
        )

        score_frame = self.card(popup)
        score_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )

        tk.Label(
            score_frame,
            text=f"{analysis['score']:.0f}%",
            font=("Segoe UI", 34, "bold"),
            bg=CARD,
            fg=GREEN if analysis["score"] >= 70 else YELLOW
        ).pack(
            side="left",
            padx=25,
            pady=20
        )

        tk.Label(
            score_frame,
            text=self.score_label(analysis["score"]),
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            side="left"
        )

        metrics = tk.Frame(popup, bg=BG)
        metrics.pack(
            fill="x",
            padx=30
        )

        metric_values = [
            ("Technical", analysis["technical"]),
            ("Relevance", analysis["relevance"]),
            ("Completeness", analysis["completeness"]),
            ("Confidence", analysis["confidence"])
        ]

        for title, value in metric_values:
            row = tk.Frame(metrics, bg=BG)
            row.pack(
                fill="x",
                pady=4
            )

            tk.Label(
                row,
                text=title,
                font=("Segoe UI", 9, "bold"),
                bg=BG,
                fg=MUTED,
                width=15,
                anchor="w"
            ).pack(side="left")

            self.progress_bar(
                row,
                value,
                width=300
            ).pack(side="left")

            tk.Label(
                row,
                text=f"{value:.0f}%",
                font=("Segoe UI", 9, "bold"),
                bg=BG,
                fg=TEXT
            ).pack(
                side="left",
                padx=10
            )

        feedback = self.card(popup)
        feedback.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        tk.Label(
            feedback,
            text="COACH FEEDBACK",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        tk.Label(
            feedback,
            text=analysis["feedback"],
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED,
            wraplength=620,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        found_text = (
            "Detected: " +
            ", ".join(analysis["found_keywords"])
            if analysis["found_keywords"]
            else "No expected keywords detected."
        )

        missing_text = (
            "Consider including: " +
            ", ".join(analysis["missing_keywords"])
            if analysis["missing_keywords"]
            else "All major expected concepts detected."
        )

        tk.Label(
            feedback,
            text=found_text,
            font=("Segoe UI", 8),
            bg=CARD,
            fg=GREEN
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 2)
        )

        tk.Label(
            feedback,
            text=missing_text,
            font=("Segoe UI", 8),
            bg=CARD,
            fg=YELLOW
        ).pack(
            anchor="w",
            padx=20
        )

        self.button(
            popup,
            "CONTINUE  →",
            lambda: self.continue_interview(popup)
        ).pack(
            pady=(0, 25)
        )

    def continue_interview(self, popup):

        popup.destroy()

        self.current_question_index += 1

        if self.current_question_index >= len(
            self.interview_questions
        ):
            self.finish_interview()
        else:
            self.show_interview_question()

    def score_label(self, score):
        if score >= 85:
            return "Excellent response"
        if score >= 70:
            return "Good response"
        if score >= 55:
            return "Needs improvement"
        return "Needs significant improvement"

    # ========================================================
    # FINISH INTERVIEW
    # ========================================================

    def finish_interview(self):

        answers = self.current_interview_answers

        if not answers:
            return

        avg_score = statistics.mean(
            [a["score"] for a in answers]
        )

        avg_technical = statistics.mean(
            [a["technical"] for a in answers]
        )

        avg_relevance = statistics.mean(
            [a["relevance"] for a in answers]
        )

        avg_completeness = statistics.mean(
            [a["completeness"] for a in answers]
        )

        avg_confidence = statistics.mean(
            [a["confidence"] for a in answers]
        )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cur = self.db.execute("""
            INSERT INTO interviews
            (role, interview_type, difficulty, date,
             total_score, communication, technical,
             relevance, completeness, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.interview_role,
            self.interview_type,
            self.interview_difficulty,
            now,
            avg_score,
            avg_confidence,
            avg_technical,
            avg_relevance,
            avg_completeness,
            avg_confidence
        ))

        interview_id = cur.lastrowid

        for answer in answers:
            self.db.execute("""
                INSERT INTO interview_answers
                (interview_id, question, answer, score,
                 technical, relevance, completeness,
                 confidence, feedback, missing_keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                interview_id,
                answer["question"],
                answer["answer"],
                answer["score"],
                answer["technical"],
                answer["relevance"],
                answer["completeness"],
                answer["confidence"],
                answer["feedback"],
                ", ".join(answer["missing_keywords"])
            ))

        self.show_interview_result(
            avg_score,
            avg_technical,
            avg_relevance,
            avg_completeness,
            avg_confidence
        )

    def show_interview_result(
        self,
        score,
        technical,
        relevance,
        completeness,
        confidence
    ):

        self.clear_content()

        self.page_header(
            "Interview Complete 🎉",
            "Your performance has been analyzed and saved to your interview history."
        )

        card = self.card(self.content)
        card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=5
        )

        tk.Label(
            card,
            text=f"{score:.0f}%",
            font=("Segoe UI", 55, "bold"),
            bg=CARD,
            fg=GREEN if score >= 70 else YELLOW
        ).pack(
            pady=(35, 0)
        )

        tk.Label(
            card,
            text=self.score_label(score),
            font=("Segoe UI", 16, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            pady=5
        )

        tk.Label(
            card,
            text=f"{len(self.current_interview_answers)} questions analyzed",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED
        ).pack()

        metrics = tk.Frame(card, bg=CARD)
        metrics.pack(
            fill="x",
            padx=100,
            pady=30
        )

        for title, value in [
            ("Technical Knowledge", technical),
            ("Relevance", relevance),
            ("Completeness", completeness),
            ("Confidence", confidence)
        ]:
            col = tk.Frame(metrics, bg=CARD)
            col.pack(
                side="left",
                fill="both",
                expand=True,
                padx=10
            )

            tk.Label(
                col,
                text=title,
                font=("Segoe UI", 9),
                bg=CARD,
                fg=MUTED
            ).pack()

            tk.Label(
                col,
                text=f"{value:.0f}%",
                font=("Segoe UI", 20, "bold"),
                bg=CARD,
                fg=TEXT
            ).pack(
                pady=5
            )

            self.progress_bar(
                col,
                value,
                width=150
            ).pack()

        # Weak areas
        weak = []

        if technical < 70:
            weak.append("technical knowledge")
        if relevance < 70:
            weak.append("answer relevance")
        if completeness < 70:
            weak.append("answer completeness")
        if confidence < 70:
            weak.append("communication/confidence")

        if weak:
            recommendation = (
                "Focus next on: " +
                ", ".join(weak) +
                ". Visit Learning Hub and practice again."
            )
        else:
            recommendation = (
                "Excellent! Your main dimensions are above 70%. "
                "Try a harder interview to challenge yourself."
            )

        rec = tk.Label(
            card,
            text="🎯  " + recommendation,
            font=("Segoe UI", 10, "bold"),
            bg=CARD2,
            fg=TEXT,
            wraplength=700,
            padx=20,
            pady=15,
            justify="left"
        )
        rec.pack(
            fill="x",
            padx=80
        )

        buttons = tk.Frame(card, bg=CARD)
        buttons.pack(pady=30)

        self.button(
            buttons,
            "📊 VIEW ANALYTICS",
            self.show_analytics
        ).pack(
            side="left",
            padx=5
        )

        self.button(
            buttons,
            "🎤 TRY AGAIN",
            self.show_interview,
            primary=False
        ).pack(
            side="left",
            padx=5
        )

        self.button(
            buttons,
            "🏠 DASHBOARD",
            self.show_dashboard,
            primary=False
        ).pack(
            side="left",
            padx=5
        )

    # ========================================================
    # ANALYTICS
    # ========================================================

    def show_analytics(self):
        self.current_page = "Analytics"
        self.set_active_nav("Analytics")
        self.clear_content()

        self.page_header(
            "Interview Analytics",
            "Understand how your responses are improving over time."
        )

        rows = self.db.execute("""
            SELECT * FROM interviews
            ORDER BY id ASC
        """, fetch=True)

        if not rows:
            empty = self.card(self.content)
            empty.pack(
                fill="both",
                expand=True,
                padx=35,
                pady=5
            )

            tk.Label(
                empty,
                text="📊",
                font=("Segoe UI", 40),
                bg=CARD,
                fg=ACCENT2
            ).pack(pady=(100, 10))

            tk.Label(
                empty,
                text="No interview data yet",
                font=("Segoe UI", 18, "bold"),
                bg=CARD,
                fg=TEXT
            ).pack()

            tk.Label(
                empty,
                text="Complete your first mock interview to unlock detailed analytics.",
                font=("Segoe UI", 10),
                bg=CARD,
                fg=MUTED
            ).pack(pady=8)

            self.button(
                empty,
                "START FIRST INTERVIEW",
                self.show_interview
            ).pack(pady=20)

            return

        latest = rows[-1]

        # Summary cards
        stats_frame = tk.Frame(
            self.content,
            bg=BG
        )
        stats_frame.pack(
            fill="x",
            padx=35
        )

        self.stat_card(
            stats_frame,
            "INTERVIEWS",
            str(len(rows)),
            "Completed",
            BLUE
        )

        avg = statistics.mean(
            [r["total_score"] for r in rows]
        )

        self.stat_card(
            stats_frame,
            "AVERAGE",
            f"{avg:.0f}%",
            "Overall score",
            GREEN
        )

        self.stat_card(
            stats_frame,
            "LATEST",
            f"{latest['total_score']:.0f}%",
            "Most recent",
            ACCENT2
        )

        improvement = (
            latest["total_score"] -
            rows[0]["total_score"]
        )

        self.stat_card(
            stats_frame,
            "IMPROVEMENT",
            f"{improvement:+.0f}%",
            "Since first interview",
            YELLOW
        )

        # Main analytics
        main = tk.Frame(
            self.content,
            bg=BG
        )
        main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        graph_card = self.card(main)
        graph_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            graph_card,
            text="PERFORMANCE TREND",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        canvas = tk.Canvas(
            graph_card,
            bg=CARD,
            highlightthickness=0
        )
        canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.draw_chart(
            canvas,
            [r["total_score"] for r in rows]
        )

        analysis_card = self.card(main)
        analysis_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        tk.Label(
            analysis_card,
            text="RESPONSE PROFILE",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        latest_metrics = [
            ("Technical Knowledge", latest["technical"]),
            ("Communication", latest["communication"]),
            ("Relevance", latest["relevance"]),
            ("Completeness", latest["completeness"]),
            ("Confidence", latest["confidence"])
        ]

        for title, value in latest_metrics:
            row = tk.Frame(
                analysis_card,
                bg=CARD
            )
            row.pack(
                fill="x",
                padx=20,
                pady=7
            )

            tk.Label(
                row,
                text=title,
                font=("Segoe UI", 8, "bold"),
                bg=CARD,
                fg=MUTED,
                width=20,
                anchor="w"
            ).pack(side="left")

            self.progress_bar(
                row,
                value,
                width=170
            ).pack(side="left")

            tk.Label(
                row,
                text=f"{value:.0f}%",
                font=("Segoe UI", 9, "bold"),
                bg=CARD,
                fg=TEXT
            ).pack(
                side="left",
                padx=8
            )

        # Detailed history
        history_card = self.card(self.content)
        history_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 20)
        )

        tk.Label(
            history_card,
            text="INTERVIEW HISTORY",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        tree = ttk.Treeview(
            history_card,
            columns=(
                "id",
                "role",
                "type",
                "difficulty",
                "date",
                "score"
            ),
            show="headings"
        )

        headings = [
            ("id", "#"),
            ("role", "Role"),
            ("type", "Type"),
            ("difficulty", "Difficulty"),
            ("date", "Date"),
            ("score", "Score")
        ]

        for col, title in headings:
            tree.heading(col, text=title)

        tree.column("id", width=45)
        tree.column("role", width=180)
        tree.column("type", width=110)
        tree.column("difficulty", width=110)
        tree.column("date", width=160)
        tree.column("score", width=80)

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        for r in reversed(rows):
            tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["role"],
                    r["interview_type"],
                    r["difficulty"],
                    r["date"],
                    f"{r['total_score']:.0f}%"
                )
            )

    # ========================================================
    # READINESS
    # ========================================================

    def calculate_readiness(self):

        profile = self.get_profile()

        profile_score = 0

        if profile:
            fields = [
                "name",
                "email",
                "college",
                "degree",
                "target_role",
                "objective"
            ]

            completed = sum(
                1
                for field in fields
                if profile[field]
            )

            profile_score = completed / len(fields) * 100

        skills = self.get_profile_skills()

        skill_score = min(
            100,
            len(skills) * 10
        )

        cert_count = self.db.execute(
            "SELECT COUNT(*) AS c FROM certifications",
            fetch=True
        )[0]["c"]

        cert_score = min(
            100,
            cert_count * 25
        )

        interviews = self.db.execute("""
            SELECT total_score
            FROM interviews
            ORDER BY id DESC
            LIMIT 5
        """, fetch=True)

        interview_score = (
            statistics.mean(
                [r["total_score"] for r in interviews]
            )
            if interviews else 0
        )

        topics = self.db.execute(
            "SELECT COUNT(*) AS c FROM learning_topics WHERE role=?",
            (self.current_role,),
            fetch=True
        )[0]["c"]

        completed_topics = self.db.execute("""
            SELECT COUNT(*) AS c
            FROM learning_progress lp
            JOIN learning_topics lt
            ON lp.topic_id = lt.id
            WHERE lt.role=? AND lp.completed=1
        """, (self.current_role,), fetch=True)[0]["c"]

        learning_score = (
            completed_topics / topics * 100
            if topics else 0
        )

        readiness = (
            profile_score * 0.20 +
            skill_score * 0.15 +
            cert_score * 0.10 +
            interview_score * 0.40 +
            learning_score * 0.15
        )

        return min(100, readiness)

    def readiness_status(self, score):
        if score >= 85:
            return "Interview Ready"
        if score >= 70:
            return "Strong Progress"
        if score >= 50:
            return "Developing"
        return "Getting Started"

    # ========================================================
    # DASHBOARD STATS
    # ========================================================

    def get_dashboard_stats(self):

        interviews = self.db.execute(
            "SELECT COUNT(*) AS c FROM interviews",
            fetch=True
        )[0]["c"]

        rows = self.db.execute(
            "SELECT total_score FROM interviews",
            fetch=True
        )

        average = (
            statistics.mean(
                [r["total_score"] for r in rows]
            )
            if rows else 0
        )

        skills = len(
            self.get_profile_skills()
        )

        certifications = self.db.execute(
            "SELECT COUNT(*) AS c FROM certifications",
            fetch=True
        )[0]["c"]

        return {
            "interviews": interviews,
            "average": average,
            "skills": skills,
            "certifications": certifications
        }

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    def get_recommendations(self):

        recommendations = []

        profile = self.get_profile()

        if not profile:
            recommendations.append(
                "Complete your candidate profile first."
            )
        else:
            missing = []

            for field, name in [
                ("email", "email"),
                ("college", "college"),
                ("degree", "degree"),
                ("objective", "career objective")
            ]:
                if not profile[field]:
                    missing.append(name)

            if missing:
                recommendations.append(
                    "Complete your profile: " +
                    ", ".join(missing) + "."
                )

        skills = self.get_profile_skills()

        if len(skills) < 5:
            recommendations.append(
                "Add more technical skills to improve your role matching."
            )

        certs = self.db.execute(
            "SELECT COUNT(*) AS c FROM certifications",
            fetch=True
        )[0]["c"]

        if certs == 0:
            recommendations.append(
                "Add your certifications to strengthen your career profile."
            )

        interviews = self.db.execute("""
            SELECT *
            FROM interviews
            ORDER BY id DESC
            LIMIT 1
        """, fetch=True)

        if not interviews:
            recommendations.append(
                f"Take your first {self.current_role} mock interview."
            )
        else:
            latest = interviews[0]

            if latest["technical"] < 70:
                recommendations.append(
                    "Improve technical knowledge through the Learning Hub."
                )

            if latest["communication"] < 70:
                recommendations.append(
                    "Practice clearer and more structured responses."
                )

            if latest["completeness"] < 70:
                recommendations.append(
                    "Give more detailed answers with examples and reasoning."
                )

            if latest["confidence"] < 70:
                recommendations.append(
                    "Reduce filler phrases and answer more directly."
                )

            if latest["total_score"] >= 80:
                recommendations.append(
                    "Try an Advanced interview to challenge yourself."
                )

        if not recommendations:
            recommendations.append(
                "You're progressing well. Keep practicing consistently."
            )

        return recommendations

    # ========================================================
    # CLOSE
    # ========================================================

    def on_close(self):
        try:
            self.db.close()
        except:
            pass

        self.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    app = InterviewCoach()
    app.mainloop()  

