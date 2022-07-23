import psycopg2

connection = False

try:
    connection = psycopg2.connect(user="postgres",
                                  password="Reibach2020+",
                                  host="34.77.211.120",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from json_dict"

    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from json_dict table using cursor.fetchall")
    mobile_records = cursor.fetchall()

    print("Print each row and it's columns values")
    
    for row in mobile_records:
        print("Id = ", row[0], )
        print("Key = ", row[1])
        print("Value  = ", row[2], "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
