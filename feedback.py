import pygal
import sqlite3

con = sqlite3.connect("project.db")
c=con.cursor()

c.execute("select * from feedback")
x =[]
for row in c.fetchall():

        x.append(row)
#print len(x)
#print x[0][0]
#print x[0][1]

horizontalbar_chart = pygal.HorizontalBar()
horizontalbar_chart.title = 'Recommendation for course'
for i in range(len(x)):
 horizontalbar_chart.add(x[i][0],x[i][1])

horizontalbar_chart.render_to_file("bar_chart.svg")
