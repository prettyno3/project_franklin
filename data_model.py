class User(object):
    def __init__(self, id=0, name=''):
        self.id = id
        self.name = name

class Order(object):
    def __init__(self, id=0, user_id=0):
        self.id = id
        self.user_id = user_id

class Item(object):
    def __init__(self, id=0, name=''):
        self.id = id
        self.name = name

class OrderItem(object):
    def __init__(self, order_id, item_id):
        self.order_id = order_id
        self.item_id = item_id
