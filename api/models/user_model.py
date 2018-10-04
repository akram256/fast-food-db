"""
    This is a a user model
"""
from api.models.database_model import Databaseconn
from werkzeug.security import generate_password_hash, check_password_hash
        
class Users(Databaseconn):
    
    def delete_tables(self):
        """
            this method is for dropping tables
        """
        table_names=['users','orders','menus']
        for name in table_names:
            self.cursor.execute("DROP TABLE IF EXISTS {} CASCADE".format(name))


    def register_a_user(self, username, email, password):
        """
           Method for registering a user
        """
  

        self.cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        check_email = self.cursor.fetchone()
        hashed_password = generate_password_hash(password, method='sha256')
        if check_email:
            return "This email already exists, Please use another email"

        insert_user = "INSERT INTO users(username, email, password) VALUES('"+username+"', '"+email+"', '"+hashed_password+"')"
        self.cursor.execute(insert_user)
        return "Account successfully created, Please login "

    def fetch_password(self, email, password):
        """
           Method for fetching the user_password
        """
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            if user[2] == email and check_password_hash(user[3], password):
                return user[0]
        return None 
       
    def get_user_with_id(self, user_id):
        """
           Method for getting an admin
        """

        self.cursor.execute("SELECT * FROM users WHERE user_id = '{}' AND is_admin = True".format(user_id))
        user_now = self.cursor.fetchone()
        return user_now



    