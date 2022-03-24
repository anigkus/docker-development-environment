#coding=utf-8
import MySQLdb
import time
#import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')

conn= MySQLdb.connect(
        host='x.x.x.x',
        port = 3306,
        user='dev',
        passwd='dev',
        db ='me_victory',
        charset='utf8'
        )
cur = conn.cursor()

#Exclude tables
exclude_table_name="'ME_ACCESS_RECORD','CONTENT_KEYWORD','AMP_DATA_RANGE'"

#Query DB All tables
sql="SELECT IST.TABLE_NAME FROM INFORMATION_SCHEMA.TABLES IST WHERE IST.TABLE_SCHEMA = 'me_victory'" \
" AND IST.TABLE_NAME NOT IN (%s) AND IST.TABLE_ROWS>0"\
" ORDER BY IST.TABLE_NAME ASC"%(exclude_table_name)
#print(sql)


#Keyword
find_me_keyword='www.me.com'.lower()
find_img_keyword='img.me.com'.lower()

#Finded keyword table list
finded_me_tables=[]
finded_img_tables=[]

#begin time
begin=time.time()
table_count =0
try:
    # Execute sql
    table_count=cur.execute(sql)
    # Get All Record
    results = cur.fetchall()
    for table_row in results:
        table_name = table_row[0]
       
        # SQL to concatenate each table
        sql="SELECT ISC.TABLE_SCHEMA,ISC.TABLE_NAME,ISC.COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS ISC WHERE ISC.TABLE_SCHEMA = 'me_victory' " \
      "AND ISC.TABLE_NAME='%s' AND  ISC.COLUMN_NAME NOT IN('CREATED_STAMP','CREATED_TX_STAMP','LAST_UPDATED_STAMP','LAST_UPDATED_TX_STAMP')" \
      "ORDER BY ISC.ORDINAL_POSITION ASC" %(table_name)

        #print(sql)
        row_count=cur.execute(sql)
        #print(row_count)
        table_result = cur.fetchall()
        index=0
        for desc_row in table_result:
            if index==0:
                sql=desc_row[2]
            else:
                sql="%s,%s"%(sql,desc_row[2])

            index+=1

        sql ='SELECT %s FROM %s'%(sql,table_name)
        #print(sql)
        data_count=cur.execute(sql)
        data_row=2000
        data_page=1
        print("%s%s: %d"%(table_name,'number of table data'.decode('utf-8'),data_count))
        if data_count>0:
            if data_count > data_row:
                # calc data count
                if data_count%data_row==0:
                    data_page=data_count/data_row
                else:
                    data_page=(data_count/data_row)+1


            #limit record
            for num in range(0,data_page):
                start= num*data_row
                table_sql = '%s LIMIT %d,%d'%(sql,start,data_row)
                #print(table_sql)
                cur.execute(table_sql)
                table_data_result = cur.fetchall()
                for table_data_row in table_data_result:
                    for table_data_row_column in table_data_row:
                        if (isinstance(table_data_row_column,(unicode)) and (table_data_row_column!=None) and table_data_row_column.lower().find(find_me_keyword)!=-1):
                            if table_name not in finded_me_tables :
                                finded_me_tables.append(table_name)
                                #print('111:%s\n'%table_data_row_column)
                                break


                    for table_data_row_column in table_data_row:
                        if (isinstance(table_data_row_column,(unicode)) and (table_data_row_column!=None) and table_data_row_column.lower().find(find_img_keyword)!=-1):
                            if table_name not in finded_img_tables:
                                finded_img_tables.append(table_name)
                                print(table_name)
                                break




        else:
            print('%s table no data'%(table_name))

        #break

    print("\nexiste this '%s' keyword table:"%(find_me_keyword))
    for mename in finded_me_tables:
        print(mename)

    print("\nexiste this '%s' keyword table:"%(find_img_keyword))
    for imgname in finded_img_tables:
        print(imgname)

except Exception as  e:
    print ("Error: unable to fecth data\t"+str(e))
finally:
    cur.close()
    #conn.commit()
    conn.close()

end=time.time()
cons=(end-begin)*1000
print("\nTotal Table Count: %d"%(table_count))
print("begin time: %d"%(begin))
print("End Time: %d"%(end))
print("Total Time: %d%s"%(cons,'ms'))
