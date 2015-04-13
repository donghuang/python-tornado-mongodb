function check() {
    username=document.getElementById('username').value
    password=document.getElementById('password').value
    if (! username ) {
        document.getElementById("showinfo").innerHTML="请输入用户名/邮箱";
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
}
