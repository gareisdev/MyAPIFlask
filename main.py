from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/tasks')
@app.route('/tasks/<int:id_task>')
def index(id_task=None):
    if not id_task:
        return jsonify({"code": 200, "message": "success"})
    else:
        return jsonify({"code": 200, "message": "success", "id_task": id_task})


@app.route("/tasks/add/", methods=['POST'])
def add_task():
    new_task = {
        "task": request.json['task'],
        "status": request.json['status'],
    }

    return jsonify({
        "status": "success",
        "message": "task received",
        "task": new_task
    })


@app.route('/tasks/update/<int:id_task>', methods=['PUT'])
def update_task(id_task):
    new_task = {
        "task": request.json['task'],
        "status": request.json['status'],
    }
    return jsonify({"code": 200, "message": "Task update successfully", "update": new_task})


@app.route('/tasks/delete/<int:id_task>', methods=['DELETE'])
def delete_task(id_task):
    return jsonify({"code": 200, "message": "Task delete successfully", "delete": id_task})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
