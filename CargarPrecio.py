import MySQLdb
import os

# When running on Google App Engine, use the special unix socket
# to connect to Cloud SQL.
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    db = MySQLdb.connect(
        unix_socket='/cloudsql/farmalium:us-central1:farmalium'.format(
            CLOUDSQL_PROJECT,
            CLOUDSQL_INSTANCE),
        user='root', passwd="elpdhsqep", db="farmalium_latin1")
# When running locally, you can either connect to a local running
# MySQL instance, or connect to your Cloud SQL instance over TCP.
else:
    db = MySQLdb.connect(host='localhost', user='root', passwd="farmalium2016", db="farmalium_latin1")

cursor = db.cursor()
cursor.execute('select distinct producto from invimacompletaexcel order by 1')


add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")


data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
cursor.execute(add_employee, data_employee)
emp_no = cursor.lastrowid

# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()