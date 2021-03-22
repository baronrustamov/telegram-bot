import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='34.220.146.118',
                             user='ubuntu',
                             password='ubuntu',
                             database='mainbulka',
                             cursorclass=pymysql.cursors.DictCursor)

#with connection:
    #with connection.cursor() as cursor:
        # Create a new record
     #   sql = "INSERT INTO `customers` (`email`, `password`) VALUES (%s, %s)"
      #  cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    #connection.commit()

with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT `customerNumber`, `phone`, `contactFirstName` FROM `customers` WHERE `ifdeliver`=%s"
    cursor.execute(sql, ('1',))
    result = cursor.fetchall()
    print(result)