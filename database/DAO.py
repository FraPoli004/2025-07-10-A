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
        query = """SELECT p1.product_id AS pi1, p2.product_id AS pi2,
              (SELECT COUNT(DISTINCT o.order_id)
               FROM order_items oi JOIN orders o ON oi.order_id = o.order_id
               WHERE oi.product_id = p1.product_id
                 AND o.order_date BETWEEN %s AND %s) AS vendita1,
              (SELECT COUNT(DISTINCT o.order_id)
               FROM order_items oi JOIN orders o ON oi.order_id = o.order_id
               WHERE oi.product_id = p2.product_id
                 AND o.order_date BETWEEN %s AND %s) AS vendita2
           FROM products p1, products p2
           WHERE p1.category_id = %s AND p2.category_id = %s
             AND p1.product_id < p2.product_id
           HAVING vendita1 > 0 AND vendita2 > 0"""

        cursor.execute(query,(di,df,di,df,c,c))

        for row in cursor:
            results.append((row["pi1"],row["pi2"],row["vendita1"],row["vendita2"]))

        cursor.close()
        conn.close()
        return results


