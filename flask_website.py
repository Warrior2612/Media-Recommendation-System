from flask import Flask, render_template
    
app = Flask(__name__) #creating the Flask class object   
    
@app.route('/') #decorator drfines the   
def MediaRecommender():  
    return "<a href='/index'>Media Recommendation Website</a>";

@app.route('/index') #decorator drfines the   
def Index():  
    return render_template('index.html') ;  

@app.route('/login') #decorator drfines the   
def Login():  
    return render_template('login.html') ;  

@app.route('/register') #decorator drfines the   
def Register():  
    return render_template('register.html') ;  
    
if __name__ =='__main__':  
    app.run(debug = True)