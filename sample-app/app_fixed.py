import sqlite3, subprocess, hashlib, os

API_KEY = os.environ.get("API_KEY")           # read from environment, not hardcoded

def get_user(name):
    conn = sqlite3.connect("db.sqlite")
    return conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()

def run(cmd_list):
    return subprocess.call(cmd_list, shell=False)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
