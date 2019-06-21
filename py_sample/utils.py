from sqlalchemy import create_engine
from sqlalchemy import exc
from py_sample import views

ENGINE = None # <-- Stores the engine
CONN = None # <-- Stores the connection
DIR = 'C:\\Users\\xyzes\\Documents\\Python\\py-sample\\data' # <-- Not used
COLUMNS = {"album" : ["ID", "Title", "Artist ID", "Length (Time)", "Num. of Tracks"],
           "artist" : ["ID", "Artist", "First Name", "Last Name", "Genre ID"],
           "genre" : ["ID", "Genre"],
           "movie" : ["ID", "Filepath", "Filename", "Title", "Running Length", "Encoding Rate", "Release Year", "Publisher ID"],
           "publisher" : ["ID", "Publisher", "City", "Country"],
           "song" : ["ID", "Filepath", "Filename", "Title", "Artist ID", "Album ID", "Album Artist ID", "Release Year", "Genre ID", "Length (Time)", "Bit Rate", "Publisher ID"],
           "sound" : ["ID", "Filepath", "Filename", "Artist ID", "Genre ID", "Length (Time)", "Bit Rate", "Publisher ID"]}
PARAMS = {"album" : ["ID", "Title", "ArtistID", "TimeLength", "Tracks"],
           "artist" : ["ID", "Artist", "FirstName", "LastName", "GenreID"],
           "genre" : ["ID", "Genre"],
           "movie" : ["ID", "Directory", "Movie", "Title", "RunningLength", "EncodingRate", "ReleaseYear", "PublisherID"],
           "publisher" : ["ID", "Publisher", "City", "Country"],
           "song" : ["ID", "Directory", "Song", "Title", "ArtistID", "AlbumID", "AlbumArtistID", "ReleaseYear", "GenreID", "TimeLength", "BitRate", "PublisherID"],
           "sound" : ["ID", "Directory", "Sound", "ArtistID", "GenreID", "TimeLength", "BitRate", "PublisherID"]}
TYPES = {"album" : [1, 0, 1, 0, 1],
         "artist" : [1, 0, 0, 0, 1],
         "genre" : [1, 0],
         "movie" : [1, 0, 0, 0, 0, 1, 1, 1],
         "publisher" : [1, 0, 0, 0],
         "song" : [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1],
         "sound" : [1, 0, 0, 1, 1, 0, 1, 1]}
MANDATORY = {"album" : [0, 1],
              "artist" : [0, 1],
              "genre" : [0, 1],
              "movie" : [0, 1, 2],
              "publisher" : [0, 1],
              "song" : [0, 1, 2],
              "sound" : [0, 1, 2]}
dataset = "song" # <-- The table currently displayed to the user (changed by controller based on input
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
    sql = "EXEC dbo.sp_get{}" # <-- Default query selects a table when formatted.
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
            create = add(new)
            if not create:
                # If the Add form was not submitted, check if the Query form was:
                action = input.get("action")
                if not action:
                    # If no action was selected, continue to display current table:
                    query = sql.format(dataset)
                else:
                    if action == "update":
                        id = input.get("id")
                        col = input.get("col")
                        val = input.get("new")
                        modify = update(id, col, val)
                        # If the update helper did not return an empty sequence, execute
                        # the string as an SQL statement.
                        if modify:
                            transaction = CONN.begin()
                            try:
                                CONN.execute(modify)
                                transaction.commit()
                            except exc.IntegrityError or exc.SQLAlchemyError or exc.ProgrammingError:
                                transaction.rollback()
                                raise
                        # Since the procedure to update values does not return a table,
                        # the program needs to call the default query to display the
                        # table once again.
                        query = sql.format(dataset)
                    # If action is delete:
                    elif action == "delete":
                        # Call the delete helper to retrieve the query
                        id = input.get("id")
                        remove = delete(id)
                        # If the delete helper did not return an empty sequence, execute
                        # the string as an SQL statement.
                        if remove:
                            transaction = CONN.begin()
                            try:
                                CONN.execute(remove)
                                transaction.commit()
                            except exc.IntegrityError or exc.SQLAlchemyError:
                                transaction.rollback()
                                raise
                        # Since the procedure to delete values does not return a table,
                        # the program needs to call the default query to display the
                        # table once again.
                        query = sql.format(dataset)
                        pass

            else:
                # If new is not empty, that means the user attempted to add new entries.
                # The program attempts the transaction.
                transaction = CONN.begin()
                try:
                    # Attempt to commit the transaction:
                    CONN.execute(create) # <-- Calls helper function add(vals)
                    transaction.commit() # COMMIT
                except exc.IntegrityError or exc.SQLAlchemyError:
                    # If the transaction fails, it should be rolled back.
                    # WARNING! This block is not properly catching exceptions:
                    # Application crashes if invalid values are entered.
                    transaction.rollback()
                    raise
                # Since the procedure to add values does not return a table, the program
                # needs to call the default query to display the table once again.
                query = sql.format(dataset)
                pass
    else:
        # If no input is given, continue to display current table:
        query = sql.format(dataset)
    if not query:
        # If input was given, but no valid query was constructed, continue to display current table:
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
            data += "<input type=\"text\" name=\"add{}\" placeholder=\"{}\">".format(str(col), tags[col])
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

