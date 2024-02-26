hide_password_btn = document.querySelector('img')
password_input = document.querySelector('#pass')

hide_password_btn.addEventListener('click', ()=> {
    if (hide_password_btn.src.includes("eye-hide.svg")) {
        hide_password_btn.src = "static/eye-see.svg"
        password_input.type = "password"
    }
    else {
        hide_password_btn.src = "static/eye-hide.svg"
        password_input.type = "text"
    }
})