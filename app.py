from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
client = MongoClient(f'mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@mongodb:27017/')
db = client['todo_db']
collection = db['tasks']

@app.route('/')
def home():
    tasks = list(collection.find())
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():

    task = request.form.get('task')

    if task:
        collection.insert_one({
            "task": task
        })

    return redirect('/')

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):

    collection.delete_one({
        "_id": ObjectId(task_id)
    })

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)