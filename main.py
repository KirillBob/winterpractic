from flask import Flask, request, redirect, send_file, Response
from database import *
import shutil
import json

db = Database(database="WinterPractic", user="postgres", password="kirill", host="localhost", port=5432)
head = ["name", "extension", "size", "path", "created_at", "updated_at", "comment"]
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        root = request.form.get('root')
        db.make_root(root)
        return redirect('/all')
    return """
        <form method='POST'>
        <div><label>Path: <input type='text' name='root'></label></div>
        </form>"""


@app.route("/all")
def get_data_all():
    cur = db.select()
    data = [{head[i]: row[i] for i in range(len(head))} for row in cur]
    json_data = json.dumps(data, default=str, sort_keys=False, indent=2, ensure_ascii=False)
    return Response(json_data, mimetype='application/json; charset=utf-8')

@app.route("/file", methods=['GET', 'POST'])
def form_file():
    if request.method == 'POST':
        path = request.form.get('path')
        cur = db.select(path)
        data = [{head[i]: row[i] for i in range(len(head))} for row in cur]
        json_data = json.dumps(data, default=str, sort_keys=False, indent=2, ensure_ascii=False)
        return Response(json_data, mimetype='application/json; charset=utf-8')
    return """
        <form method='POST'>
        <div><label>Path: <input type='text' name='path'></label></div>
        </form>"""

@app.route("/add", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        upload_path = request.form.get('path')
        file.save(os.path.join(upload_path, filename))
        db.write_sql(upload_path, file.filename)
    return '''
        <!doctype html>
        <title>Загрузить новый файл</title>
        <h1>Загрузить новый файл</h1>
        <form method=post enctype=multipart/form-data>
            <div><label>Path: <input type='text' name='path'></label></div>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        </html>'''


@app.route("/delete", methods=['GET', 'POST'])
def delete_file():
    if request.method == 'POST':
        path = request.form.get('path')
        db.delete(path)
        os.remove(path)
        return redirect('/all')
    return """
        <form method='POST'>
        <div><label>Path: <input type='text' name='path'></label></div>
        </form>"""
    

@app.route("/search", methods=["GET", "POST"])
def search_file():
    if request.method == 'POST':
        data = []
        path = request.form.get('path').replace("\\", "\\\\")
        cur = db.select(path, search=True)
        data = [{head[i]: row[i] for i in range(len(head))} for row in cur]
        json_data = json.dumps(data, default=str, sort_keys=False, indent=2, ensure_ascii=False)
        return Response(json_data, mimetype='application/json; charset=utf-8')
    return """
        <form method='POST'>
        <div><label>Path: <input type='text' name='path'></label></div>
        </form>"""


@app.route("/download", methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        path = request.form.get('path')
        return send_file(path, as_attachment=True)
    return """
        <form method='POST'>
        <div><label>Path: <input type='text' name='path'></label></div>
        </form>"""

@app.route("/update", methods=['GET', 'POST'])
def update_file():
    if request.method == "GET":
        return '''
        <form method='POST'>
            <div>Path: <input type='text' name='path' required></div>
        </form>'''
    
    path = request.form.get('path')
    data = db.select(path)[0]
    return f'''
    <form method='POST' action='/update_confirm'>
        <input type='hidden' name='old_path' value='{data[3]}'>
        <input type='hidden' name='extension' value='{data[1]}'>
        <div>Name: <input type='text' name='name' value='{data[0]}' required></div>
        <div>Path: <input type='text' name='new_path' value='{data[3].replace(f"{data[0]}.{data[1]}", "")}' required></div>
        <div>Comment: <textarea name='comment'>{data[6]}</textarea></div>
        <input type='submit' value='Сохранить'>
    </form>'''

@app.route("/update_confirm", methods=['POST'])
def update_file_confirm():
    old_path = request.form.get('old_path')
    name = request.form.get('name')
    extension = request.form.get('extension')
    new_path = f'{request.form.get('new_path')}\\{name}.{extension}'
    comment = request.form.get('comment')
    
    db.update(name, new_path, old_path, comment)
    
    shutil.move(old_path, new_path)
    return f'Файл обновлен'


if __name__ == '__main__':
    app.run(debug=True)