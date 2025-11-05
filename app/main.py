from flask import Flask, render_template, request
import sqlite3, os

# --- 設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "DB", "date.db"))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
print("📁 DB_PATH =", DB_PATH)

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# --- DB検索関数 ---
def query_db(keyword):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT "group", number, name, enerc_kcal, prot_, fat_, choavlm, na, k, ca, mg, p, fe
        FROM items
        WHERE name LIKE ?
    """, (f'%{keyword}%',))
    rows = cur.fetchall()
    conn.close()
    return rows

# --- トップページ ---
@app.route('/', methods=['GET', 'POST'])
def index():
    rows = []
    keyword = ''
    if request.method == 'POST':
        keyword = request.form['keyword']
        rows = query_db(keyword)
    return render_template('index.html', rows=rows, keyword=keyword)
# # CSVエクスポート用
# @app.route('/export', methods=['POST'])
# def export_csv():
#     keyword = request.form['keyword']
#     rows = query_db(keyword)
#     os.makedirs('../export', exist_ok=True)
#     filepath = '../export/result.csv'
#     with open(filepath, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(['id', 'name', 'category', 'description'])
#         writer.writerows(rows)
#     return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
