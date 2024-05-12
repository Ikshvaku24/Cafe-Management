import pyodbc
from socket import gethostname, gethostbyname
class ItemDatbase:
    def __init__(self) -> None:
        host_ipaddress = gethostbyname('host.docker.internal')
        self.conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={host_ipaddress}; DATABASE=cafe;UID=sa;PWD=<password>')
        self.cursor = self.conn.cursor()
        
    def get_Items(self):
        result = []
        query = "SELECT *FROM item"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            items_dict = {}
            items_dict['id'], items_dict['name'], items_dict['price'] = row
            result.append(items_dict)
        return result
        
    def get_Item(self, id):
        query = f"SELECT *FROM item where id = '{id}'"   
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            items_dict = {}
            items_dict['id'], items_dict['name'], items_dict['price'] = row
            return [items_dict]
        
    
    def add_Item(self, id, body):
        query = f"INSERT INTO item VALUES('{id}', '{body['name']}', {body['price']})"
        self.cursor.execute(query)
        self.conn.commit()
        
        
    def put_Item(self, id, body):
        query = f"UPDATE item SET name = '{body['name']}', price = {body['price']} WHERE id = '{id}'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0: # if no changes due to id not found then rowcount is 0
            return False
        else:
            self.conn.commit()
            return True
        
    def delete_Item(self, id):
        query = f"DELETE FROM item WHERE id = '{id}'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0: # if no changes due to id not found then rowcount is 0
            return False
        else:
            self.conn.commit()
            return True
        
    # db = ItemDatbase()
    # db.delete_Item('ebafe30bc105413dabb981763b65d15a')