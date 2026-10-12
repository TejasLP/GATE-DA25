import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost", user="my_user", password="your_strong_password"
)
cursor = db.cursor()

# Read the contents of q22.sql
with open("q22.sql", "r") as file:
  sql_script = file.read()

# Split the script into individual statements by semicolon
statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]

# Execute each statement one by one
for statement in statements:
  cursor.execute(statement)

  # If the statement produces rows (like a SELECT query), fetch and print them
  if cursor.with_rows:
    print("--- Query Output ---")
    for row in cursor.fetchall():
      print(row[0])

# Commit changes and close connections
db.commit()
cursor.close()
db.close()
