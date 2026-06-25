import psycopg2

conn = psycopg2.connect("postgresql://postgres:postgres20@localhost:5432/euklydia_prod")
cur = conn.cursor()

# ── Query 1: All tables ──────────────────────────────────────────────────────
print("=== QUERY 1: ALL TABLES ===")
cur.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
""")
tables = cur.fetchall()
for row in tables:
    print(row[0])

# ── Query 2: All columns ─────────────────────────────────────────────────────
print("\n=== QUERY 2: ALL COLUMNS ===")
cur.execute("""
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
""")
for row in cur.fetchall():
    print("|".join(str(x) if x is not None else "NULL" for x in row))

# ── Query 3: Foreign keys ────────────────────────────────────────────────────
print("\n=== QUERY 3: FOREIGN KEYS ===")
cur.execute("""
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name  AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
""")
for row in cur.fetchall():
    print("|".join(str(x) if x is not None else "NULL" for x in row))

cur.close()
conn.close()
print("\nDone.")
