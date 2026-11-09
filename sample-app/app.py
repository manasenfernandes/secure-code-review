import sqlite3, subprocess, hashlib

API_KEY = "sk_live_1234567890abcdef"          # hardcoded secret

def get_user(name):
    conn = sqlite3.connect("db.sqlite")
    # SQL injection
    return conn.execute("SELECT * FROM users WHERE name = '" + name + "'").fetchall()

def run(cmd):
    return subprocess.call(cmd, shell=True)   # command injection

def hash_pw(pw):
    return hashlib.md5(pw.encode()).hexdigest()  # weak hash
