import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from pymongo import MongoClient 

# Scrape data

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)

browser.get('http://feeds.reuters.com/reuters/topNews')

wait = WebDriverWait(browser, 1)

wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='itemcontent']")))
wait.until(EC.presence_of_element_located((By.XPATH, ".//h4[@class='itemtitle']")))
wait.until(EC.presence_of_element_located((By.XPATH, ".//h5[@class='itemposttime']")))

itemtitles = browser.find_elements_by_class_name("itemtitle")
itemcontents = browser.find_elements_by_class_name("itemcontent")
itemposttimes = browser.find_elements_by_class_name("itemposttime")

list_of_itemtitles = []
list_of_itemcontents = []
list_of_itemposttimes = []
list_of_links = []

for item in itemtitles:
    list_of_itemtitles.append(item.text)

for item in itemcontents:
    list_of_itemcontents.append(item.text)

for item in itemposttimes:
    list_of_itemposttimes.append(item.text)

for item in itemtitles:
    links = item.find_elements_by_tag_name("a")
    for link in links:
        list_of_links.append(link.get_attribute("href"))

# PostgreSQL

try:
    connection = psycopg2.connect(user = "reuters_user", password = "reuters_password", host = "127.0.0.1", port = "5432", database = "reuters_db")

    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE reuters (ITEMTITLE TEXT, ITEMCONTENT TEXT, ITEMPOSTTIME TEXT, LINK TEXT PRIMARY KEY NOT NULL); '''
    
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
i = 0
try:
    for i in range(len(list_of_links)):
        postgres_insert_query = """INSERT INTO reuters (ITEMTITLE, ITEMCONTENT, ITEMPOSTTIME, LINK) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (list_of_itemtitles[i], list_of_itemcontents[i], list_of_itemposttimes[i], list_of_links[i])
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into PostgreSQL table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into table", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

# MongoDB

try: 
    conn = MongoClient() 
    print("Connected to MongoDB") 
except:   
    print("Could not connect to MongoDB") 

db = conn.database 

collection = db.reuters

record = []
record_id = []
try:
    for i in range(len(list_of_links)):
        record.append({"itemtitle": list_of_itemtitles[i], "itemcontent": list_of_itemcontents[i], "itemposttime": list_of_itemposttimes[i], "link": list_of_links[i]})
        record_id.append(collection.insert_one(record[i]))
        print("Data inserted with record id", record[i]) 
except:
    print ("Error writing to MongoDB")
    pass

cursor = collection.find() 
for record in cursor: 
    print(record) 

