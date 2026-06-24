from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from categories"

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(c):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.product_id, p.product_name, p.category_id, p.list_price
                    from products p
                    join categories c on p.category_id = c.category_id
                    where p.category_id = %s"""

        cursor.execute(query,(c,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(c,di,df):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct p1.product_id as pi1, p2.product_id as pi2, COUNT(o1.order_id ) as vendita1, COUNT(o2.order_id ) as vendita2
                    from products p1, products p2, orders o1, orders o2, order_items oi1, order_items oi2
                    where p1.product_id = oi1.product_id  and oi1.order_id = o1.order_id 
                    and p2.product_id = oi2.product_id  and oi2.order_id = o2.order_id
                    and p1.product_id < p2.product_id
                    and p1.category_id =%s 
                    and p2.category_id = %s
                    and o1.order_date  between %s and %s
                    and o2.order_date  between %s and %s
                    group by p1.product_id, p2.product_id"""

        cursor.execute(query,(c,c,di,df,di,df))

        for row in cursor:
            results.append((row["pi1"],row["pi2"],row["vendita1"],row["vendita2"]))

        cursor.close()
        conn.close()
        return results


