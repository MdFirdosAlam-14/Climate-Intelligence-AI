"""Local SQLite authentication and audit utilities."""
import sqlite3, hashlib, os, re, time, hmac
DB = "app.db"

def _c():
    c = sqlite3.connect(DB, timeout=20)
    c.execute("PRAGMA busy_timeout=20000")
    return c

def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)

def init():
    with _c() as c:
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("CREATE TABLE IF NOT EXISTS users(u TEXT PRIMARY KEY, salt BLOB, h BLOB, role TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS audit(t TEXT, u TEXT, a TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS fails(u TEXT PRIMARY KEY, n INTEGER, t REAL)")
        exists = c.execute("SELECT 1 FROM users LIMIT 1").fetchone()
    if not exists:
        register("admin", "Admin@123", "admin")

def log(user, action):
    with _c() as c:
        c.execute("INSERT INTO audit VALUES(?,?,?)", (time.strftime("%Y-%m-%d %H:%M:%S"), user, action))

def register(user, password, role="user"):
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", user or ""):
        return False, "Username 3-20 chars (letters/digits/_)"
    if len(password or "") < 8:
        return False, "Password kam se kam 8 chars ka ho"
    salt = os.urandom(16)
    try:
        with _c() as c:
            c.execute("INSERT INTO users VALUES(?,?,?,?)", (user, salt, _hash(password, salt), role))
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    log(user, "register")
    return True, "Registered. Ab login karo."

def login(user, password):
    # Keep each transaction short. Never open a second writer connection while
    # the authentication transaction is still active (the old lock bug).
    with _c() as c:
        fail = c.execute("SELECT n,t FROM fails WHERE u=?", (user,)).fetchone()
        if fail and fail[0] >= 5 and time.time() - fail[1] < 300:
            return False, "5 galat attempts: 5 min ke liye lock"
        row = c.execute("SELECT salt,h,role FROM users WHERE u=?", (user,)).fetchone()
        valid = bool(row and hmac.compare_digest(_hash(password or "", row[0]), row[1]))
        if valid:
            c.execute("DELETE FROM fails WHERE u=?", (user,))
            role = row[2]
        else:
            c.execute("INSERT INTO fails VALUES(?,1,?) ON CONFLICT(u) DO UPDATE SET n=n+1,t=excluded.t", (user or "?", time.time()))
            role = None
    log(user or "?", "login ok" if valid else "login FAILED")
    return (True, role) if valid else (False, "Galat username/password")

def audit_log():
    with _c() as c:
        return c.execute("SELECT * FROM audit ORDER BY t DESC LIMIT 200").fetchall()

def plausible(row):
    return -60 <= row.tmin <= row.tmax <= 56 and 0 <= row.rain <= 1000 and 0 <= row.wind <= 250
