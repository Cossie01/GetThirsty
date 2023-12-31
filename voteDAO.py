import mysql.connector


import dbconfig as cfg

class VoteDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def create(self, values): #function to create the table
        
       cursor = self.getcursor()
       sql="insert into vote (teaname,ipaddress) values (%s,%s)"
       cursor.execute(sql, values)

       self.connection.commit()
       newid = cursor.lastrowid
       self.closeAll()
       return newid
        
    def countvotes(self,teaname): #function to count the total votes
        
        cursor = self.getcursor()
        sql="select count(*) as votes from vote where teaname like %s"
        values = (teaname, )
        cursor.execute(sql, values)
        result = cursor.fetchone()
        count = result[0]
        
        self.closeAll()
        return count
       

    def convertToDictionary(self, result):
        pass
    '''
        colnames=['id','title','author', "price"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
       '''
    def createtable(self): #Creating a table
        cursor = self.getcursor()
        sql="create table vote (id int AUTO_INCREMENT NOT NULL PRIMARY KEY, teaname varchar(250), ipaddress varchar(250))"
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()

    def createdatase(self): #Creating a database
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql="create database "+ self.database
        self.cursor.execute(sql)

        self.connection.commit()
        self.closeAll()
        

voteDAO = VoteDAO()

if __name__ == "__main__":
    #voteDAO.createdatase() #This was used to initially to create the database - not needed now as it ran successfully.
    #voteDAO.createtable() #Also this as it was successfully executed.

    #data = ("Barrys", "123.123.123.123") #inputing our first vote - tea type and ip address.
    #voteDAO.create(data) #here we created one input into our voting system
    count = voteDAO.countvotes('Barrys') #counting the votes for the tea lyons
    print (count) #show the count of votes so far.