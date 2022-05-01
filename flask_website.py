import json
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import requests
from flask_jsglue import JSGlue

df = pd.read_json(r'db/media.json')
movie_df = pd.read_json(r'db/movies.json')
shows_df = pd.read_json(r'db/shows.json')
users = pd.read_json(r'db/users.json')
likes = pd.read_json(r'db/likes.json')
unpw = dict(zip(users['Username'], users['Password']))

app = Flask(__name__)
jsglue = JSGlue(app)
app.secret_key = 'abc123'

varId = 1;

recommended_ids = list(range(0, 250))
all_ids = list(range(0, 250))
liked_ids = []

@app.route('/index')
def Index():
    if 'username' in session:
        global liked_ids
        liked_ids = likes.iloc[likes.index[likes['Username'] == session['username']]]['liked_ids'][0]
        return render_template('index.html', data=df, id=0) ; 
    else:
        return redirect(url_for('Form')) 

@app.route('/top')
def Top():
    if 'username' in session:
        return render_template('top.html', data=df, id=0) ; 
    else:
        return redirect(url_for('Form')) 

@app.route('/movies')
def Movies():
    if 'username' in session:
        return render_template('movies.html', data=df, id=0) ; 
    else:
        return redirect(url_for('Form')) 

@app.route('/shows')
def Shows():
    if 'username' in session:
        return render_template('shows.html', data=df, id=0) ; 
    else:
        return redirect(url_for('Form')) 

@app.route('/')
def HomeRedirect():
    return redirect(url_for('Form'))

@app.route('/form', methods=['GET', 'POST']) 
def Form():  
    global unpw
    if request.method == 'POST':
        if 'email' in request.form:
            un = request.form.get('username')
            pw = request.form.get('password')
            em = request.form.get('email')
            name = request.form.get('name')

            users.loc[len(users.index)] = [un, pw, em, name]
            users.to_json('db/users.json')
            unpw = dict(zip(users['Username'], users['Password']))
            return redirect(url_for('Form'))
        else:
            un = request.form.get('username')
            pw = request.form.get('password')

            if un in unpw:
                if unpw[un] == pw:
                    return redirect(url_for('Success', username=un))
                else:
                    return render_template('form.html')
            else:
                return render_template('form.html')
    return render_template('form.html')

@app.route('/choices')
def Choices():  
    return render_template('choices.html')

@app.route('/stream')
def Stream():
    global varId
    def generate(id):
        return str(id)+"\n"+df.iloc[id]['Title']+"\n"+df.iloc[id]['Thumbnail']+"\n"+str(df.iloc[id]['Rating'])+"\n"+''.join(df.iloc[id]['Genre'])+"\n"+df.iloc[id]['Description']+"\n"+' '.join(df.iloc[id]['Stars'])+"\n"+str(df.iloc[id]['Director'])+"\n"+df.iloc[id]['Date']+"\n"+str(df.iloc[id]['Votes'])+"\n"+str(df.iloc[id]['Runtime'])
    return app.response_class(generate(recommended_ids[varId]), mimetype="text/plain")

@app.route('/streamInd/<type>')
def StreamInd(type):
    global varId
    def generate(id):
        return str(id)+"\n"+df.iloc[id]['Title']+"\n"+df.iloc[id]['Thumbnail']+"\n"+str(df.iloc[id]['Rating'])+"\n"+''.join(df.iloc[id]['Genre'])+"\n"+df.iloc[id]['Description']+"\n"+' '.join(df.iloc[id]['Stars'])+"\n"+str(df.iloc[id]['Director'])+"\n"+df.iloc[id]['Date']+"\n"+str(df.iloc[id]['Votes'])+"\n"+str(df.iloc[id]['Runtime'])
    def generateMovies(id):
        return str(id)+"\n"+movie_df.iloc[id]['Title']+"\n"+movie_df.iloc[id]['Thumbnail']+"\n"+str(movie_df.iloc[id]['Rating'])+"\n"+''.join(movie_df.iloc[id]['Genre'])+"\n"+movie_df.iloc[id]['Description']+"\n"+' '.join(movie_df.iloc[id]['Stars'])+"\n"+str(movie_df.iloc[id]['Director'])+"\n"+movie_df.iloc[id]['Date']+"\n"+str(movie_df.iloc[id]['Votes'])+"\n"+str(movie_df.iloc[id]['Runtime'])
    def generateShows(id):
        return str(id)+"\n"+shows_df.iloc[id]['Title']+"\n"+shows_df.iloc[id]['Thumbnail']+"\n"+str(shows_df.iloc[id]['Rating'])+"\n"+''.join(shows_df.iloc[id]['Genre'])+"\n"+shows_df.iloc[id]['Description']+"\n"+' '.join(shows_df.iloc[id]['Stars'])+"\n"+str(shows_df.iloc[id]['Director'])+"\n"+shows_df.iloc[id]['Date']+"\n"+str(shows_df.iloc[id]['Votes'])+"\n"+str(shows_df.iloc[id]['Runtime'])
    if type == '1':
        return app.response_class(generate(all_ids[varId]), mimetype="text/plain")
    elif type == '2':
        return app.response_class(generateMovies(all_ids[varId]), mimetype="text/plain")
    elif type == '3':
        return app.response_class(generateShows(all_ids[varId]), mimetype="text/plain")
   

@app.route('/response', methods=['GET', 'POST'])
def Response():
    global varId
    if request.method == 'GET':
        varId = int(request.values.get("id"))
    return ""

@app.route('/like', methods=['GET', 'POST'])
def Like():
    global liked_ids
    if request.method == 'GET':
        liked_ids.append(int(request.values.get("id")))
        likes.iloc[likes.index[likes['Username' == session['username']]]]['liked_ids'] = liked_ids
        likes.to_json('db/likes.json')
    return ""

@app.route('/success/<username>',methods = ["GET"])  
def Success(username):  
    session['username']=username 
    return render_template('success.html') 

@app.route('/logout')  
def Logout():  
    if 'username' in session:  
        session.pop('username',None)  
        return render_template('logout.html');  
    else:  
        return render_template('session.html')
 
@app.route('/profile')  
def Profile():  
    if 'username' in session:  
        username = session['username']  
        return render_template('profile.html',name=username)  
    else:  
        return render_template('session.html')  

@app.route('/watchlist')  
def Watchlist(): 
    return render_template('session.html')

if __name__ =='__main__':
    app.run(debug = True)