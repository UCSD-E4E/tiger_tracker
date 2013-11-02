import sqlite3


def open_data_base():
    connection = sqlite3.connect("tiger_log.db")
    the_cursor = connection.cursor()
    return connection, the_cursor


def close_data_base(connection):
    connection.commit()
    connection.close()


# Create--if one doesn't already exist--a sqlite
# data_base for the tiger_log.
def create_table():
    conn, cursor = open_data_base()
    cursor.execute("CREATE TABLE IF NOT EXISTS tiger_log (date, camera_id, abs_path, processed, pos_frames)")
    close_data_base(conn)



# Do a batch insert.  
# Parameters: a list where every row 
# has a date, camera_id, and absolute path.
# data_and_camera = [(2013/10/12/12, cam, abs_path), (2013/10/12/13, cam, abs_path)]
# for example.
def insert_many_rows(date_camera_absolute):
    conn, cursor = open_data_base() 
    cursor.executemany("INSERT OR IGNORE INTO tiger_log(date, camera_id, abs_path) values(?,?,?)",date_camera_absolute)
    close_data_base(conn)


# Insert one row to the data_base with
# a date, camera id, and abs_path
def insert_row(date, camera_id, abs_path):
    conn, cursor = open_data_base() 
    cursor.execute("INSERT OR IGNORE INTO tiger_log(date, camera_id, abs_path) values(?,?,?)", (date, camera_id, abs_path))
    close_data_base(conn)



# Update the Y/N processed field for a 
# particular camera at a given date (update 1 row)
# Parameters: date of the row to be updated
# camera_id of the row to be updated
# processed: Y = is processed, N = is NOT processed
# Return: True on success, False on failure
def update_processed(date, camera_id, processed):
    if processed == "Y" or processed == "N":
        conn, cursor = open_data_base() 
        cursor.execute("UPDATE tiger_log SET processed = ? WHERE date = ? AND camera_id = ?",(processed, date, camera_id))  
        close_data_base(conn)
        return True
    else:
        print "The processed field must be Y/N."
        return False



# Update the Y/N processed field for a 
# particular camera at a given date (update 1 row)
# Parameters: date of the row to be updated
# camera_id of the row to be updated
# processed: Y = is processed, N = is NOT processed
# Return: True on success, False on failure
def update_processed_by_dir(abs_dir, processed):
    if processed == "Y" or processed == "N":
        conn, cursor = open_data_base() 
        cursor.execute("UPDATE tiger_log SET processed = ? WHERE abs_path = ?",(processed, abs_dir))  
        close_data_base(conn)
        return True
    else:
        print "The processed field must be Y/N."
        return False



# Update the number of positive frames for a 
# particular camera at a given date (update 1 row)
# Parameters: date of the row to be updated
# camera_id of the row to be updated
# num_pos: # of positive frames found for this entry
def update_pos_frames(date, camera_id, num_pos):
    conn, cursor = open_data_base() 
    cursor.execute("UPDATE tiger_log SET pos_frames = ? WHERE date = ? AND camera_id = ?",(num_pos, date, camera_id))  
    close_data_base(conn)


# Update the number of positive frames for a 
# particular camera at a given abs directory
# Parameters: abs directory of the video files
# num_pos: # of positive frames found for this entry
def update_pos_frames_by_dir(abs_dir, num_pos):
    conn, cursor = open_data_base() 
    cursor.execute("UPDATE tiger_log SET pos_frames = ? WHERE abs_path = ?",(num_pos, date, abs_dir))  
    close_data_base(conn)




# Select the rows that are unprocessed (the processed column
# is not marked, or marked no.)
# Return: a tuple of tuples. Each of the inner tuples 
# represent a row in the table (contains the abs_paths)
def select_unprocessed():
    conn, cursor = open_data_base() 
    conn.row_factory = sqlite3.Row
    cursor.execute("SELECT abs_path FROM tiger_log WHERE processed IS null OR processed = '' or processed = 'N'")
    unprocessed = cursor.fetchall()
    close_data_base(conn)
    return unprocessed

