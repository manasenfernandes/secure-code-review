def find_user(conn, name):
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    conn.execute(query)
