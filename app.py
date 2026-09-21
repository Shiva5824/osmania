from flask import Flask, request, render_template_string, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Mapping of hall ticket prefix to database file
DB_MAPPING = {
    "2453": "2453.db",
    "2455": "2455.db"
}

BASE_DIR = r"C:\Users\areys\OneDrive\Desktop\osmania"

def get_db_connection(db_file):
    conn = sqlite3.connect(os.path.join(BASE_DIR, db_file))
    conn.row_factory = sqlite3.Row
    return conn

# The Result HTML Template
RESULT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title>Osmania University Results - 2026</title>
<script language="JavaScript">
function FrontPage_Form1_Validator(theForm)
{
    if (theForm.htno.value == "") {
      alert("Please enter a value for the \\"Hall ticket Number\\" field.");
      theForm.htno.focus();
      return (false);
    }
    if (theForm.htno.value.length < 12 ) {
      alert("Please enter at least 12 characters in the \\"Hall ticket Number\\" field.");
      theForm.htno.focus();
      return (false);
    }
    if (theForm.htno.value.length > 12 ) {
      alert("Please enter not more than 12 characters in the \\"Hall ticket Number\\" field.");
      theForm.htno.focus();
      return (false);
    }
    return (true);
}
</script>
</head>
<body bgcolor="#FAF0D8" topmargin="0" leftmargin="0">
<form method="post" action="/search" name="FrontPage_Form1" onsubmit="return FrontPage_Form1_Validator(this)">
<input type="hidden" name="mbstatus" value="SEARCH">

<div align="center">
<center>
<table border="0" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="90%" id="AutoNumber1">
  <tr><td width="100%">
    <p align="center" style="margin: 0;"><font face="Arial" size="2"><b> B.E. (AICTE) VI, IV, II sem. (Main &amp; Backlogs); I, III, V VII sem. (Backlogs) And Make-up July/August 2026 Examination Results. </b></font></p></td></tr>
  <tr><td width="100%">  <p align="right" style="margin: 0;"><font face="Arial" size="1">19-Sep-2026 </font></p></td></tr>

  {% if student %}
  <tr>  <td width="100%">
      <div align="center">    <center>
        <table border="0" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="90%" id="AutoNumber2" bgcolor="#FFFFFF">
           <tr> <td width="100%">
            <table border="1" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="100%" id="AutoNumber3">
              <tr> <td width="100%" colspan="4" align="center" bgcolor="#EDC987">
                <b><font face="Arial" size="2">Personal Details</font></b></td></tr>
              <tr> <td width="17%" bgcolor="#FEFCF5"><font face="Arial" size="2">Hall Ticket No.</font></td>
                <td width="33%"><b> <font face="Arial" size="2" color="#FF0000">&nbsp;{{ student['htno'] }}</font></b></td>
                <td width="16%" bgcolor="#FEFCF5"> <font face="Arial" size="2">Gender</font></td>
                <td width="34%"><b> <font face="Arial" size="2">{{ student['gender'] }}</font></b></td>
              </tr>
              <tr> <td width="17%" bgcolor="#FEFCF5"><font face="Arial" size="2">Name</font></td>
                <td width="33%"><b><font face="Arial" size="2"> {{ student['name'] }}</font></b></td>
                <td width="16%" bgcolor="#FEFCF5"><font face="Arial" size="2">Father's Name</font></td>
                <td width="34%"><b><font face="Arial" size="2">{{ student['father_name'] }}</font></b></td>
              </tr>
              <tr> <td width="17%" bgcolor="#FEFCF5"><font face="Arial" size="2">Course</font></td>
                <td width="33%"><b><font face="Arial" size="2">{{ student['course'] }}</font></b></td>
                <td width="16%" bgcolor="#FEFCF5"><font face="Arial" size="2">Medium</font></td>
                <td width="34%"><b><font face="Arial" size="2"> {{ student['medium'] }}</font></b></td>
              </tr>
            </table>
            </td>
          </tr>
           <tr> <td width="100%">
             <table border="1" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="100%" id="AutoNumber4">
              <tr> <td width="100%" colspan="5" align="center" bgcolor="#EDC987" height="12"><b> <font face="Arial" size="2">Marks Details</font></b></td></tr>
              <tr><td width="10%" align="center" height="16" bgcolor="#FAF0D8"><font face="Arial" size="2">Sub Code</font></td>
                <td width="50%" align="left" height="16" bgcolor="#FAF0D8"><font face="Arial" size="2">Subject Name</font></td>
                <td width="10%" align="center" height="16" bgcolor="#FAF0D8"><font face="Arial" size="2">Credits</font></td>
                <td width="20%" align="center" height="16" bgcolor="#FAF0D8"><font face="Arial" size="2">Grade Secured</font></td>
              </tr>
              {% for mark in marks %}
              <tr><td width="10%" align="center" height="19"><b><font face="Arial" size="2">&nbsp;{{ mark['sub_code'] }} </font></b></td>
                <td width="50%" align="left" height="19"><b><font face="Arial" size="2">&nbsp;{{ mark['sub_name'] }} </font></b></td>
                <td width="10%" align="center" height="19"><b><font face="Arial" size="2">&nbsp;{{ mark['credits'] }} </font></b></td>
                <td width="20%" align="center" height="19"><b><font face="Arial" size="2">&nbsp;{{ mark['grade'] }} </font></b></td>
              </tr>
              {% endfor %}
            </table>
            </td>
          </tr>
          <tr> <td width="100%">
            <table border="1" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="100%" id="AutoNumber5">
              <tr> <td width="100%" colspan="3" align="center" bgcolor="#EDC987"> <b><font face="Arial" size="2">Result</font></b></td></tr>
               <tr>
                    <td width="20%" align="center" bgcolor="#FAF0D8"><b><font face="Arial" size="2">Semester</font></b></td>
                    <td width="50%" align="center" bgcolor="#FAF0D8"> <b><font face="Arial" size="2">Result With SGPA</font></b></td>
                    <td width="30%" align="center" bgcolor="#FAF0D8"> <b><font face="Arial" size="2">Over all CGPA</font></b></td>
                  </tr>
                  {% for res in results %}
                  <tr>
                    <td width="20%" align="center"><b> <font face="Arial" size="2">  {{ res['semester'] }} </font></b></td>
                    <td width="50%" align="center"><b> <font face="Arial" size="2">  {{ res['status'] }}-{{ res['sgpa'] }} </font></b></td>
                    <td width="30%" align="center"><b> <font face="Arial" size="2">  - </font></b></td>
                  </tr>
                  {% endfor %}
            </table>
            </td>
          </tr>
          <tr> <td width="100%" align="center">
            <font face="Arial" size="2" color="#000080">This information is provided to the candidate on his/her online request and is only a prototype list.</font> </td>
          </tr>
          <tr> <td width="100%" align="center">
            <input name="print" type="button" value="Print Page" onClick="window.print()"> </td>
          </tr>
          <tr> <td width="100%" align="right"><font face="verdana" size="2"> 0 &nbsp;</font></td> </tr>
        </table>
        </center>
      </div>
      </td>
    </tr>
  {% endif %}

  <tr> <td width="100%"> <div align="center"> <center>
   <table border="1" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="80%" id="AutoNumber6" height="19">
    <tr> <td width="100%" align="center" height="16" bgcolor="#FEFCF5"><b>
         <font face="Arial" size="2">Enter  Hall Ticket No. :
         <input type="text" name="htno" size="15" maxlength="12" value="">
         <input type="image" name="Submit" value="Go" src="gobut.gif">
         </font> </b></td>
    </tr>
    <tr><td width="100%" align="center">
        <font face="verdana" size="2" color="#FF0000"><b> Please Enter  12 Digit Hall Ticket Number
        Ex: 245524748302,  245524748303.  </b></font></td>
    </tr>
    </table>  </center>  </div>  </td>
  </tr>
  </table >  </center></div> </form>
