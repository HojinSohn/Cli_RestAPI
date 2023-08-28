import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request
from datetime import datetime
from helper import sort_by_date

@app.route('/task', methods=['POST', 'GET'])
def task():
    if request.method == "POST":
        try:
            _json = request.json
            _title = _json['title']
            _description = _json['description']
            # _timestamp = _json['timestamp']
            time_string = _json['timestamp']
            print(time_string)
            datetime_obj = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
            _timestamp = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

            if _title and _description and _timestamp and request.method == 'POST':
                connection = mysql.connect()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                sqlQuery = "INSERT INTO task(title, description, timestamp) VALUES(%s, %s, %s)"
                bindData = (_title, _description, _timestamp)
                cursor.execute(sqlQuery, bindData)
                connection.commit()
                cursor.close()
                respone = jsonify('task creat success')
                respone.status_code = 200
                return respone
            else:
                showErrMessage()
        except Exception as err:
            print(err)
        finally:
            connection.close()
    if request.method == "GET":
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, title, description, timestamp FROM task")
            task_rows = cursor.fetchall()
            connection.commit()
            # response = jsonify(task_rows)
            raw_tasks = jsonify(task_rows).json
            response = jsonify(sort_by_date(raw_tasks))
            response.status_code = 200
            return response
        except Exception as err:
            print(err)
        finally:
            cursor.close()
            connection.close()

@app.route('/task/<int:task_id>', methods=['GET'])
def specific_task(task_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, title, description, timestamp FROM task WHERE id=%s", task_id)
        taskRow = cursor.fetchone()
        connection.commit()
        response = jsonify(taskRow)
        response.status_code = 200
        return response
    except Exception as err:
        print(err)
    finally:
        cursor.close()
        connection.close()

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    _json = request.json
    # _id = None
    _title = None
    _description = None
    _timestamp = None
    # if 'id' in _json:
    #     print("id@@@@@")
    #     _id = _json['id']
    if 'title' in _json:
        print("title@@@@@")
        _title = _json['title']
    if 'description' in _json:
        print("des@@@@@")
        _description = _json['description']
    if 'timestamp' in _json:
        print("time@@@@@")
        _timestamp = _json['timestamp']

    try:
        if task_id and request.method == "PUT":
            print("yesyes")
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            if _title:
                print("title execute")
                cursor.execute("UPDATE task SET title=%s WHERE id=%s",
                               (_title, task_id))
            if _description:
                print("_description execute")
                cursor.execute("UPDATE task SET description=%s WHERE id=%s",
                               (_description, task_id))
            if _timestamp:
                print("_timestamp execute")
                cursor.execute("UPDATE task SET timestamp=%s WHERE id=%s",
                               (_timestamp, task_id))
            connection.commit()
            response = jsonify("task update success")
            response.status_code = 200
            return response
        else:
            print("what error no id update")
            showErrMessage()
    except Exception as err:
        print("errrrrr@@@2")
        print(err)
    finally:
        cursor.close()
        connection.close()

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM task WHERE id =%s", (task_id,))
        connection.commit()
        respone = jsonify('task delete success')
        respone.status_code = 200
        return respone
    except Exception as err:
        print(err)
    finally:
        cursor.close()
        connection.close()

@app.errorhandler(404)
def showErrMessage():
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response




if __name__ == "__main__":
    app.run()