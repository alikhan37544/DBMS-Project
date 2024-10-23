import mysql.connector
from tkinter import Tk, Label, Button, Text, ttk, messagebox, StringVar


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

# Available countries
countries = {
    "Canada": "CA_videos",
    "United States": "US_videos",
    "Germany": "DE_videos",
    "France": "FR_videos",
    "Great Britain": "GB_videos",
    "India": "IN_videos",
    "Japan": "JP_videos",
    "South Korea": "KR_videos",
    "Mexico": "MX_videos",
    "Russia": "RU_videos"
}

# Function to execute SQL queries and display the result
def execute_query(query, country_table):
    try:
        cursor.execute(query.format(country_table=country_table))
        if query.lower().startswith('select'):
            results = cursor.fetchall()
            show_results(results, cursor.column_names)
        else:
            conn.commit()
            messagebox.showinfo("Success", "Query executed successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to display the results in a table
def show_results(data, columns):
    for widget in result_frame.winfo_children():
        widget.destroy()  # Clear previous results

    if not data:
        messagebox.showinfo("No Results", "Query executed successfully but returned no results.")
        return

    tree = ttk.Treeview(result_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, minwidth=100, width=150)
    for row in data:
        tree.insert('', 'end', values=row)
    tree.pack(expand=True, fill='both')

# Function to handle query execution
def run_query():
    query = query_text.get(1.0, 'end').strip()
    country = country_var.get()

    if query and country:
        country_table = countries[country]
        execute_query(query, country_table)
    else:
        messagebox.showerror("Error", "Please select a country and enter an SQL query.")

# Function to insert predefined queries into the query box
def insert_query(template):
    query_text.delete(1.0, 'end')
    query_text.insert('end', template)

# GUI Setup
root = Tk()
root.title("SQL Query Executor")
root.geometry("800x600")

# Country selection
country_var = StringVar()
country_label = Label(root, text="Select a country to query:")
country_label.pack(pady=10)

country_menu = ttk.Combobox(root, textvariable=country_var, values=list(countries.keys()), state="readonly")
country_menu.pack(pady=10)
country_menu.current(0)

# Query text box
query_label = Label(root, text="Enter your SQL query:")
query_label.pack(pady=10)

query_text = Text(root, height=6, width=80)
query_text.pack(pady=10)

# Query execution button
execute_button = Button(root, text="Execute Query", command=run_query)
execute_button.pack(pady=10)

# Frame to show query results
result_frame = ttk.Frame(root)
result_frame.pack(expand=True, fill='both', pady=10)

# Predefined query buttons
query_frame = ttk.Frame(root)
query_frame.pack(fill='x', pady=10)

predefined_queries = {
    "Select All": "SELECT * FROM {country_table} LIMIT 10;",
    "Count Rows": "SELECT COUNT(*) FROM {country_table};",
    "Top 10 Most Viewed": "SELECT title, views FROM {country_table} ORDER BY views DESC LIMIT 10;",
    "Insert Example": """INSERT INTO {country_table} (video_id, trending_date, title, channel_title, category_id, publish_time, tags, views, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, video_error_or_removed, description)
VALUES ('new_video', CURDATE(), 'New Video Title', 'New Channel', 10, NOW(), 'new_tag', 100, 10, 1, 2, 'https://example.com', 0, 0, 0, 'New video description');"""
}

for label, query in predefined_queries.items():
    button = Button(query_frame, text=label, command=lambda q=query: insert_query(q))
    button.pack(side='left', padx=5)

root.mainloop()

# Close the database connection when the window is closed
cursor.close()
conn.close()
