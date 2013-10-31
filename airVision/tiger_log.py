import sqlite3



def open_data_base():
    connection = sqlite3.connect("tiger_log.db")
    the_cursor = conn.cursor()
    return connection, the_cursor


def close_data_base(connection):
    connection.commit()
    connection.close()


# Create--if one doesn't already exist--a sqlite
# data_base for the tiger_log.
def create_table():
    conn, cursor = open_data_base()
    cursor.execute("CREATE TABLE IF NOT EXISTS tiger_log (date, camera_id, processed, pos_frames)")
    close_data_base(conn)






def add_many_rows(date_and_camera):
    conn, cursor = open_data_base() 


def add_row(date, camera_id):
    conn, cursor = open_data_base() 
    cursor.execute("INSERT OR IGNORE INTO tiger_log(date, camera_id, processed, pos_frames) values(1, 'prettylongassstringlikethisone',30000, 'prettylongassstringlikethisone')")
    conn.commit()
    conn.close()


def add_



# Update the Y/N processed field for a 
# particular camera at a given date (update 1 row)
# Parameters: date of the row to be updated
# camera_id of the row to be updated
# processed: Y = is processed, N = is NOT processed
# Return: True on success, False on failure
def update_processed(date, camera_id, processed):
    if processed == "Y" or processed == "N":
        conn = sqlite3.connect("tiger_log.db")
    else:
        print "The processed field must be Y/N."
        return False



# Update the number of positive frames for a 
# particular camera at a given date (update 1 row)
# Parameters: date of the row to be updated
# camera_id of the row to be updated
# num_pos: # of positive frames found for this entry
def update_pos_frames(date, camera_id, num_pos):



# grab all dates even if processed field is unitialized
#cursor.execute("select date from tiger_activity where processed is null or processed = ''")
