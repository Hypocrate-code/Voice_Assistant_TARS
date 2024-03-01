hide_password_btn = document.querySelector('img')
password_input = document.querySelector('#pass')

submitButton = document.querySelector('input[type="submit"]')
form = document.querySelector('form')
loader = document.querySelector('.wifi-loader')


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

window.addEventListener('beforeunload', ()=> {
    form.style.display = "None"
    loader.style.display = "flex"
})

window.addEventListener('pageshow', (event)=> {
    if (event.persisted) {
        form.style.display = "flex"
        loader.style.display = "None"
    }

})