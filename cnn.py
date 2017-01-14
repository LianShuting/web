import requests
import json
from bs4 import BeautifulSoup
import pymysql

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
database=pymysql.connect(host='localhost', port=3306, user='root', passwd='',db='music1', charset='utf8',
 cursorclass=pymysql.cursors.DictCursor)
cnnHome = requests.get("http://edition.cnn.com/",headers=headers).text
cnnHome = BeautifulSoup(cnnHome,"lxml")
cnnHomes = cnnHome.find_all("a",{"class":"nav-menu-links__link"})
for cnnHome in cnnHomes:
    url = cnnHome['href']
    try:
        url.index("com")
        url = url[2:]
    except ValueError:
        try:
            url.index("video")
        except ValueError:
            url = "http://edition.cnn.com"+url
    print(url)
    try:
        newList = requests.get(url)
     
        newsheadlin = newList.text
        start = newsheadlin.index("articleList")-3
        end = newsheadlin.index("registryURL")-6
        cnn = newsheadlin[start:end].strip()
        data = json.loads(cnn)
        news = data['articleList']
        for new in news:
            headline = new['headline'].replace('"',r'\"')
            year = new['uri'][1:5]
            month = new['uri'][6:8]
            day = new['uri'][9:11]
            date = year+"-"+month+"-"+day+" 01:00:00"
            print(date)
        
            description = new['description'].replace('"',r'\"')
            description = description.replace("'",r"\'")
            uri = "http://edition.cnn.com/"+new['uri']
            source = requests.get(uri,headers=headers).text
            source = BeautifulSoup(source,'lxml')
            contents = source.find_all("div",{"class":"zn-body__paragraph"})
            c = "<p>"
            for connect in contents:
                try:
                    c = c+connect.get_text().strip()+"</p>"+"<br>"
                except ValueError:
                    a=0
            c = c.replace('"',r'\"')
            c = c.replace("'",r"\'")
            try:
                c.index("Trump")
                cursor = database.cursor()
                #sql = "insert into zb2017_posts(post_title,)"
                sql = "insert into zb2017_posts (post_keywords,post_title,post_date,post_content,post_excerpt,post_author) VALUES ("'"%s"'","'"%s"'",'%s',"'"%s"'","'"%s"'","'%s'")" % ("Trump",headline,date,c,description,1)
                print(sql)
            
                try:
                    cursor.execute(sql)
                    database.commit()
                    object_id = int(cursor.lastrowid)
                    sql = "insert into zb2017_term_relationships (object_id,term_id,listorder,status) VALUES('%s','%s','%s','%s')" % (object_id,1,0,1)
                    cursor.execute(sql)
                    database.commit()
                except :
                    print('失败')
                    database.rollback()
                    #db.close()
            except ValueError:
                try:
                    c.index("Clinton")
                    cursor = database.cursor()
                    #sql = "insert into zb2017_posts(post_title,)"
                    sql = "insert into zb2017_posts (post_keywords,post_title,post_date,post_content,post_excerpt,post_author) VALUES ("'"%s"'","'"%s"'",'%s',"'"%s"'","'"%s"'","'%s'")" % ("Clinton",headline,date,c,description,1)
                    print(sql)
                
                    try:
                        cursor.execute(sql)
                        database.commit()
                        object_id = int(cursor.lastrowid)
                        sql = "insert into zb2017_term_relationships (object_id,term_id,listorder,status) VALUES('%s','%s','%s','%s')" % (object_id,2,0,1)
                        cursor.execute(sql)
                        database.commit()
                    except :
                        print('失败')
                        database.rollback()
                        #db.close()
                except ValueError:
                    c="<p>"
    except ValueError:
        a=0
end