def get_dataset():
    """
    This function returns the name of the table currently used by the program.
    """
    global dataset
    return dataset

def add(vals):
    """
    This function will construct a SQL statement to add the values given to the
    dataset stored by global variable dataset.
    """
    global COLUMNS, TYPES, MANDATORY, dataset
    args = "" # <-- Initialize args to empty sequence
    types = TYPES.get(dataset) # <-- Fetch types for fields
    mandatory = MANDATORY.get(dataset) # <-- Fetch indexes of mandatory fields
    for col in range(1, len(COLUMNS.get(dataset))):
        next = vals[col - 1]
        if not next and col in mandatory:
            # If a mandatory field was empty, return empty sequence (no action taken in controller):
            return ""
        elif not next and col not in mandatory:
            # If a non-mandatory field was empty, add to args as NULL:
            args += "NULL"
        elif next:
            # If field was not empty:
            if types[col] == 0: # <-- Type 0 is non-integer.
                args += "'{}'".format(next)
            if types[col] == 1: # <-- Type 1 is integer.
                try:
                    # Attempt to convert value to integer to check type:
                    next = int(next)
                    args += str(next)
                except ValueError:
                    # If item cannot be converted to an integer, return empty sequence (no action taken in controller):
                    return ""
        if col + 1 != len(COLUMNS.get(dataset)):
            # If the value is not the last column, add a comma:
            args += ", "
    # print(args)
    if args:
        # If function gets this far and args is not empty, return string to insert the values:
        return "dbo.sp_Insert{} {}".format(dataset, args)
    else:
        # If function gets this far but args is empty, return empty sequence (no action taken in controller):
        return args

def update(id, col, val):
    """
    This function will construct a SQL statement to modify a column in the
    table stored in the controller, using the row ID and column name
    specified by the user and replacing its current value by the new value.
    """
    global PARAMS, TYPES, MANDATORY, dataset
    args = ""
    types = TYPES.get(dataset)
    mandatory = MANDATORY.get(dataset)
    params = PARAMS.get(dataset)
    index = None
    # The following section adds the @ID parameter
    try:
        # Check if id is an integer:
        arg = int(id)
        args += "{}, ".format(arg) # Add @ID parameter
    except ValueError:
        # If id was not an integer, return empty string (no action taken in controller):
        return ""
    # The following section adds the @column paramater
    try:
        index = COLUMNS.get(dataset).index(col) # <-- Find the index of the column to be modified
        args += "'{}', ".format(params[index]) # Add @column parameter
    except ValueError:
        # If col is not in the dataset columns, return empty string (no action taken in controller):
        return ""
    # The following section adds the @new parameter
    try:
        if not val and index in mandatory:
            # If a mandatory field was  set to be empty, return empty string (no action taken in controller):
            return ""
        elif not val and index not in mandatory:
            # If a non-mandatory field was set to be empty, add to args as NULL:
            args += "NULL"
        elif val:
            if types[index] == 0: # <-- Type 0 is non-integer.
                args = "str {}, {}".format(dataset, args)
                args += "'{}'".format(val)
            elif types[index] == 1: # <-- Type 1 is integer.
                # Attempt to convert value to integer to check type:
                args = "int {}, {}".format(dataset, args)
                new = int(val)
                args += str(val)
    except ValueError:
        # If the wrong type was give, return empty string (no action taken in controller):
        return ""
    if args:
        # If function gets this far and args is not empty, return string to edit the value:
        return "dbo.sp_Update{}".format(args)
    else:
        # If function gets this far but args is empty, return empty sequence (no action taken in controller):
        return args

def delete(id):
    """
    This function will construct a SQL statement to remove a value from the
    table stored in the controller, using the row ID specified by the user
    """
    global dataset
    try:
        # Check if id is an integer:
        args = int(id)
        return "dbo.sp_Delete{} {}".format(dataset, str(args))
    except ValueError:
        # If id was not an integer, return empty string (no action taken in controller):
        return ""