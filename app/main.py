from flask import Flask, render_template, request, send_file
import sqlite3, csv, os

app = Flask(__name__)

def query_db(keyword):
    conn = sqlite3.connect('../db/app.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE name LIKE ? OR category LIKE ? OR description LIKE ?",
                (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/', methods=['GET', 'POST'])
def index():
    rows = []
    keyword = ''
    if request.method == 'POST':
        keyword = request.form['keyword']
        rows = query_db(keyword)
    return render_template('index.html', rows=rows, keyword=keyword)

@app.route('/export', methods=['POST'])
def export_csv():
    keyword = request.form['keyword']
    rows = query_db(keyword)
    os.makedirs('../export', exist_ok=True)
    filepath = f"../export/result.csv"
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'category', 'description'])
        writer.writerows(rows)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
