__author__ = 'pa'

import sqlite3
import pygal

conn =  sqlite3.connect('courseSelector.db',check_same_thread=False)

class Register:
    pass

    def getMajors(self):
        cursor = conn.execute('SELECT major_code,major_name FROM majors_lookup order by id')
        entries = [dict(code=row[0], name=row[1]) for row in cursor.fetchall()]
        return entries

    def getCourses(self):
        cursor = conn.execute('SELECT course_code,course_name FROM course_lookup order by major_code')
        entries = [dict(code=row[0], name=row[1]) for row in cursor.fetchall()]
        return entries

    def getInterests(self):
        cursor = conn.execute('SELECT DISTINCT tag_name FROM course_tags order by course_code')
        entries = [dict(name=row[0]) for row in cursor.fetchall()]
        return entries

    def insertAccDtls(self,accountDtls):

        cursor = conn.execute('insert into student_account_details(title,first_name,middle_name,last_name,email,birth_date,password) values (?,?,?,?,?,?,?)',
                              [accountDtls['title'],
                               accountDtls['fName'],
                               accountDtls['mName'],
                               accountDtls['lName'],
                               accountDtls['email'],
                               accountDtls['birthdate'],
                               accountDtls['password']])
        conn.commit()
        last_id = cursor.lastrowid

        courseDetails = accountDtls['courseDtls']
        cursor = conn.execute('insert into student_academic_details(degree,major,semester) values (?,?,?)',
                              [courseDetails['degree'],
                               courseDetails['major'],
                               courseDetails['semester']])
        conn.commit()

        coursesTaken = courseDetails['coursesTaken']
        coursesCodeTaken = courseDetails['coursesCodeTaken']
        
        print coursesTaken

        coursesNameList = coursesTaken.split("\n")
        coursesCodeList = coursesCodeTaken.split("\n")
        coursesNameList = [i.strip() for i in coursesNameList]
        coursesCodeList = [i.strip() for i in coursesCodeList]
        for i in range(len(coursesNameList)-1):
            cursor = conn.execute('insert into student_course_details(id,course_name,course_code,semester) values (?,?,?,?)',
                                  [last_id,
                                   coursesNameList[i],
                                   coursesCodeList[i],
                                   courseDetails['semester']])

        conn.commit()

        interestList = courseDetails['interests']
        print interestList
        for key in interestList:
            print key
            cursor = conn.execute('insert into student_interests(s_id,tag_name) values (?,?)',
                                  [last_id,
                                    key])

        conn.commit()

        return "inserted"

    def checkIfUserExists(self,username):
        cursor = conn.execute('SELECT * from student_account_details s where s.email="'+username+'"')
        cur = cursor.fetchall()
        if cur.__len__()>0:
            return True
        else:
            return False


    def updateStudCourses(self,courseName,courseCode,semester,user):
        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]

        cursor = conn.execute('insert into student_course_details(id,course_name,course_code,semester) values (?,?,?,?)',
                              [id,
                              courseName,
                              courseCode,
                              semester])
        conn.commit()
        return "inserted"

    def deleteStudCourse(self,code,user):
        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]

        query = "delete from student_course_details where course_code =\""+ code + "\" and id ="+str(id)
        print query
        cursor = conn.execute(query)
        conn.commit()
        return "deleted"

    def getOtherCourses(self,id):
        cursor = conn.execute('select c.course_code,c.course_name from course_lookup c where c.course_code not in ( select s.course_code from student_course_details s where s.id= '+str(id)+')')
        entries = [dict(code=row[0], name=row[1]) for row in cursor.fetchall()]
        return entries
    
    def getCoursesBasedOnInterests(self,user):
        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]

        query = "select c.course_code,c.course_name,c.prerequisite,c.credits,c.description from course_lookup c where c.course_code in (SELECT t.course_code from course_tags t where t.tag_name IN (SELECT s.tag_name from student_interests s where s.s_id = "+str(id)+"))and c.course_code not in (SELECT cc.course_code from student_course_details cc where cc.id ="+str(id)+") group by c.course_code;"
        cursor = conn.execute(query)
        entries = [dict(code=row[0], name=row[1],prereq=row[2],credits=row[3],desc=row[4]) for row in cursor.fetchall()]

        query = "select c.prerequisite from course_lookup c where c.course_code in (SELECT t.course_code from course_tags t where t.tag_name IN (SELECT s.tag_name from student_interests s where s.s_id = "+str(id)+"))and c.course_code not in (SELECT cc.course_code from student_course_details cc where cc.id ="+str(id)+") group by c.course_code; "
        cursor = conn.execute(query)
        entries1 = [dict(prereq=row[0]) for row in cursor.fetchall()]
        #print "here"


        codeList = [0 for x in range(len(entries1))]
        for i in range(0,len(entries1)):

            d = entries1[i]
            for j in range(len(d)):

                code = d['prereq']
                cursor = conn.execute('select * from student_course_details where course_code ="'+str(code)+'"')
                cur = cursor.fetchall()
                if cur.__len__()>0:
                    codeList[i] = "yes"
                else:
                    if code == "None":
                        codeList[i] = "-"
                    else:
                        codeList[i]="no"


        #print codeList
        for d,num in zip(entries,codeList):
            d['taken'] = num

        #print entries

        return entries

    def getCoursesBasedOnTaken(self,user):
        print "in getCoursesBasedOnTaken"
        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]

        query = "select cc.course_code,cc.course_name,cc.prerequisite,cc.credits,cc.description from course_lookup cc,course_tags tt where cc.course_code = tt.course_code and tt.tag_name in (select t.tag_name from course_tags t where t.course_code in (SELECT c.course_code from student_course_details c where c.id = "+str(id)+")) and cc.course_code not in (SELECT c.course_code from student_course_details c where c.id ="+str(id)+") group by cc.course_code;"
        cursor = conn.execute(query)
        entries = [dict(code=row[0], name=row[1],prereq=row[2],credits=row[3],desc=row[4]) for row in cursor.fetchall()]
        print entries

        query = "select cc.prerequisite from course_lookup cc,course_tags tt where cc.course_code = tt.course_code and tt.tag_name in (select t.tag_name from course_tags t where t.course_code in (SELECT c.course_code from student_course_details c where c.id = "+str(id)+")) and cc.course_code not in (SELECT c.course_code from student_course_details c where c.id ="+str(id)+") group by cc.course_code;"
        cursor = conn.execute(query)
        entries1 = [dict(prereq=row[0]) for row in cursor.fetchall()]
        print "here"


        codeList = [0 for x in range(len(entries1))]
        for i in range(0,len(entries1)):

            d = entries1[i]
            for j in range(len(d)):

                code = d['prereq']
                print code
                cursor = conn.execute('select * from student_course_details where course_code ="'+str(code)+'"')
                cur = cursor.fetchall()
                if cur.__len__()>0:
                    codeList[i] = "yes"
                else:
                    if code == "None":
                        codeList[i] = "-"
                    else:
                        codeList[i]="no"


        print codeList
        for d,num in zip(entries,codeList):
            d['taken'] = num

        print entries

        return entries

    def checkIfPreReqTaken(self,user):
        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]

        query = "select c.prerequisite from course_lookup c where c.course_code in (SELECT t.course_code from course_tags t where t.tag_name IN (SELECT s.tag_name from student_interests s where s.s_id = "+str(id)+"))and c.course_code not in (SELECT cc.course_code from student_course_details cc where cc.id ="+str(id)+")  "
        cursor = conn.execute(query)
        entries = [dict(prereq=row[0]) for row in cursor.fetchall()]
        print entries
        print str(len(entries))

        result = []
        for i in range(0,len(entries)):
            print entries[i]
            d = entries[i]
            for j in range(len(d)):
                print d['prereq']
                code = d['prereq']
                cursor = conn.execute('select * from student_course_details where course_code ="'+str(code)+'"')
                cur = cursor.fetchall()
                if cur.__len__()>0:
                    result.append({"code":"yes"})
                else:
                    result.append({"code":"no"})
            print result

        print result
        return result

    #WORKING CODE FOR GRAPHS


    def createGraphCoursesTaken(self,user):

        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]

        query = "select course_code,count(*) as NumberOfRecommendations from Graph  where course_code in (select cc.course_code from course_lookup cc,course_tags tt where cc.course_code = tt.course_code and tt.tag_name in (select t.tag_name from course_tags t where t.course_code in (SELECT c.course_code from student_course_details c where c.id = "+str(id)+")) and cc.course_code not in (SELECT c.course_code from student_course_details c where c.id ="+str(id)+")) group by course_code;"
        #cursor = conn.execute('select course_code,count(*) as NumberOfRecommendations from Graph group by course_code')
        cursor = conn.execute(query)
        entries = cursor.fetchall()
        print entries

        horizontalbar_chart = pygal.HorizontalBar()
        horizontalbar_chart.title = 'Recommendation for Courses based on Previous courses'
        print len(entries)

        for i in range(len(entries)):
            print (entries[i][1])
            horizontalbar_chart.add(entries[i][0],(entries[i][1]))

        #horizontalbar_chart.render_template("bar_chart.svg")
        horizontalbar_chart.render_to_file("./templates/bar_chartCourses.html")


    def createGraphInterests(self,user):

        cursor = conn.execute('select id from student_account_details where email = "'+user+'"')
        cur = cursor.fetchone()
        id =  cur[0]
        print id

        query = "select course_code,count(*) from Graph  where course_code in (select c.course_code from course_lookup c where c.course_code in (SELECT t.course_code from course_tags t where t.tag_name IN (SELECT s.tag_name from student_interests s where s.s_id = "+str(id)+"))and c.course_code not in (SELECT cc.course_code from student_course_details cc where cc.id ="+str(id)+")) group by course_code;"
        cursor = conn.execute(query)
        #cursor = conn.execute('select course_code,count(*) as NumberOfRecommendations from Graph group by course_code')
        #cursor = conn.execute('select course_code,count(*) from Graph where course_code in (select c.course_code from course_lookup c where c.course_code in (SELECT t.course_code from course_tags t where t.tag_name IN (SELECT s.tag_name from student_interests s where s.s_id = 1))and c.course_code not in (SELECT cc.course_code from student_course_details cc where cc.id =1) group by c.course_code)group by Graph.course_code;')
        entries = cursor.fetchall()
        print entries

        horizontalbar_chart = pygal.HorizontalBar()
        horizontalbar_chart.title = 'Recommendation for Interest Based courses'
        for i in range(len(entries)):
            print (entries[i][1])
            horizontalbar_chart.add(entries[i][0],(entries[i][1]))

        #horizontalbar_chart.render_template("bar_chart.svg")
        horizontalbar_chart.render_to_file("./templates/bar_chartInterest.html")

