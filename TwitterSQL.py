import mysql.connector as mysql
import Markov.Scrape_Markov as scrape
from pathlib import Path


def Insertion(handle):
    #connect to database
    mydb = mysql.connect(
        host = "localhost",
        port = 25565,
        user = "meme",
        passwd = "software_dev",
        database = "meme"
    )

    mycursor = mydb.cursor()

    scrape.get_all_tweets(handle)
    data = scrape.return_tweets()
    sql_insert = """insert ignore into content (source_text, author) values (%s,%s);"""
    mycursor.executemany(sql_insert, data)
    mydb.commit()
    mycursor.close()

def Query(handle):
    #connect to database
    mydb = mysql.connect(
        host = "localhost",
        port = 25565,
        user = "meme",
        passwd = "software_dev",
        database = "meme"
    )

    mycursor = mydb.cursor()
    query = """select source_text from content where author =  %s;"""
    mycursor.execute(query, (handle,))

    temp = mycursor.fetchone()
    if (temp == None):
        self.Insertion(handle)

    with open("query.txt", "w+",encoding = "utf-8") as f:
        for x in mycursor:
            f.write(x[0]+"\n")

    file_name = "query.txt"
    base_path = Path(file_name).parent
    file_path = (base_path / file_name).resolve()
    mycursor.close()
    return file_path
