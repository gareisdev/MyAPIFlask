'''
This program is free software: you can redistribute it and/or   modify it under the terms of the GNU General Public License aspublished bythe Free Software Foundation, either version 3 of the License, or(at your option) any later version.This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty ofMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See theGNU General Public License for more details.You should have received a copy of the GNU General Public Licensealong with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
# Configs Database
app.config['MONGO_URI'] = "mongodb://127.0.0.1/tasksdb"

mongo = PyMongo(app)


@app.route('/tasks')
def getTasks(id_task=None, task_word=None):
    tasks = mongo.db.tasks.find()
    if not tasks:
        return not_found()
    response = json_util.dumps(tasks)
    return Response(response, mimetype="application/json")


@app.route("/tasks/id/<string:id_task>")
def getTaskById(id_task):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id_task)})
    if not task:
        return not_found()
    response = json_util.dumps(task)
    return Response(response, mimetype="application/json")


@app.route("/tasks/add", methods=['POST'])
def add_task():
    description_task = request.json['description_task']

    if description_task:
        status_task = 1 if "status_task" in request.json else 0
        mongo.db.tasks.insert_one(
            {
                "description_task": description_task,
                "status_task": status_task
            }
        )
        return jsonify({
            "message": "Task added successfully",
            "description_task": description_task,
            "status_task": status_task
        })

    else:
        return not_found()


@app.route('/tasks/update/<string:id_task>', methods=['PUT'])
def update_task(id_task):

    description_task = request.json['description_task']
    status_task = request.json['status_task']

    if not id_task and not description_task and not status_task:
        return jsonify({"message": "Error: ID, description or status not indicated"})

    mongo.db.tasks.update_one(
        {"_id": ObjectId(id_task)}, {"$set": {"description_task": description_task, "status": status_task}}, upsert=True)
    return jsonify({"code": 200, "message": "Task updated successfully"})


@app.route('/tasks/delete/<string:id_task>', methods=['DELETE'])
def delete_task(id_task):
    if not id_task:
        return jsonify({
            "message": "Not id indicate"
        })
    else:
        mongo.db.tasks.find_one_and_delete({'_id': ObjectId(id_task)})
        return jsonify({"message": "Task deleted successfully"})


@app.errorhandler(404)
def not_found(error=None):
    message = jsonify({
        "message": "Task not found " + request.url,
        "status": 404
    })

    return message


if __name__ == '__main__':
    app.run(debug=True, port=5000)
