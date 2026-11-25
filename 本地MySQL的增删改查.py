import requests
kw1 = {
    "method":"get",
    "url":"http://127.0.0.1:5000/api/users"
}
response = requests.request(**kw1)
print(response.json())
# 增加用户
# response = requests.post('http://127.0.0.1:5000/api/users', json={"id": 1, "name": "张三"})
# print(response.json())
# 修改用户
# put_response = requests.put('http://127.0.0.1:5000/api/users/1', json={"id": 1, "name": "李四"})
# print(put_response.json())
# # 删除用户
# delete_response = requests.delete('http://127.0.0.1:5000/api/users/1')
# print(delete_response.json())
# # 查询用户
# selected_response = requests.get('http://127.0.0.1:5000/api/users')
# print(selected_response.json())


