# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from menulog_proj.items import MenulogProjItem, Menulog1ProjItem, Menulog_productProjItem
import menulog_proj.db_config as db

#firstly you need to create table in mysql or columer as well
class MenulogProjPipeline:
    def process_item(self, item, spider):
        # if isinstance(item, MenulogProjItem):
        #     try:
        #         qry = f"insert into {db.takeaway_link} (`first_link`,`location`) values (%s,%s)"
        #         spider.cur.execute(qry, (item['link'], item['loc']))
        #         spider.con.commit()
        #     except Exception as e:
        #         print(e)
        if isinstance(item, Menulog1ProjItem):

            try:
                qry=f"insert into {db.menu_link} (menulog_linkcol,location) values(%s,%s)"
                spider.cur.execute(qry,(item['p_link'],item['location']))
                spider.con.commit()
                update_qry = f"update {db.takeaway_link} set status = 'Done' where id = %s"
                value=item['id']
                spider.cur.execute(update_qry, value)
                spider.con.commit()
            except Exception as e:
                print(e)
        if isinstance(item,Menulog_productProjItem):
            try:
                qry=f"insert into {db.pdp_table} (URL,Location,City,Name,Cusines,Rating,Review,street_Address,addressLocality,postalCode, Delivery_time, Phone, Min_Order,Delivery_fee,Full_Address,About_us,Delivery_hours,Offers,latitude,longitude,Stampcard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                spider.cur.execute(qry,(item['URL'],item['Location'],item['City'],item['Name'],item['Cusines'],item['Rating'],item['Review'],item['street_Address'],item['addressLocality'],item['postalCode'],item['Delivery_time'],item['Phone'],item['Min_Order'],item['Delivery_fee'],item['Full_Address'],item['About_us'],item['Delivery_hours'],item['Offers'],item['latitude'],item['longitude'],item['Stampcard']))
                spider.con.commit()
                update_qry = f"update {db.menu_link} set status = 'Done' where number = %s"
                value = item['id']
                spider.cur.execute(update_qry,value)
                spider.con.commit()
            except Exception as e:
                print(e)

        return item