</body>
</html>
'''

@app.route('/res07/20260655.jsp')
def home():
    return render_template_string(RESULT_TEMPLATE, student=None)

@app.route('/gobut.gif')
def serve_gif():
    return send_from_directory(BASE_DIR, 'gobut.gif')

@app.route('/res07/20260655.jsp', methods=['POST'])
def search():
    htno = request.form.get('htno')
    if not htno or len(htno) != 12:
        return render_template_string(RESULT_TEMPLATE, student=None)

    prefix = htno[:4]
    db_file = DB_MAPPING.get(prefix)

    if not db_file:
        return render_template_string(RESULT_TEMPLATE, student=None)

    try:
        conn = get_db_connection(db_file)

        # Fetch student
        student = conn.execute("SELECT * FROM students WHERE htno = ?", (htno,)).fetchone()
        if not student:
            return render_template_string(RESULT_TEMPLATE, student=None)

        # Fetch marks for both sem 1 and 2 if student has backlog/promotion cases
        marks = conn.execute("SELECT * FROM marks WHERE htno = ? ORDER BY semester ASC, sub_code ASC", (htno,)).fetchall()

        # Fetch results for semester 1 and 2
        res_rows = conn.execute("SELECT * FROM results WHERE htno = ? ORDER BY semester ASC", (htno,)).fetchall()

        # Implement Detailed Backlog Logic
        final_results = []
        sem1 = next((r for r in res_rows if r['semester'] == '1'), None)
        sem2 = next((r for r in res_rows if r['semester'] == '2'), None)

        if sem1 and sem2:
            # Case 1: Pass both or fail both or mixed
            # Use provided status from DB, but ensure correct terminology
            s1_status = sem1['status']
            s2_status = sem2['status']

            # Refine based on your rules:
            if s1_status == "PASSED":
                s1_label = "COMPLETED"
            elif s1_status == "FAILED":
                s1_label = "ALREADY PROMOTED"
            else:
                s1_label = s1_status

            if s2_status == "PASSED":
                s2_label = "PASSED"
            else:
                s2_label = "PROMOTED"

            final_results = [
                {'semester': '1', 'status': s1_label, 'sgpa': sem1['sgpa']},
                {'semester': '2', 'status': s2_label, 'sgpa': sem2['sgpa']}
            ]
        elif sem1:
            final_results = [{'semester': '1', 'status': sem1['status'], 'sgpa': sem1['sgpa']}]
        elif sem2:
            # Only sem 2 = No backlog in sem 1
            final_results = [{'semester': '2', 'status': sem2['status'], 'sgpa': sem2['sgpa']}]

        conn.close()
        return render_template_string(RESULT_TEMPLATE, student=student, marks=marks, results=final_results)

    except Exception as e:
        print(f"Error: {e}")
        return render_template_string(RESULT_TEMPLATE, student=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
