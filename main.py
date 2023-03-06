import sqlite3

from flask import Flask, request, g, render_template, send_file

DATABASE ='/tmp/chatbot.db'
app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def commit():
    get_db().commit()

@app.route("/")
def hello():
    execute_query("DROP TABLE IF EXISTS userstable")
    execute_query("CREATE TABLE userstable (firstname text,lastname text,email text)")
    return render_template('index.html')

@app.route('/startenquiry', methods =['POST', 'GET'])
def startinquiry():
    message = ''
    if request.method == 'POST' and str(request.form['ufname']) !="" and str(request.form['ulname']) != "" and str(request.form['mail']) != "":
        firstname = str(request.form['ufname'])
        lastname = str(request.form['ulname'])
        email = str(request.form['mail'])
        result = execute_query("""INSERT INTO userstable (firstname, lastname, email) values (?, ?, ?)""",(firstname, lastname, email))
        commit()
    elif request.method == 'POST':
        message = 'OOPS!! Fields Missing. Fill all fields.'
    return render_template('Chat.html', message = message)

ChatWindowHTMLFirst = """
    <!DOCTYPE html>
    <html>
      <title>College Enquiry Chatbot</title>
      <body>
      <div style="width:500px;margin: auto;border: 1px solid black;padding:10px">
        <form {{url_for('chatbotsystem')}} method="POST">
          <h1>College Inquiry Chabot</h1>
          <div class="icon">
    	 <i class="fas fa-user-circle"></i>
          </div>
          <div class="formcontainer">
          <div class="container">
           <label for="ufname"><strong>Hi!! Welcome to college inquiry portal</strong></label></br></br>
    	  <label for="ufname"><strong>Choose your questions from below list</strong></label></br>
    	  <label for="ufname"><strong>1. Does the college have a football team?</strong></label></br>
    	  <label for="ufname"><strong>2. Does it have Computer Science Major?</strong></label></br>
    	  <label for="ufname"><strong>3. What is the in-state tuition?</strong></label></br>
    	  <label for="ufname"><strong>4. Does its have on campus housing?</strong></label></br>
    """

ChatWindowHTMLLast = """
    </br>
    </div>
    	<div class="text-box">
            <input type="text" style="width:300pt;height:50px" name="question" id="message" autocomplete="off" placeholder="Type your Questions here">
    	  <input class="send-button" style="width:50pt;height:50px" type="submit" value=">">
          </div></br>
           <a href='/endchat' align='center'">End Chat</a>
    	</div>
        </form>
        </div>
      </body>
    </html>
    """


@app.route('/chatbotsystem', methods =['GET', 'POST'])
def chatbotsystem():
    global ChatWindowHTMLFirst
    ChatWindowHTMLMiddle = ''
    if request.method == 'POST' and str(request.form['question']) !="":
        questionasked = str(request.form['question'])
        if(questionasked in "Does the college have a football team?"):
            ChatWindowHTMLMiddle="""
            </br><label for="ufname" style="color:blue;"><strong>"""+questionasked+"""</strong></label></br>
            <label for ="ufname"><strong> Yes! Bearcats is the football team name </strong></label></br>
            """
            # answergiven="Yes! Bearcats is the football team name"
        elif(questionasked in "Does it have Computer Science Major?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>Yes! It has Computer Science Major</strong></label></br>
            """
            # answergiven = "Yes! It has Computer Science Major"
        elif (questionasked in "What is the in-state tuition?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong> The total tuition and living expense budget for in-state Ohio residents to go to UC is $28,150</strong></label></br>
            """
            # answergiven = "The total tuition and living expense budget for in-state Ohio residents to go to UC is $28,150"
        elif (questionasked in "Does its have on campus housing?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong> No!! it doesn't have campus housing</strong></label></br>
            """
            # answergiven = "No!! it doesn't have campus housing"
        else:
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong> Sorry!! I don't have answer to your question</strong></label></br>
            """
            # answergiven = "Sorry!! I don't have answer to your question"
    ChatWindowHTMLFirst=ChatWindowHTMLFirst + ChatWindowHTMLMiddle
    return ChatWindowHTMLFirst+ChatWindowHTMLLast

EndChatHTMLFirst="""
<!DOCTYPE html>
<html>
  <title>Session Closed</title>
  <body>
  <div style="width:500px;margin: auto;border: 1px solid black;padding:10px">
    <form>
      <h1>Chat Session Closed</h1>
      <div class="icon">
	 <img src="ChatClosed.jpg"></img>
      </div>
      <div class="formcontainer">
      <div class="container">
        <label for="ufname"><strong>Hope your Questions are answered!!</strong></label></br></br>
"""

EndChatHTMLLast="""
 </div>
	</div>
    </form>
    </div>
  </body>
</html>
"""
@app.route("/endchat")
def endchat():
    global ChatWindowHTMLFirst
    ChatWindowHTMLFirst = """
        <!DOCTYPE html>
        <html>
          <title>College Enquiry Chabot</title>
          <body>
          <div style="width:500px;margin: auto;border: 1px solid black;padding:10px">
            <form {{url_for('chatbotsystem')}} method="POST">
              <h1>College Enquiry Chabot</h1>
              <div class="formcontainer">
              <div class="container">
               <label for="ufname"><strong>Hi!! Welcome to college inquiry portal</strong></label></br></br>
        	  <label for="ufname"><strong>Choose your questions from below list</strong></label></br>
        	  <label for="ufname"><strong>1.Does the college have a football team?</strong></label></br>
        	  <label for="ufname"><strong>2.Does it have Computer Science Major?</strong></label></br>
        	  <label for="ufname"><strong>3.What is the in-state tuition?</strong></label></br>
        	  <label for="ufname"><strong>4.Does its have on campus housing?</strong></label></br>
        """
    result = execute_query("""SELECT firstname,lastname,email  FROM userstable""")
    if result:
        for row in result:
            Userdetails=row[0]+","+row[1]+","+row[2]
    EndChatHTMLMiddle="""
    User Details<br>
    <label for="ufname"><strong>"""+Userdetails+"""</strong></label></br></br>
    Creator Details<br>
    <label for="ufname"><strong>Sushma, Kasarla, kasarlsd@mail.uc.edu</strong></label></br></br>
    """
    return EndChatHTMLFirst+EndChatHTMLMiddle+EndChatHTMLLast

if __name__ == '__main__':
  app.run()
