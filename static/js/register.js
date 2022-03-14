function validateForm(){
    var n = document.mainform.name.value;
    var user = document.mainform.username.value;
    var pass = document.mainform.password.value;
    var conf_pass = document.mainform.confirm_password.value;
    var id = document.mainform.email.value;
   
    if(n==null || n==""){
        alert("Name cannot be blank");
        return false;
    }
    
    if(n.length<=6){
        alert("Name cannot be less than 8 characters")
        return false;

    }
    for(let i=0;i<n.length;i++){
        if(n[i]==='0' || n[i]=== '1' || n[i]=== '2' || n[i]=== '3' || n[i]=== '4' || n[i]==='5' || n[i]=== '6' || n[i]=== '7' || n[i]=== '8' || n[i]=== '9'){
            alert("Name cannot contain any numeric value");
            return false;
        }
    }
    if(user==null || user==""){
        alert("Username cannot be blank");
        return false;
    }
    
    if(pass == null || pass =="" ){
        alert("Password cannot be blank");
        return false;

    }
    else if(pass.length<=6)
    if(conf_pass == null || conf_pass =="" ){
        alert("Password is invalid"); 
        return false;
    }
    
    if(conf_pass!= pass){
        alert("Confirm Password does not match Try Again")
        return false;
    }
    if(id == null || id ==""){
        alert("Email-id cannot be blank"); 
        return false;
    }
    const regularExpression = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$/;
    if(!id.match(regularExpression)){
        alert("Invalid email");
        return false;
    }
    return true;

 

}
