const slider_containers = Array.from(document.querySelectorAll('.slider-container'))
let slider_values = Array.from(slider_containers).map(slider_container => slider_container.children[2].getAttribute("value"))
let is_applyable = false
const apply_personnality_btn = document.querySelector('#apply-personnality')
const reset_personnality_btn = document.querySelector('#reset-personnality')
const radioBtns = Array.from(document.querySelectorAll('input[type="radio"]'))
const fieldset = document.querySelector("fieldset")

const choosers = document.querySelectorAll('.chooser')
const chooser_btns = document.querySelectorAll(".voix .chooser > button")
const periphScrollingMenus = document.querySelectorAll('.périphériques .scrolling-menu')
const voiceScrollingMenus = document.querySelectorAll('.voix .scrolling-menu')
let voiceOne = document.querySelector(".show-tick")

radioBtns.forEach(radioBtn => {
    radioBtn.checked = radioBtn.getAttribute('checked').toLowerCase() == "true"
    radioBtn.addEventListener('input', ()=> {
        fieldset.children[2].classList.toggle('None')
        fieldset.children[3].classList.toggle('None')
    })
})

voiceScrollingMenus.forEach(voiceScrollingMenu=> {
    voiceScrollingMenu.childNodes.forEach(child=> {
        child.addEventListener("click", ()=> {
            if (child != voiceOne) {
                voiceOne.classList.remove("show-tick")
                child.classList.add('show-tick')
                voiceScrollingMenu.parentElement.children[0].innerText = child.innerText
		chooser_btns.forEach(btn => {
		    if (btn != child.parentElement.parentElement.children[0]) {
			console.log("Fait")
		  	btn.innerText = "Choisissez la voix de Tars"
		    }
		})
                voiceOne = child
		let origin = radioBtns.filter(radioBtn=>radioBtn.checked == true)[0].getAttribute("value")
                console.log(origin)
		let spec;
		if (origin == "native") {
		    if (child.innerText == "Voix masculine") {
			spec = "mb-fr1"
		    }
		    else {
		    	spec = "mb-fr4+3"
		    }
		}
		else {
		    spec = child.innerText
		}
		voice = {
                    "origin": origin,
                    "spec": spec
                }
                fetch('/api/update_tars_voice', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json;charset=UTF-8"
                    },
                    body: JSON.stringify(voice)
                })
                .catch(e=>console.error('Il y a eu une erreur : ', e))
            }
        })
    })
})

choosers.forEach(chooser => {
    chooser.children[0].addEventListener('click', ()=>{
        choosers.forEach(chooser2 => {
            if (chooser2 != chooser) {
                chooser2.children[1].style.setProperty('display', 'none')
            }
        })
        if (window.getComputedStyle(chooser.children[1]).getPropertyValue('display') == "none") {
            chooser.children[1].style.setProperty("display","flex")
        }
        else {
            chooser.children[1].style.setProperty("display","none")
        }
    })
})
periphScrollingMenus.forEach(periphScrollingMenu => {
    periphScrollingMenu.childNodes.forEach(child=> {
        child.addEventListener('click', ()=> {
            periphScrollingMenu.parentElement.children[0].innerText = child.innerText
            periphScrollingMenu .style.setProperty('display', 'none')
        })
    })
})


apply_personnality_btn.addEventListener('click',()=> {
    if (is_applyable) {
        console.log("Données mise à jour !");
        slider_values = Array.from(slider_containers).map(slider_container => slider_container.children[2].value)
        data_for_tars = {
            "humor": parseInt(slider_values[0]),
            "sarcasm": parseInt(slider_values[1]),
            "lenght of response": parseInt(slider_values[2])
        }
        fetch('/api/update_tars_personality', {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=UTF-8"
            },
            body: JSON.stringify(data_for_tars)
        })
        .catch(e=>console.error('Il y a eu une erreur : ', e))

        is_applyable = false
        check_apply_slider(slider_containers[0])
    }
})
reset_personnality_btn.addEventListener('click', ()=> {
    for (i=0; i<slider_values.length ; i++) {
        slider_containers[i].children[2].value = slider_values[i]
        set_pb_value(slider_containers[i].children[2], slider_containers[i].children[0])
    }
    check_apply_slider(slider_containers[2])
})

window.addEventListener('load', ()=> {
    slider_containers.forEach(slider_container => {
        slider_container.children[2].value = slider_container.children[2].getAttribute("value")
        set_pb_value(slider_container.children[2], slider_container.children[0])
        slider_container.children[2].addEventListener('input', ()=> {
            set_pb_value(slider_container.children[2], slider_container.children[0])
            check_apply_slider(slider_container)
        })
    })
})

function set_pb_value(pb, el_text) {
    text = el_text.innerText.split(":")
    text[1] = " " + pb.value + "%"
    el_text.innerText = text.join(":")
}

function check_apply_slider(slider_container) {
    let i = slider_containers.indexOf(slider_container)
    is_applyable = slider_container.children[2].value != slider_values[i]
    if (is_applyable) {
        apply_personnality_btn.style.filter = "brightness(100%)"
    }
    else {
        apply_personnality_btn.style.filter = "brightness(70%)"
    }
}
