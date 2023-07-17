
from itemadapter import ItemAdapter

class NewPipeline(object):
    def __init__(self):
        pass

    # def create_connection(self):
    #     self.connection = mysql.connector.connect(
    #         host='localhost',
    #         user='root',
    #         password='actowiz',
    #         database='mytable'
    #     )
    #     self.curr = self.connection.cursor()
    #
    # def process_item(self, item, spider):
    #     self.store_db(item)
    #     return item
    #
    # def store_db(self, item):
    #     self.curr.execute(
    #         """insert into allsaint_data (store_name, address, phone_no, opening_hour, direction) values (%s, %s, %s, %s, %s)""",
    #         (
    #             item['store_name'],
    #             item['address'],
    #             item['phone_no'],
    #            str (item['opening_hour']),
    #             item['direction']
    #         ))
    #     self.connection.commit()
