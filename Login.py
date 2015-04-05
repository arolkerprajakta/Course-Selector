__author__ = 'pa'

import sqlite3

conn =  sqlite3.connect('courseSelector.db',check_same_thread=False)

class loginAccount:
    pass

    def ifUserExists(self,username,password):
        print username
        cursor = conn.execute('SELECT * from student_account_details s where s.email="'+username+'" and s.password ="'+password+'"')
        cur = cursor.fetchall()
        if cur.__len__()>0:
            return True
        else:
            return False

    def getStudDtls(self,username):
        cursor = conn.execute('SELECT s.first_name || " " || s.last_name,a.degree,a.major,a.semester,s.id from student_account_details s,student_academic_details a where s.id = a.id and s.email="'+username+'"')
        entries = [dict(name=row[0], degree=row[1], major=row[2], ay = row [3], id  = row [4]) for row in cursor.fetchall()]
        print "ahsdihaodihwqdw"

        d =  entries[0]
        id = d['id']
        cursor = conn.execute('SELECT tag_name FROM student_interests where s_id = '+str(id))
        one_entries = [dict(tag=row[0]) for row in cursor.fetchall()]

        detailsList = []
        detailsList.append(entries)
        detailsList.append(one_entries)

        return detailsList

    def getCourseDtls(self,id):
        cursor = conn.execute('SELECT c.course_name,c.semester from student_course_details c where c.id = '+str(id))
        entries = [dict(name=row[0],semester=row[1]) for row in cursor.fetchall()]
        return entries
