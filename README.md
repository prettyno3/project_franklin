# project_franklin

prerequest: flask, sqlite3 (pip install flask, sqlite3)

to run api: python api_v1.py
to run unit test: python api_v1_test.py

api desc

---------------users reslated---------------

get all users
[GET] http://localhost:5000/api/users

create user
[POST] http://localhost:5000/api/users

[BODY]
{
	"name": "user1"
}

upate user
[PUT] http://localhost:5000/api/users/4

[BODY]

{
	"user_name": "user_update_4"
}

delte user
[DELETE] http://localhost:5000/api/users/4

get all orders by user id
[GET] http://localhost:5000/api/users/1/orders

---------------items reslated---------------

get all items
[GET] http://localhost:5000/api/items

create item
[POST] http://localhost:5000/api/items

[BODY]

{
	"name": "item2"
}

upate item
[PUT] http://localhost:5000/api/items/4

[BODY]

{
	"name": "item_update_4"
}

delte item
[DELETE] http://localhost:5000/api/items/4

---------------orders reslated---------------

get order by id
[GET] http://localhost:5000/api/orders/1

create a new order
[POST] http://localhost:5000/api/orders

[BODY]

{
	"user_id": 1,
	"items": [1,2]
}

add item to order
[PUT] http://localhost:5000/api/orders/1/add/3

delete item from order
[PUT] http://localhost:5000/api/orders/1/del/3

delete order by id
[DELETE] http://localhost:5000/api/orders/1
