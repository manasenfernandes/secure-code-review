def find_user(conn, name):
    conn.execute("SELECT * FROM users WHERE name = '" + name + "'")
