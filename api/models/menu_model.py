""" 
    This is a Menu model
"""
from api.models.database_model import Databaseconn

class Menu_now():
    """
        this class handles all menu operations
    """
    
    def add_item_to_menu(self, user_id, item_name):

        dbhandler = Databaseconn()
        dbhandler.cursor.execute("SELECT * FROM menus WHERE item_name = %s",[item_name])
        check_item_on_menu = dbhandler.cursor.fetchone()
        if check_item_on_menu:
            return 'item already exists on the menu'
        add_item_query = "INSERT INTO menus(user_id,item_name) VALUES('"+user_id+"','"+item_name+"')"
        dbhandler.cursor.execute(add_item_query)
        return "Meal has been successfully added to the menu"
        
        
    def get_menu(self):
        """
           Method for getting the menu by an admin
        """
        dbhandler = Databaseconn()
        item_query= "SELECT * FROM menus"
        dbhandler.cursor.execute(item_query)
        keys = ["item_id","item_name" ]
        menus = dbhandler.cursor.fetchall()
        menu_list = []
        for item in menus:
            menu_list.append(dict(zip(keys, item)))
        if not menu_list:
            return "No items on the menu, items will be added soon"
        return menu_list


    