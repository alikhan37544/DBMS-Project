import mysql.connector

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'ali',
    'password': 'admin',
    'database': 'youtube_trending'
}

# Establish connection to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Function to delete all category tables
def delete_category_tables():
    # Get all tables that match the pattern 'category_%'
    cursor.execute("SHOW TABLES LIKE 'category_%'")
    tables = cursor.fetchall()

    # Drop each category table
    for (table_name,) in tables:
        print(f"Dropping table {table_name}...")
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

# Function to delete all country tables
def delete_country_tables():
    # Get all tables that match the pattern '%_videos'
    cursor.execute("SHOW TABLES LIKE '%_videos'")
    tables = cursor.fetchall()

    # Drop each country table
    for (table_name,) in tables:
        print(f"Dropping table {table_name}...")
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

# Function to delete the video_categories table
def delete_video_categories():
    print("Dropping table video_categories...")
    cursor.execute("DROP TABLE IF EXISTS video_categories")
    conn.commit()

# Run the deletion process
delete_category_tables()  # Delete all category-specific tables
delete_country_tables()  # Delete all country-specific tables
delete_video_categories()  # Delete the video_categories table

# Close the database connection
cursor.close()
conn.close()

print("All tables have been dropped, and the database is now empty.")
