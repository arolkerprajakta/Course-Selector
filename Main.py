__author__ = 'pa'

from flask import Flask, render_template,request,session,flash,redirect,url_for,jsonify
from register import Register
from Login import loginAccount

USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/register')
def register():
    r = Register()
    majorList = r.getMajors()
    courseList = r.getCourses()
    interestList = r.getInterests()
    return render_template('register.html',majors = majorList,courses = courseList,interests = interestList)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print "in login"
    error = None
    l = loginAccount()
    print request.method

    print "1"
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        print "2"
        if not l.ifUserExists(username,password):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['login']
            print session['username']
            flash('You were logged in')
            mainList = l.getStudDtls(username)
            print mainList
            dtls = mainList[0]
            intList = mainList[1]
            d =  dtls[0]
            print d['id']
            courseDtls = l.getCourseDtls(d['id'])
            print courseDtls
            r = Register()
            courseList = r.getOtherCourses(d['id'])
            return render_template("userHomePage.html",studentDtls=dtls,courses = courseDtls,username = username,allcourses = courseList,interests = intList)
    else:
        print "in this one"
        if session['logged_in'] == True:
            username = session['username']
            mainList = l.getStudDtls(username)
            print mainList
            dtls = mainList[0]
            intList = mainList[1]
            d =  dtls[0]
            print d['id']
            courseDtls = l.getCourseDtls(d['id'])
            print courseDtls
            r = Register()
            courseList = r.getOtherCourses(d['id'])
            return render_template("userHomePage.html",studentDtls=dtls,courses = courseDtls,username = username,allcourses = courseList)

    return render_template('index.html', error=error)

@app.route('/home',methods=['GET','POST'])
def homepage():
    print "in homepage"
    print str(request.method)
    email = ""
    if request.method == 'POST':
        print "POST"
        r = Register()
        exists = r.checkIfUserExists(request.form['email'])
        print "ooooo"
        print exists
        if not exists:
            session['username'] = request.form['email']
            accountDetails = {"email":request.form['email'],
                          "password":request.form['password'],
                          "title": request.form['title'],
                          "fName": request.form['first_name'],
                          "mName":request.form['middle_name'],
                          "lName":request.form['last_name'],
                          "gender" : request.form['sex'],
                          "city" : request.form['city'],
                          "state" : request.form['state'],
                          "street" : request.form['street'],
                          "country" : request.form['country'],
                          "birthdate" : request.form['birthdate'],
                          "courseDtls" :{"degree":request.form['degree'],
                                         "major":request.form['major'],
                                         "semester":request.form['semester'],
                                         "coursesTaken":request.form['courses'],
                                         "coursesCodeTaken":request.form['coursesCode'],
                                         "interests":request.form.getlist('interests')}}
            q =  accountDetails['courseDtls']
            print q['coursesTaken']
            email = request.form['email']
            result = r.insertAccDtls(accountDetails)
            print "result" + result
            if(result == "inserted"):
                l = loginAccount()
                mainList = l.getStudDtls(accountDetails['email'])
                print mainList
                dtls = mainList[0]
                intList = mainList[1]
                d =  dtls[0]
                courseDtls = l.getCourseDtls(d['id'])
                r = Register()
                courseList = r.getOtherCourses(d['id'])
                return render_template("userHomePage.html",studentDtls=dtls,courses = courseDtls,usernames = email,allcourses = courseList,interests = intList)
        else:
            error = "Email ID already exists"
            return render_template('register.html',error = error)

    else:

        print "in GET" + str('admin')
        l = loginAccount()
        mainList = l.getStudDtls(email)
        print mainList
        dtls = mainList[0]
        intList = mainList[1]
        d =  dtls[0]
        courseDtls = l.getCourseDtls(d['id'])
        return render_template("userHomePage.html",studentDtls=dtls,courses = courseDtls)



@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        session['logged_in'] == False
        session['username'] == ""
        return render_template('index.html')
    return render_template('index.html')

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    print "in feedback" + session['username']
    user = session['username']
    l = loginAccount()
    mainList = l.getStudDtls(user)
    print mainList
    dtls = mainList[0]
    intList = mainList[1]
    d =  dtls[0]
    courseDtls = l.getCourseDtls(d['id'])
    return render_template('feedbackform.html',courses = courseDtls,username = user )

# @app.route('/feedbackGiven',methods=['GET','POST'])
# def feedbackGiven():
#     print "in feedback" + session['username']
#     user = session['username']
#     l = loginAccount()
#     mainList = l.getStudDtls(user)
#     print mainList
#     dtls = mainList[0]
#     intList = mainList[1]
#     d =  dtls[0]
#     courseDtls = l.getCourseDtls(d['id'])
#     return render_template('recommendation&graph.html',courses = courseDtls,username = user )


@app.route('/homepage',methods=['GET','POST'])
def home():
    print request.method
    print "in homepage email" + session['username']
    user = session['username']
    l = loginAccount()
    mainList = l.getStudDtls(user)
    print mainList
    dtls = mainList[0]
    intList = mainList[1]
    d =  dtls[0]
    courseDtls = l.getCourseDtls(d['id'])
    r = Register()
    courseList = r.getOtherCourses(d['id'])
    if request.method == 'GET':
        if not request.args.get('courseName') == None:
            courseName = request.args.get('courseName')
            courseCode = request.args.get('courseCode')
            semester = request.args.get('semester')
            print courseName + semester
            reg = Register()
            result = reg.updateStudCourses(courseName,courseCode,semester,user)
            print result
            if result == "inserted":
                mainList = l.getStudDtls(user)
                dtls = mainList[0]
                intList = mainList[1]
                d =  dtls[0]
                courseDtls = l.getCourseDtls(d['id'])
                r = Register()
                courseList = r.getOtherCourses(d['id'])
                message = {"msg":"success"}
                return jsonify(message)
        elif not request.args.get('code') == None:
            courseCode = request.args.get('code')
            print courseCode
            reg = Register()
            result = reg.deleteStudCourse(courseCode,user)
            print result
            if result == "deleted":
                mainList = l.getStudDtls(user)
                dtls = mainList[0]
                intList = mainList[1]
                d =  dtls[0]
                courseDtls = l.getCourseDtls(d['id'])
                r = Register()
                courseList = r.getOtherCourses(d['id'])
                message = {"msg":"success"}
                return jsonify(message)

    return render_template("userHomePage.html",studentDtls=dtls,courses = courseDtls,allcourses = courseList,interests = intList,username = user)

@app.route('/planner',methods=['GET','POST'])
def planner():
    r = Register()
    user = session['username']
    result = r.getCoursesBasedOnInterests(user)
    result_two = r.getCoursesBasedOnTaken(user)
    r.createGraphInterests(user)
    r.createGraphCoursesTaken(user)

    return render_template("planner.html",courses = result,courserecotwo = result_two)

@app.route('/barchartInterest')
def barchartInterest():
    r = Register()
    user = session['username']

    return render_template("bar_chartCourses.html")

@app.route('/barchartCourses')
def barchartCourses():
    r = Register()
    user = session['username']

    return render_template("bar_chartInterest.html")


if __name__ == '__main__':
    app.run()
