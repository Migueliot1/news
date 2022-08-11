/*=============== LINK ACTIVE ===============*/
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
    linkColor.forEach(l => l.classList.remove('active-link'))
    this.classList.add('active-link')
}

linkColor.forEach(l => l.addEventListener('click', colorLink))

/*=============== SHOW HIDDEN MENU ===============*/
const showMenu = (toggleId, navbarId) =>{
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId)

    if(toggle && navbar){
        toggle.addEventListener('click', ()=>{
            /* Show menu */
            navbar.classList.toggle('show-menu')
            /* Rotate toggle icon */
            toggle.classList.toggle('rotate-icon')
        })
    }
}
showMenu('nav-toggle','nav')


/*========== <a> TAG ACTS AS INPUT SUBMIT ==========*/
if (document.getElementById('login-button')!=null) {
    document.getElementById('login-button').onclick = function() {
        document.getElementById('login-in').submit()
    }
}

if (document.getElementById('signup-button')!=null) {
    document.getElementById('signup-button').onclick = function() {
        document.getElementById('login-up').submit()
    }
}

/*======== <i> arrow button acts as input submit ========*/
if (document.getElementById('downvote_btn')!=null) { 
    document.getElementById('downvote_btn').onclick = function() {
        document.getElementById('downvote_form').submit()
    }
}


if (document.getElementById('upvote_btn')){
    document.getElementById('upvote_btn').onclick = function() {
        document.getElementById('upvote_form').submit()
    }
}


/*=== Same functions but for deleting existing upvotes/downvotes ===*/
if (document.getElementById('previously_downvoted_btn')) {
    document.getElementById('previously_downvoted_btn').onclick = function() {
        document.getElementById('downvote_form').submit()
    }
}

if (document.getElementById('previously_upvoted_btn')) {
    document.getElementById('previously_upvoted_btn').onclick = function() {
        document.getElementById('upvote_form').submit()
    }
}

/*===== Same for 'Submit message' =====*/
if (document.getElementById('send_msg')){
    document.getElementById('send_msg').onclick = function() {
        document.getElementById('send_msg_form').submit()
    }
}


/*===== LOGIN SHOW and HIDDEN =====*/
const signUp = document.getElementById('sign-up'),
    signIn = document.getElementById('sign-in'),
    loginIn = document.getElementById('login-in'),
    loginUp = document.getElementById('login-up')

if (signUp) {
    signUp.addEventListener('click', ()=>{
        // Remove classes if they exist
        loginIn.classList.remove('block')
        loginUp.classList.remove('none')
        
        // Add classes
        loginIn.classList.add('none')
        loginUp.classList.add('block')
    })
}

if (signIn) {
    signIn.addEventListener('click', ()=>{
        // Remove classes if they exist
        loginIn.classList.remove('none')
        loginUp.classList.remove('block')
        
        // Add classes
        loginIn.classList.add('block')
        loginUp.classList.add('none')
    })
}


function showAccMenu() {
    const arrow = document.getElementById("arrow_to_rotate")
    var x = document.getElementById("acc_menu_to_show");
    if (x.style.display === "none") {
      x.style.display = "flex";
      arrow.classList.toggle('rotate-icon')
    } else {
      x.style.display = "none";
      arrow.classList.toggle('rotate-icon')
    }
}

function showCommentAnswerForm(form_answer_id) {
    var form = document.getElementById(form_answer_id);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}

function showBigCommentAnswerForm(form_answer_id) {
    var form = document.getElementById(form_answer_id);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
