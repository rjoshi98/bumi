from sys import argv
import psycopg2
import time
import os
from datetime import datetime

class Database (object):

    def __init__(self):

        try:
            # On Heroku
            DATABASE_URL = os.environ['DATABASE_URL']
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        except:
            # on localhost
            self.conn = psycopg2.connect(host="ec2-3-209-176-42.compute-1.amazonaws.com",
                                        database="d7f4b8erkrgp2b",
                                        user="xrauczsvsmptxh",
                                        password="c156cb8cf731f4ba4c0658a9c66822604ad0ac71a75ab4fbb7160f203cb3e4a7")



        self.cursor = self.conn.cursor()

    # Get the basic info on all professors for searching purposes
    def get_doctors(self):
        
        self.cursor.execute('''SELECT doctors.name, location, specialty, education
                               FROM   doctors''')
        
        row = self.cursor.fetchone()
        
        doctors = []
        while row is not None:
            doctors.append(row)
            row = self.cursor.fetchone()

        return doctors

    def get_doctors1(self, name):
        
        self.cursor.execute('SELECT doctors.name, location, specialty, procedures, experience, education FROM doctors WHERE doctors.name=\'' + name + '\'')
        
        row = self.cursor.fetchone()
        
        doctors = []
        while row is not None:
            doctors.append(row)
            row = self.cursor.fetchone()

        return doctors
    
    def add_saved(self, name, docs):

        for doc in docs:
            stmtString1 = 'SELECT * FROM saved_doctors WHERE saved_doctors.user=\'' + name + '\' AND doctor=\'' + doc + '\''

            self.cursor.execute(stmtString1)

            if not self.cursor.fetchone():
                stmtString = '''INSERT INTO saved_doctors as f VALUES (%s,%s)'''

                self.cursor.execute(stmtString, [name, doc])
                self.conn.commit()
    
    def delete_saved(self, name, doc):
        stmtString = 'DELETE FROM saved_doctors WHERE saved_doctors.user = \'' + name + '\' AND doctor=\'' + doc + '\''

        self.cursor.execute(stmtString)
        self.conn.commit()
    
    def get_saved(self, name):

        docs = []
        
        stmtString = 'SELECT doctor FROM saved_doctors WHERE saved_doctors.user=\'' + name + '\''

        self.cursor.execute(stmtString)

        doc = self.cursor.fetchone()
        while doc is not None:
            docs.append(doc[0])
            doc = self.cursor.fetchone()
        
        return docs

#-----------------------------------------------------------------------

if __name__ == '__main__':
    _test(int(argv[1]))