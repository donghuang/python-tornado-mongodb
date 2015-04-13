function validateEmail(email) {
    var re = /^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$/;
    return re.test(email.toLowerCase());
}

function check() {
    username=document.getElementById('username').value
    email=document.getElementById('email').value
    password=document.getElementById('password').value
    password2=document.getElementById('password2').value
    if (! username ) {
        document.getElementById("showinfo").innerHTML="请输入用户名";
        
        return false;
     }else{
        document.getElementById("showinfo").innerHTML="";
     }
    if (! validateEmail(email.trim().toLowerCase()) ) {
        document.getElementById("showinfo").innerHTML="请输入正确的邮箱";
        
        return false;
     }else{
        document.getElementById("showinfo").innerHTML="";
     }
    if (password.length < 6 ) {
        document.getElementById("showinfo").innerHTML="密码至少为6个字符";
        return false;
     }else{
        document.getElementById("showinfo").innerHTML="";
     }
     if (password.length !== password2.length ) {
        document.getElementById("showinfo").innerHTML="两次输入的密码不一致";
        return false;
     }else{
        document.getElementById("showinfo").innerHTML="";
     }
}
