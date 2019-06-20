from sqlalchemy import create_engine
from py_sample import views

ENGINE = None # <-- Stores the engine
CONN = None # <-- Stores the connection
DIR = 'C:\\Users\\xyzes\\Documents\\Python\\py-sample\\data' # <-- Not used
COLUMNS = {"album" : ["ID", "Title", "Artist ID", "Length (in Time)", "Num. of Tracks"],
           "artist" : ["ID", "Artist", "First Name", "Last Name", "Genre ID"],
           "genre" : ["ID", "Genre"],
           "movie" : ["ID", "Filepath", "Filename", "Title", "Running Length", "Encoding Rate", "Release Year", "Publisher ID"],
           "publisher" : ["ID", "Publisher", "City", "Country"],
           "song" : ["ID", "Filepath", "Filename", "Title", "Artist ID", "Album ID", "Album Artist ID", "Release Year", "Genre ID", "Time Length", "Bit Rate", "Publisher ID"],
           "sound" : ["ID", "Filepath", "Filename", "Artist ID", "Genre ID", "Time Length", "Bit Rate", "Publisher ID"]}
dataset = "publisher" # <-- The table displayed to the user at any given point in time


def controller(input, conn = None):
    """
    Controller interprets input from the view and updates the view with data
    from the database.
    """
    global ENGINE, CONN, COLUMNS, dataset
    # If a connection string was given and the controller is not already
    # connected, initialize the engine and connect to the database:
    if CONN == None and conn != None:
        ENGINE = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn)
        CONN = ENGINE.connect()
    sql = "EXEC dbo.sproc_get{}" # <-- Default query selects a table when formatted.
    query = "" # <-- Initialize new query to empty string.
    # The following section interprets the input and chooses or builds a query:
    if input:
        # If input is given check if table was changed:
        table = input.get("table")
        if table:
            # If table was changed, change global dataset to match table:
            dataset = table
            # The table is displayed afterwards and continues to be stored in the controller.
            query = sql.format(dataset)
        elif not table:
            new = []
            fields = COLUMNS.get(dataset) # <-- This line gets field names for new entries
            for col in range(1, len(fields)):
                # Retrieve user input based on indexes from COLUMNS
                val = input.get("add{}".format(col))
                if val != None:
                    # If value is not None, it is added to the list
                    new.append(val)
                else:
                    # Empty string is added in place of None
                    new.append("")
            if len(new) == 0:
                pass
            else:
                # If new is not empty, that means the user attempted to add new entries.
                # The program attempts the transaction.
                transaction = CONN.begin()
                try:
                    # Attempt to commit the transaction:
                    CONN.execute(add(new)) # <-- Calls helper function add(vals)
                    transaction.commit() # COMMIT
                except:
                    # If the transaction fails, it is rolled back.
                    transaction.rollback
                    raise
                # Since the procedure to add values does not return a value
                query = sql.format(dataset)
                pass
    else:
        # If no input is given, continue to display current table:
        query = sql.format(dataset)
    # The following section constructs the output from the data received:
    display = CONN.execute(query)
    data = "<table>"
    tags = COLUMNS.get(dataset) # <-- This line gets column headers.
    data += "<tr>"
    for tag in tags:
        # Each header is added to the top of the table.
        data += "<td><b>" + tag + "</b></td>"
    data += "</tr>"
    for row in display:
        # This for loop iterates through the data and adds it to the table.
        data += "<tr>"
        for col in row:
            data += "<td>" + str(col) + "</td>"
        data += "</tr>"
    data += "<tr><form name=\"Add\" action=\"/home\" method=\"GET\">"
    for col in range(len(tags)):
        # An extra row is added at the end with a form to add new values to the table.
        data += "<td>"
        if col == 0:
            data += "<input type=\"submit\" value=\"Add\">"
        else:
            # New values have the column number attached as a suffix.
            # To retrieve these values, the controller will use the indexes in COLUMNS
            data += "<input type=\"text\" name=\"add{}\" value=\"\">".format(str(col))
        data += "</td>"
    data += "</form></tr>"
    data += "</table>"
    # Return the data constructed by the controller
    return data

def scan():
    """ 
    This function will scan the directory specified by global constant DIR and
    update the database based on changes to the file system (Not used).
    """
    for subdir, dirs, files in os.walk(DIR):
        for file in files:
            print(str.join(subdir, file))

def add(vals):
    """
    This function will construct a SQL statement to add the values given to the
    dataset stored by global variable dataset.
    """
    global COLUMNS, dataset
    ans = "dbo.sproc_Insert{} ".format(dataset)
    for col in range(1, len(COLUMNS.get(dataset))):
        next = vals[col - 1]
        try:
            next = int(next)
            ans += str(next)
        except ValueError:
            next = "'{}'".format(next)
            ans += next
        if col + 1 != len(COLUMNS.get(dataset)):
            ans += ", "
    print(ans)
    return ans
