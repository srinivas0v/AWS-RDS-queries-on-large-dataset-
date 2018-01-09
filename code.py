from flask import Flask, request, render_template, redirect, url_for
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = '#########'
app.config['MYSQL_DATABASE_PASSWORD'] = '###########'
app.config['MYSQL_DATABASE_DB'] = '###########'
app.config['MYSQL_DATABASE_HOST'] = '###############'
app.config['local_infile'] = 1
mysql.init_app(app)

app = Flask(__name__)


#op='mysqlimport -h aa1mqnen2sdxm1z.cmybe4kcd8wr.us-west-2.rds.amazonaws.com --fields-terminated-by=, --verbose --local -u HarshaMysur -p test_db1 '+fname
#os.system(op)

fpath = 'C:/Users/srinivas venkatesh/Downloads/'

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
      if request.form['submit'] == 'import':
          inputcsv = request.files['csvUpload']
          csvname = inputcsv.filename
          return redirect('/import/' + csvname)
      elif request.form['submit'] == 'count':
          return redirect('/count/')
      elif request.form['submit'] == 'state':
          st = request.form['statetext']
          return redirect('/state/'+st)
      elif request.form['submit'] == 'salias':
          print 'aliasrequest'
          m1 = request.form['enroll']
          print 'here'
          m2 = request.form['state']
          print m2
          mag=m1+'$'+m2
          return redirect('/salias/' + mag)
      elif request.form['submit'] == 'calias':
          print 'aliasrequest'
          m1 = request.form['enroll']
          print 'here'
          m2 = request.form['city']
          print m2
          mag=m1+'$'+m2
          return redirect('/calias/' + mag)
      elif request.form['submit'] == 'search-mag':
          print 'mag request'
          m1 = request.form['mag1']
          print 'here'
          m2 = request.form['mag2']
          print m2
          mag=m1+','+m2
          return redirect('/mag/' + mag)
          #Q_finemag(m1, m2)

    return render_template('index.html')

@app.route('/import/<fname>',methods=['POST','GET'])
def importer(fname):
    cur = mysql.connect().cursor()
    query =('LOAD DATA LOCAL infile %s' 
    'INTO TABLE MyDB.earthquake fields terminated BY ''\",\"'' lines terminated BY "\\n" IGNORE 1 LINES'
    '(time,latitude,longitude,depth,mag,magType,@nst,@gap,@dmin,rms,net,id,updated,place,type,@horizontalError,@depthError,@magError,'
    '@magNst,@status,locationSource,magSource) SET nst = nullif(@nst,\'\'), gap = nullif(@gap,\'\'),dmin = nullif(@dmin,\'\'),'
    'horizontalError = nullif(@horizontalError,\'\'), depthError = nullif(@depthError,\'\'),magError = nullif(@magError,\'\'),'
    'magNst = nullif(@magNst,\'\'),status = nullif(@status,\'\');')
    print query
    cur.execute(query,fpath+fname)
    data = cur.fetchone()
    print data
    if data is None:
        print "not uploaded"
    else:
        print "uploaded successfully"

@app.route('//<mag>',methods=['POST','GET'])
def Q_finemag(mag):
        mag1,mag2= mag.split(',')
        print 'in func'
        cur = mysql.connect().cursor()
        query=('select place,type from MyDB.earthquake where mag between %s and %s')
        cur.execute(query,(mag1,mag2))
        data = cur.fetchall()
        print data

        return render_template('display.html', flist=data)

@app.route('/count/',methods=['POST','GET'])
def count():
    print 'in func'
    cur = mysql.connect().cursor()
    query = ('select count(*) as count from MyDB.uc ')
    cur.execute(query)
    data = cur.fetchall()
    print data
    return render_template('count.html', flist=data)





@app.route('/state/<st>',methods=['POST','GET'])
def Q_state(st):
        print 'in func'
        cur = mysql.connect().cursor()
        query1=('select count(*) from MyDB.uc where STATE = %s')
        query2 = ('select Name from MyDB.uc where STATE = %s')
        cur.execute(query1,(st))
        data1 = cur.fetchall()
        print data1
        cur.execute(query2,(st))
        data2 = cur.fetchall()
        print data2

        return render_template('state.html', count=data1, list = data2)

@app.route('/salias/<var>',methods=['POST','GET'])
def alias(var):
    print 'in func'
    en,v1 = var.split('$')
    v2=''
    print en,v1,v2
    cur = mysql.connect().cursor()
    query = ('select ALIAS  from MyDB.uc where TOT_ENROLL > %s and NOT ALIAS = \'NOT AVAILABLE\' and (STATE = %s or  CITY =%s)')
    cur.execute(query,(en,v1,v2))
    data = cur.fetchall()
    print data
    return render_template('alias2.html', list = data)

@app.route('/calias/<var>',methods=['POST','GET'])
def alias1(var):
    print 'in func'
    en,v2 = var.split('$')
    v1=''
    cur = mysql.connect().cursor()
    query = ('select ALIAS  from MyDB.uc where TOT_ENROLL > %s and NOT ALIAS = \'NOT AVAILABLE\' and (STATE = %s or  CITY =%s)')
    cur.execute(query,(en,v1,v2))
    data = cur.fetchall()
    print data
    return render_template('alias.html', list = data)

if __name__ == '__main__':
    app.run(debug='true', port= 8000 )


#earthquqke dataset- usgs - latest--- csv file
# load data from csv -- sql
#query--> find mag between 3-3.5, 3-6 ---> display result in webpage
#query--> earthquarke occurred yesterday, california --> time nad place
#query--> count of earthquakes for a particular place
## log and lat near us-- 10 degrees
#read csv, read entire thing, missing field--and error-- remove all spurious data remove it,clean and then import
#visulaization-graph -- d3.js
#nhtsa recall dataset
#to make faster for large dataset->
