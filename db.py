import pandas as pd
import psycopg2

# database connection
def get_df():
    # setting
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="infs7205",
        user="postgres",
        password="admin"
        )

    # cursor
    cursor = conn.cursor()

    # get main table
    sql = "SELECT * FROM chipotles"
    cursor.execute(sql)
    result = cursor.fetchall()

    # convert to pandas dataframe
    columns = [row[0] for row in cursor.description]
    df = pd.DataFrame(result, columns=columns)

    # close connection
    cursor.close()
    conn.close()

    # return table
    return df
