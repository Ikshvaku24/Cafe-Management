import pyodbc
class UserDatabase:
    def __init__(self) -> None:
        self.conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=LAPTOP-1IG9818Q; DATABASE=cafe;Trusted_Connection=no;')
        self.cursor = self.conn.cursor()
        
    def get_user(self, id):
        query = f"SELECT *FROM users WHERE id = {id}"   
        self.cursor.execute(query)
        user_dict = {}
        result = self.cursor.fetchone()
        if result is not None:
            user_dict['id'], user_dict['username'], user_dict['password'] = result
            return user_dict
        
    
    def add_user(self, username, password):
        query = f"INSERT INTO users VALUES('{username}', '{password}')"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except pyodbc.IntegrityError:
            return False
        
    def delete_user(self, id):
        query = f"DELETE FROM users WHERE id = {id}"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0: # if no changes due to id not found then rowcount is 0
            return False
        else:
            self.conn.commit()
            return True
    
    def verify_user(self, username, password):
        query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
    
        
# db = UserDatabase()
# print(db.add_user("is11","pass123"))
    