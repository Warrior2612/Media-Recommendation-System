from flask import Flask, render_template
    
app = Flask(__name__) #creating the Flask class object   
    
@app.route('/MediaRecommender') #decorator drfines the   
def MediaRecommender():  
    return "Media Recommendation Website";

@app.route('/Index') #decorator drfines the   
def Index():  
    return render_template('index.html') ;  

@app.route('/Login') #decorator drfines the   
def Login():  
    return render_template('login.html') ;  

@app.route('/Register') #decorator drfines the   
def Register():  
    return render_template('register.html') ;  
    
if __name__ =='__main__':  
    app.run(debug = True)