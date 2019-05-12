import flask
from flask import abort, request, jsonify, g
import sqlite3
import data_model
import json


app = flask.Flask(__name__)

# transform db fetch result to dict object
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# initial db connection
def connect_db():
    conn = sqlite3.connect('franklin.db')
    conn.row_factory = dict_factory
    return conn

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Test Home Page</h1>
    '''

def fetch_user_by_id(id):
    cur = g.db.cursor()
    users = cur.execute('SELECT * FROM users WHERE id = {0};'.format(id)).fetchall()
    return users

@app.route('/api/users', methods=['GET'])
def get_user():
    cur = g.db.cursor()
    users = cur.execute('SELECT * FROM users;').fetchall()
    return jsonify({'users': users})

@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json:
        abort(400)
    cur = g.db.cursor()
    cur.execute('''
        INSERT INTO users (name)
        VALUES ('{0}');
    '''.format(request.json['name']))
    id = cur.lastrowid
    g.db.commit()
    users_res = fetch_user_by_id(id)
    if len(users_res) == 0:
        abort(404)
    return jsonify({'user': users_res[0]})

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    if not request.json or 'name' not in request.json:
        abort(400)
    cur = g.db.cursor()
    cur.execute('''
        UPDATE users
        SET name = '{0}'
        WHERE id = {1};
    '''.format(request.json['name'], id))
    g.db.commit()
    users_res = fetch_user_by_id(id)
    if len(users_res) == 0:
        abort(404)
    return jsonify({'user': users_res[0]})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    cur = g.db.cursor()
    cur.execute('''
        DELETE FROM users
        WHERE id = {0};
    '''.format(id))
    g.db.commit()
    return jsonify({'result': True})

@app.route('/api/users/<int:id>/orders', methods=['GET'])
def get_users_order(id):
    cur = g.db.cursor()
    orders = cur.execute('SELECT * FROM orders WHERE user_id ={0};'.format(id)).fetchall()
    return jsonify({'orders': orders})

def fetch_item_by_id(id):
    cur = g.db.cursor()
    users = cur.execute('SELECT * FROM items WHERE id = {0};'.format(id)).fetchall()
    return users

@app.route('/api/items', methods=['GET'])
def get_item():
    cur = g.db.cursor()
    items = cur.execute('SELECT * FROM items;').fetchall()
    return jsonify({'items': items})

@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.json or 'name' not in request.json:
        abort(400)
    cur = g.db.cursor()
    cur.execute('''
        INSERT INTO items (name)
        VALUES ('{0}');
    '''.format(request.json['name']))
    id = cur.lastrowid
    g.db.commit()
    items_res = fetch_item_by_id(id)
    if len(items_res) == 0:
        abort(404)
    return jsonify({'item': items_res[0]})

@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    if not request.json or 'name' not in request.json:
        abort(400)
    cur = g.db.cursor()
    cur.execute('''
        UPDATE items
        SET name = '{0}'
        WHERE id = {1};
    '''.format(request.json['name'], id))
    g.db.commit()
    items_res = fetch_item_by_id(id)
    if len(items_res) == 0:
        abort(404)
    return jsonify({'item': items_res[0]})

@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    cur = g.db.cursor()
    cur.execute('''
        DELETE FROM items
        WHERE id = {0};
    '''.format(id))
    g.db.commit()
    return jsonify({'result': True})

def fetch_order_by_id(id):
    cur = g.db.cursor()
    orders = cur.execute('''
        SELECT o.user_id, o.id as order_id, i.id as item_id, i.name
        FROM orders o
        JOIN order_items oi
        ON o.id = oi.order_id
        JOIN items i
        ON oi.item_id = i.id
        WHERE o.id = {0};
    '''.format(id)).fetchall()
    return orders

def add_item_to_order(order_id, item_id):
    cur = g.db.cursor()
    orders = cur.execute('''
        INSERT INTO order_items (order_id, item_id) VALUES ({0}, {1});
    '''.format(order_id, item_id))
    g.db.commit()
    return

def del_item_from_order(order_id, item_id):
    cur = g.db.cursor()
    orders = cur.execute('''
        DELETE FROM order_items
        WHERE order_id = {0} AND item_id = {1};
    '''.format(order_id, item_id))
    g.db.commit()
    return

@app.route('/api/orders/<int:id>', methods=['GET'])
def get_order(id):
    orders = fetch_order_by_id(id)
    if len(orders) == 0:
        abort(404)
    return jsonify({'orders': orders})

@app.route('/api/orders', methods=['POST'])
def create_order():
    if not request.json or ('user_id' not in request.json and 'items' not in request.json):
        abort(400)
    if type(request.json['items']) != list:
        abort(400)
    cur = g.db.cursor()
    cur.execute('''
        INSERT INTO orders (user_id)
        VALUES ('{0}');
    '''.format(request.json['user_id']))

    order_id = cur.lastrowid
    add_order_items_sql = '''INSERT INTO order_items (order_id, item_id) VALUES'''

    for item_id in request.json['items']:
        add_order_items_sql += ' ('+str(order_id)+', '+str(item_id)+'), '
    print(add_order_items_sql)
    add_order_items_sql = add_order_items_sql.rstrip(', ') 
    add_order_items_sql += ';'
    print(add_order_items_sql)

    cur.execute(add_order_items_sql)
    g.db.commit()
    orders_res = fetch_order_by_id(order_id)
    if len(orders_res) == 0:
        abort(404)
    return jsonify({'orders_res': orders_res})

@app.route('/api/orders/<int:order_id>/add/<int:item_id>', methods=['PUT'])
def add_item_order(order_id, item_id):
    add_item_to_order(order_id, item_id)
    orders_res = fetch_order_by_id(order_id)
    return jsonify({'orders': orders_res})

@app.route('/api/orders/<int:order_id>/del/<int:item_id>', methods=['PUT'])
def del_item_order(order_id, item_id):
    del_item_from_order(order_id, item_id)
    orders_res = fetch_order_by_id(order_id)
    return jsonify({'orders': orders_res})

@app.route('/api/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    cur = g.db.cursor()
    cur.execute('''
        DELETE FROM order_items
        WHERE order_id = {0};
    '''.format(id))
    cur.execute('''
        DELETE FROM orders
        WHERE id = {0};
    '''.format(id))
    g.db.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)