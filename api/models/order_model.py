""" 
    This is an Order model
"""
from api.models.database_model import Databaseconn


class Order_now(Databaseconn):
    """
        this class handles all order methods
    """
    def get_all_orders(self):
        """
           Method for getting all orders
        """
        order_query= "SELECT * FROM orders"
        self.cursor.execute(order_query)
        keys = ["order_id", "order_now","user_id","item_id" ,"order_date"]
        orders = self.cursor.fetchall()
        order_list = []
        for order in orders:
            order_list.append(dict(zip(keys, order)))
        if not order_list:
            return "No orders available at the moment"
        return order_list

    def get_one_order(self, order_id):
        """
           Method for getting a specific order using an inserted_order_id
        """
        self.cursor.execute("SELECT * FROM orders WHERE order_id = %s", [order_id])
        order_list = self.cursor.fetchone()
        keys=["order_id", "order_now","user_id","item_id" ,"order_date"]
        if not order_list:
            return "Order not available at the moment"
        one_order_list = []
        one_order_list.append(dict(zip(keys, order_list)))
        return one_order_list


    def update_order_status(self,order_id,order_now):
        """
             this is a method for updating an order_status
        """
        self.cursor.execute("""SELECT "order_id" FROM orders WHERE order_id= %s""",(order_id, ) )
        check_status=self.cursor.fetchone()
        print(check_status)
        if not check_status:
            return "No order to update, please select another order_id"
        put_status_query = "UPDATE  orders SET order_now = %s WHERE order_id = %s;"
        self.cursor.execute(put_status_query,(order_now, order_id, ))
        updated_rows = self.cursor.rowcount
        # if updated_rows:
        return updated_rows
        # return "No orders to update"


    def specify_user_order(self):
        """
            this method is for getting orders for a specific user
        """
        order_query_user= "SELECT * FROM orders"
        self.cursor.execute(order_query_user)
        keys =["order_id","order_now","user_id","item_id"]
        orders = self.cursor.fetchall()
        specfic_list = []
        for order in orders:
            specfic_list.append(dict(zip(keys, order)))
        if not specfic_list:
            return "user has not made orders yet"
        return specfic_list
        
    def place_new_order(self, user_id, item_id):
        """
           Method for placing an order
           params: order_now
        """
       
        self.cursor.execute("SELECT * FROM menus WHERE item_id= %s",(item_id, ) )
        data=self.cursor.fetchone()
        print(data)
        add_order_query = "INSERT INTO orders(user_id, item_id) VALUES( %s,%s);"

        self.cursor.execute(add_order_query,(user_id,item_id,))
        return "Order has been Placed successfully"