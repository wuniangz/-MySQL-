from flask import Flask, request, jsonify
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')



app = Flask(__name__)


# 连接本地 MySQL 的函数
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user=mysql_user,
        password=mysql_password,
        database='test_db',
        charset='utf8mb4'
    )


@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify({"code": 200, "data": users})


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = data.get('id')
    name = data.get('name')

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. 先查询这个 id 是不是已经存在了
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # 2. 如果查到了，说明存在，直接返回错误，不执行插入
        conn.close()
        return jsonify({"code": 400, "message": "该 ID 已经存在，请勿重复添加"}), 400

    # 3. 如果没查到，说明是全新的 id，执行插入
    cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
    conn.commit()
    conn.close()

    return jsonify({"code": 201, "message": "添加成功"}), 201


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 执行删除 SQL
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    # 检查是否真的删除了（rowcount 为 0 说明没找到这个 id）
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"code": 404, "message": "没有找到该用户"}), 404

    conn.close()
    return jsonify({"code": 200, "message": "删除成功"}), 200


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    # 获取新的名字
    new_name = data.get('name')

    if not new_name:
        return jsonify({"code": 400, "message": "缺少 name 字段"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # 执行更新 SQL：把 id 为 user_id 的那条数据的 name 改成 new_name
    cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
    conn.commit()

    # 检查是否真的更新了（如果传了一个不存在的 id，rowcount 会是 0）
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"code": 404, "message": "未找到该用户，更新失败"}), 404

    conn.close()
    return jsonify({"code": 200, "message": "更新成功"}), 200
if __name__ == '__main__':
    # 启动本地服务器，运行在 5000 端口
    app.run(port=5000, debug=True)


# @app.route('/api/users', methods=['POST'])
# def create_user():
#     data = request.json
#     # 假设传过来的字典就是 {"id": 1, "name": "张三", "age": 20, "address": "上海"}
#
#     # 动态提取所有的键（字段名）和值
#     columns = ', '.join(data.keys())
#     placeholders = ', '.join(['%s'] * len(data))
#
#     sql = f"INSERT INTO users ({columns}) VALUES ({placeholders})"
#
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(sql, tuple(data.values()))
#     conn.commit()
#     conn.close()
#
#     return jsonify({"code": 201, "message": "添加成功"}), 201