from flask import Flask, request, jsonify, send_file
from backend.manager import FileManager
from backend.config import settings
import os


app = Flask(__name__)
manager = FileManager(storage_path=settings.STORAGE_PATH)


@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/files', methods=['GET'])
def list_files():
    q = request.args.get('q')
    files = manager.list_files(search=q)
    return jsonify(files)


@app.route('/files', methods=['POST'])
def create_file():
    data = request.get_json() or {}
    dirpath = data.get('dirpath')
    filename = data.get('filename')
    if not dirpath or not filename:
        return jsonify({'error': 'dirpath and filename required'}), 400
    try:
        result = manager.create_from_path(dirpath, filename)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id: int):
    f = manager.get(file_id)
    if not f:
        return jsonify({'error': 'not found'}), 404
    return jsonify(f)


@app.route('/files/<int:file_id>', methods=['PUT', 'PATCH'])
def update_file(file_id: int):
    data = request.get_json() or {}
    name = data.get('name')
    new_path = data.get('path')
    comment = data.get('comment')
    try:
        updated = manager.update(file_id, name=name, new_path=new_path, comment=comment)
        if not updated:
            return jsonify({'error': 'not found'}), 404
        return jsonify(updated)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id: int):
    try:
        ok = manager.delete(file_id)
        if not ok:
            return jsonify({'error': 'not found'}), 404
        return jsonify({'status': 'deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/<int:file_id>/download', methods=['GET'])
def download_file(file_id: int):
    f = manager.get(file_id)
    if not f:
        return jsonify({'error': 'not found'}), 404
    path = f.get('path')
    if not os.path.exists(path):
        return jsonify({'error': 'file not found on disk'}), 404
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=settings.DEBUG)
=======
    app.run(debug=True)
>>>>>>> e73b98e8f3f530283c4b87c9d554ab879362f7aa
