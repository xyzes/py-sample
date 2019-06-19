import os
import pypyodbc as pyodbc
from py_sample import views

DATA = "test"
CONN = None

def controller(input, conn = None):
    global CONN, DATA
    if CONN == None and conn != None:
        CONN = conn
    default = "SELECT * FROM song"
    query = ""
    if input:
        action = input.get("action")
        table = input.get("table")
        item1 = input.get("Item 1")
        comp = input.get("Comparator")
        item2 = input.get("Item 2")
        col = input.get("column")
        vals = input.get("new")
        cond = ""
        if item1 and comp and item2:
            cond = "{} {} {}".format(item1, comp, item2)
        if action and table:
            if action == "read":
                query = read(table, vals)
            if action == "create" and vals:
                query = create(table, vals)
            if action == "update" and vals and cond:
                query = update(table, cond, col, vals)
            if action == "delete" and cond:
                query = delete(table, cond)
            if action == "sort" and col and order:
                query = sort(table, col, order)
            if action == "find" and cond:
                query = find(table, cond)
    cursor = CONN.cursor()
    if query != "":
        cursor.execute(query)
    else:
        cursor.execute(default)
    DATA = "<table>"
    for row in cursor:
        DATA += "<tr>"
        for x in row:
            DATA += "<td>" + str(x) + "</td>"
        DATA += "</tr>"
    DATA += "</table>"
    views.DATA = DATA
        
DATA = 'C:\\Users\\xyzes\\Documents\\Python\\py-sample\\data'

def scan(CONN):
    cursor = CONN.cursor()
    for subdir, dirs, files in os.walk(DATA):
        for file in files:
            print(str.join(subdir, file))

def create(table, val):
    ans = "EXEC sampleorganizer.dbo.Add{}, {}".format(str(table).capitalize(), values)
    return ans

def read(table, val = "*"):
    col = str(val);
    if col == None:
        col = "*"
    ans = "SELECT {} FROM {}".format(values, table)
    return ans;

def update(table, cond, col, val):
    ans = "EXEC sampleorganizer.dbo.CommandAlter {}, {}, {}, {}".format(table, cond, col, val)
    return ans

def delete(table, cond):
    ans = "EXEC sampleorganizer.dbo.CommandDelete {}, {}".format(table, cond)
    return ans

def sort(table, col, order):
    ans = "EXEC sampleorganizer.dbo.Sort {}, {}, {}".format(table, col, order)
    return ans

def find(table, cond):
    ans = "EXEC sampleorganizer.dbo.Find {}, {}, {}".format(table, cond)
    return ans