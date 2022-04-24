from flask import Flask, render_template, request, redirect, url_for, session
from flask_jsglue import JSGlue
import pandas as pd

df = pd.read_json(r'db/media.json')

app = Flask(__name__)
jsglue = JSGlue(app)
app.secret_key = 'abc123'

varId = 1;

recommended_ids = [0, 1, 10, 18, 35, 47, 76, 95, 115, 137, 170, 180, 199, 215, 237, 242]

@app.route('/index')
def Index():
    if 'username' in session:
        return render_template('index.html', data=df, id=0) ; 
    else:
        return redirect(url_for('Form')) 

@app.route('/')
def HomeRedirect():
    return redirect(url_for('Form'))

@app.route('/form', methods=['GET', 'POST']) 
def Form():  
    if request.method == 'POST':
        return redirect(url_for('Index'))
    return render_template('form.html') ;  

@app.route('/choices')
def Choices():  
    return render_template('choices.html') ;

@app.route('/stream')
def Stream():
    global varId
    def generate(id):
        return df.iloc[id]['Title']+"\n"+df.iloc[id]['Thumbnail']+"\n"+str(df.iloc[id]['Rating'])+"\n"+''.join(df.iloc[id]['Genre'])+"\n"+df.iloc[id]['Description']
    return app.response_class(generate(recommended_ids[varId]), mimetype="text/plain")

@app.route('/response', methods=['GET', 'POST'])
def Response():
    global varId
    if request.method == 'GET':
        varId = int(request.values.get("id"))
    return ""

@app.route('/success',methods = ["POST"])  
def Success():  
    if request.method == "POST":  
        session['username']=request.form['username']  
    return render_template('success.html') 

@app.route('/logout')  
def Logout():  
    if 'username' in session:  
        session.pop('username',None)  
        return render_template('logout.html');  
    else:  
        return '<p>user already logged out</p>'  
 
@app.route('/profile')  
def Profile():  
    if 'username' in session:  
        username = session['username']  
        return render_template('profile.html',name=username)  
    else:  
        return '<p>Please login first</p>'  

@app.route('/watchlist')  
def Watchlist(): 
    return '<p>Under Construction</p>' 

@app.route('/preferences')  
def Preferences(): 
    return '<p>Under Construction</p>' 

if __name__ =='__main__':
    app.run(debug = True)