from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sqlite3
import secrets
import hashlib
import smtplib
from email.message import EmailMessage

# =========================================================
# FAISU AI LAB
# Local browser address:
# http://faisuailab:8000
#
# Windows Hosts file required:
# 127.0.0.1 faisuailab
# =========================================================

app = FastAPI(title="FAISU AI LAB")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

DB = BASE_DIR / "users.db"


# =========================================================
# GMAIL SETTINGS
# =========================================================

SMTP_EMAIL = "YOUR_GMAIL@gmail.com"
SMTP_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"


# =========================================================
# DATABASE
# =========================================================

def db():
    con = sqlite3.connect(DB)

    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            verified INTEGER DEFAULT 0,
            otp TEXT
        )
    """)

    con.commit()
    return con


# =========================================================
# PASSWORD
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# SEND OTP
# =========================================================

def send_otp(email, otp):

    msg = EmailMessage()

    msg["Subject"] = "FAISU AI LAB - Email Verification"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email

    msg.set_content(
        f"""
FAISU AI LAB

Your verification code is:

{otp}

Enter this code on FAISU AI LAB to verify your account.

If you did not create this account, ignore this email.
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        server.send_message(msg)


# =========================================================
# HOME PAGE
# =========================================================

HOME = """
<!DOCTYPE html>
<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>FAISU AI LAB</title>

<style>

*{
 box-sizing:border-box;
}

body{
 margin:0;
 font-family:Arial,sans-serif;
 color:white;
 background:#050816;
}

nav{
 height:70px;
 display:flex;
 align-items:center;
 justify-content:space-between;
 padding:0 7%;
 background:rgba(5,8,22,.9);
 position:sticky;
 top:0;
 z-index:10;
}

.logo{
 font-size:25px;
 font-weight:900;
 color:#fff;
}

.logo span{
 color:#7c5cff;
}

.navbtn{
 padding:11px 20px;
 border:0;
 border-radius:25px;
 background:#7c5cff;
 color:white;
 cursor:pointer;
 font-weight:bold;
}

.hero{
 min-height:680px;
 padding:80px 7%;
 display:flex;
 align-items:center;
 justify-content:space-between;
 gap:40px;

 background:
 radial-gradient(
  circle at 20% 20%,
  #40208055,
  transparent 35%
 ),
 radial-gradient(
  circle at 80% 30%,
  #0066ff44,
  transparent 35%
 ),
 #050816;
}

.heroText{
 max-width:650px;
}

.badge{
 display:inline-block;
 padding:8px 15px;
 border-radius:30px;
 background:#ffffff12;
 border:1px solid #ffffff22;
}

h1{
 font-size:60px;
 line-height:1.05;
 margin:20px 0;
}

.gradient{
 background:linear-gradient(
  90deg,
  #7c5cff,
  #00d4ff
 );

 -webkit-background-clip:text;
 color:transparent;
}

.hero p{
 color:#b8bfd8;
 font-size:18px;
 line-height:1.7;
}

.heroVisual{
 width:420px;
 height:420px;
 border-radius:35px;

 background:
 linear-gradient(
  145deg,
  #171d42,
  #10152e
 );

 border:1px solid #ffffff18;

 display:flex;
 align-items:center;
 justify-content:center;

 box-shadow:0 0 80px #604cff22;
}

.person{
 width:240px;
 height:260px;
 position:relative;
}

.head{
 width:120px;
 height:120px;
 border-radius:50%;
 background:#c98f72;
 margin:auto;
 position:relative;
 z-index:2;
}

.hair{
 position:absolute;
 width:125px;
 height:55px;
 background:#17120f;
 border-radius:60px 60px 20px 20px;
 top:0;
 left:57px;
 z-index:3;
}

.headphones{
 position:absolute;
 width:145px;
 height:145px;
 border:12px solid #7c5cff;
 border-bottom-color:transparent;
 border-radius:50%;
 top:-13px;
 left:48px;
 z-index:4;
}

.laptop{
 position:absolute;
 width:230px;
 height:125px;
 background:#20283f;
 border:7px solid #8791b2;
 border-radius:12px;
 bottom:0;
 left:5px;
}

.screen{
 margin:10px;
 height:90px;
 border-radius:7px;

 background:
 linear-gradient(
  135deg,
  #7c5cff,
  #00d4ff
 );
}

section{
 padding:80px 7%;
}

.sectionTitle{
 text-align:center;
 font-size:38px;
 margin-bottom:45px;
}

.cards{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:25px;
}

.card{
 padding:30px;
 min-height:230px;
 border-radius:25px;

 background:
 linear-gradient(
  145deg,
  #111936,
  #0b1024
 );

 border:1px solid #ffffff14;
 transition:.3s;
}

.card:hover{
 transform:translateY(-8px);
 border-color:#7c5cff;
}

.icon{
 font-size:45px;
 margin-bottom:15px;
}

.card h3{
 font-size:22px;
}

.card p{
 color:#aab1ca;
 line-height:1.6;
}

.cta{
 text-align:center;

 background:
 linear-gradient(
  135deg,
  #101938,
  #16102d
 );
}

footer{
 text-align:center;
 padding:35px;
 color:#858da8;
}

.modal{
 display:none;
 position:fixed;
 inset:0;
 background:#000b;
 z-index:100;

 align-items:center;
 justify-content:center;

 padding:20px;
}

.box{
 width:100%;
 max-width:420px;
 padding:35px;

 border-radius:25px;

 background:#11172c;

 border:1px solid #ffffff18;
}

.box h2{
 text-align:center;
}

input{
 width:100%;
 padding:14px;
 margin:8px 0;

 border-radius:12px;

 border:1px solid #ffffff18;

 background:#080d20;

 color:white;
}

.action{
 width:100%;
 padding:14px;
 margin-top:10px;

 border:0;
 border-radius:12px;

 background:#7c5cff;

 color:white;

 font-weight:bold;

 cursor:pointer;
}

.close{
 text-align:right;
 cursor:pointer;
 color:#aaa;
}

@media(max-width:800px){

 .hero{
  flex-direction:column;
  text-align:center;
  padding-top:50px;
 }

 h1{
  font-size:42px;
 }

 .heroVisual{
  width:100%;
  max-width:380px;
 }

 .cards{
  grid-template-columns:1fr;
 }

 nav{
  padding:0 5%;
 }

 .logo{
  font-size:20px;
 }

}

</style>

</head>


<body>


<nav>

<div class="logo">
FAISU <span>AI LAB</span>
</div>

<button
class="navbtn"
onclick="openModal('login')">

Login

</button>

</nav>


<div class="hero">


<div class="heroText">

<div class="badge">
🚀 Free AI Creative Lab
</div>


<h1>

Create With

<span class="gradient">
Artificial Intelligence
</span>

</h1>


<p>

Generate images, videos and scripts
with FAISU AI LAB.

Create your ideas with simple prompts.

</p>


<button
class="navbtn"
onclick="openModal('signup')">

Start Creating Free

</button>

</div>


<div class="heroVisual">

<div class="person">

<div class="hair"></div>

<div class="head"></div>

<div class="headphones"></div>

<div class="laptop">

<div class="screen"></div>

</div>

</div>

</div>


</div>


<section>

<h2 class="sectionTitle">
Explore AI Creation
</h2>


<div class="cards">


<div class="card">

<div class="icon">
🎨
</div>

<h3>
AI Image Creation
</h3>

<p>
Create high-quality images
from simple text prompts.
</p>

</div>


<div class="card">

<div class="icon">
🎬
</div>

<h3>
AI Video Creation
</h3>

<p>
Turn your ideas into
cinematic AI videos.
</p>

</div>


<div class="card">

<div class="icon">
💻
</div>

<h3>
Creative AI Workspace
</h3>

<p>
A modern workspace for
your AI creative projects.
</p>

</div>


</div>

</section>


<section class="cta">

<h2 class="sectionTitle">
Ready To Create?
</h2>

<button
class="navbtn"
onclick="openModal('signup')">

Create Free Account

</button>

</section>


<footer>

FAISU AI LAB © 2026

</footer>


<div class="modal" id="modal">

<div class="box">


<div
class="close"
onclick="closeModal()">

✕

</div>


<div id="loginForm">

<h2>
Login
</h2>


<form
method="post"
action="/login">


<input
name="email"
type="email"
placeholder="Gmail"
required>


<input
name="password"
type="password"
placeholder="Password"
required>


<button class="action">
Login
</button>


</form>


<p style="text-align:center">

Don't have an account?

<a
href="#"
onclick="showSignup()"
style="color:#7c5cff">

Sign Up

</a>

</p>

</div>


<div
id="signupForm"
style="display:none">


<h2>
Create Account
</h2>


<form
method="post"
action="/signup">


<input
name="name"
placeholder="Your Name"
required>


<input
name="email"
type="email"
placeholder="Real Gmail Address"
required>


<input
name="password"
type="password"
placeholder="Password"
required>


<button class="action">

Send Verification Code

</button>

</form>


<p style="text-align:center">

Already have an account?

<a
href="#"
onclick="showLogin()"
style="color:#7c5cff">

Login

</a>

</p>

</div>


</div>

</div>


<script>

function openModal(type){

 document.getElementById(
  "modal"
 ).style.display="flex";

 if(type==="signup")
  showSignup();
 else
  showLogin();

}


function closeModal(){

 document.getElementById(
  "modal"
 ).style.display="none";

}


function showSignup(){

 document.getElementById(
  "loginForm"
 ).style.display="none";

 document.getElementById(
  "signupForm"
 ).style.display="block";

}


function showLogin(){

 document.getElementById(
  "signupForm"
 ).style.display="none";

 document.getElementById(
  "loginForm"
 ).style.display="block";

}

</script>


</body>

</html>
"""


# =========================================================
# SIGNUP
# =========================================================

@app.post("/signup")
def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    con = db()

    cur = con.cursor()

    existing = cur.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    if existing:

        con.close()

        return HTMLResponse(
            """
            <h2>Account already exists.</h2>
            <a href="/">Back</a>
            """
        )


    otp = str(
        secrets.randbelow(900000) + 100000
    )


    cur.execute(
        """
        INSERT INTO users
        (name,email,password,verified,otp)
        VALUES(?,?,?,?,?)
        """,
        (
            name,
            email,
            hash_password(password),
            0,
            otp
        )
    )


    con.commit()
    con.close()


    try:

        send_otp(
            email,
            otp
        )

    except Exception:

        return HTMLResponse(
            """
            <h2>
            Gmail verification could not be sent.
            </h2>

            <p>
            Gmail SMTP settings need to be configured.
            </p>

            <a href="/">
            Back
            </a>
            """
        )


    return HTMLResponse(
        f"""
        <html>

        <body style="
        background:#070b18;
        color:white;
        font-family:Arial;
        text-align:center;
        padding:100px 20px">

        <h1>
        Check Your Gmail 📩
        </h1>

        <p>
        A verification code has been sent to:
        </p>

        <h3>
        {email}
        </h3>

        <form
        method="post"
        action="/verify">


        <input
        name="email"
        value="{email}"
        type="hidden">


        <input
        name="otp"
        placeholder="Enter 6 digit OTP"
        maxlength="6"
        required
        style="
        padding:15px;
        border-radius:10px;
        background:#11172c;
        color:white;
        border:1px solid #555">


        <br><br>


        <button
        style="
        padding:14px 30px;
        border:0;
        border-radius:12px;
        background:#7c5cff;
        color:white">

        Verify Account

        </button>


        </form>

        </body>

        </html>
        """
    )


# =========================================================
# VERIFY
# =========================================================

@app.post("/verify")
def verify(
    email: str = Form(...),
    otp: str = Form(...)
):

    con = db()


    user = con.execute(
        """
        SELECT *
        FROM users
        WHERE email=? AND otp=?
        """,
        (
            email,
            otp
        )
    ).fetchone()


    if not user:

        con.close()

        return HTMLResponse(
            """
            <h2>
            Wrong verification code.
            </h2>

            <a href="/">
            Back
            </a>
            """
        )


    con.execute(
        """
        UPDATE users
        SET verified=1,
            otp=NULL
        WHERE email=?
        """,
        (email,)
    )


    con.commit()
    con.close()


    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )


    response.set_cookie(
        "user_email",
        email,
        httponly=True,
        samesite="lax"
    )


    return response


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):

    con = db()


    user = con.execute(
        """
        SELECT *
        FROM users
        WHERE email=? AND password=?
        """,
        (
            email,
            hash_password(password)
        )
    ).fetchone()


    con.close()


    if not user:

        return HTMLResponse(
            """
            <h2>
            Wrong Gmail or password.
            </h2>

            <a href="/">
            Try again
            </a>
            """
        )


    if user[4] != 1:

        return HTMLResponse(
            """
            <h2>
            Email not verified.
            </h2>

            <p>
            Please verify your Gmail first.
            </p>

            <a href="/">
            Back
            </a>
            """
        )


    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )


    response.set_cookie(
        "user_email",
        email,
        httponly=True,
        samesite="lax"
    )


    return response


# =========================================================
# DASHBOARD
# =========================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    email = request.cookies.get(
        "user_email"
    )


    if not email:

        return RedirectResponse("/")


    con = db()


    user = con.execute(
        """
        SELECT name,email
        FROM users
        WHERE email=?
        AND verified=1
        """,
        (email,)
    ).fetchone()


    con.close()


    if not user:

        return RedirectResponse("/")


    name = user[0]


    return HTMLResponse(
        f"""
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<title>
FAISU AI LAB - AI Dashboard
</title>


<style>

*{{
 box-sizing:border-box;
}}

body{{
 margin:0;
 font-family:Arial;
 color:white;

 background:
 radial-gradient(
  circle at 10% 10%,
  #713cff44,
  transparent 30%
 ),

 radial-gradient(
  circle at 90% 20%,
  #00c6ff33,
  transparent 30%
 ),

 #050816;

 min-height:100vh;
}}


header{{
 padding:25px 7%;

 display:flex;

 justify-content:space-between;

 align-items:center;

 border-bottom:
 1px solid #ffffff12;

 background:#050816aa;
}}


.logo{{
 font-size:25px;
 font-weight:900;
}}


.logo span{{
 color:#7c5cff;
}}


.logout{{
 background:#ffffff12;

 color:white;

 border:
 1px solid #ffffff20;

 padding:10px 18px;

 border-radius:20px;

 cursor:pointer;
}}


main{{
 padding:55px 7%;
}}


.welcome{{
 margin-bottom:45px;
}}


.welcome h1{{
 font-size:42px;
 margin:5px 0;
}}


.welcome p{{
 color:#aab1ca;
}}


.tools{{
 display:grid;

 grid-template-columns:
 repeat(2,1fr);

 gap:25px;
}}


.tool{{
 padding:35px;

 min-height:240px;

 border-radius:28px;

 background:
 linear-gradient(
 145deg,
 #151c3b,
 #0b1024
 );

 border:
 1px solid #ffffff14;

 cursor:pointer;

 transition:.3s;
}}


.tool:hover{{
 transform:
 translateY(-8px);

 border-color:#7c5cff;

 box-shadow:
 0 20px 60px #0005;
}}


.toolIcon{{
 font-size:50px;
}}


.tool h2{{
 margin-bottom:10px;
}}


.tool p{{
 color:#9fa8c2;
 line-height:1.6;
}}


@media(max-width:700px){{

 .tools{{
  grid-template-columns:1fr;
 }}

 main{{
  padding:35px 5%;
 }}

 .welcome h1{{
  font-size:32px;
 }}

}}

</style>

</head>


<body>


<header>

<div class="logo">

FAISU <span>AI LAB</span>

</div>


<button
class="logout"
onclick="location.href='/logout'">

Logout

</button>

</header>


<main>


<div class="welcome">

<p>
Welcome back
</p>


<h1>
Hello, {name} 👋
</h1>


<p>
Your AI creative workspace is ready.
</p>

</div>


<div class="tools">


<div class="tool">

<div class="toolIcon">
🎨
</div>

<h2>
Prompt to Image
</h2>

<p>
Create an image from your text prompt.
</p>

</div>


<div class="tool">

<div class="toolIcon">
🎬
</div>

<h2>
Prompt to Video
</h2>

<p>
Generate an AI video from your prompt.
</p>

</div>


<div class="tool">

<div class="toolIcon">
🖼️🎬
</div>

<h2>
Image + Prompt to Video
</h2>

<p>
Animate your image using an AI prompt.
</p>

</div>


<div class="tool">

<div class="toolIcon">
✨
</div>

<h2>
Video Enhancer
</h2>

<p>
Improve sharpness, clarity and video quality.
</p>

</div>


<div class="tool">

<div class="toolIcon">
📝
</div>

<h2>
AI Script Writer
</h2>

<p>
Generate image and video scripts with AI.
</p>

</div>


</div>

</main>


</body>

</html>
"""
    )


# =========================================================
# LOGOUT
# =========================================================

@app.get("/logout")
def logout():

    response = RedirectResponse("/")

    response.delete_cookie(
        "user_email"
    )

    return response


# =========================================================
# HOME ROUTE
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return HTMLResponse(HOME)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "online",
        "project": "FAISU AI LAB",
        "local_address": "http://faisuailab:8000"
    }


# =========================================================
# ADMIN
# =========================================================

@app.get(
    "/admin",
    response_class=HTMLResponse
)
def admin():

    return HTMLResponse(
        """
        <html>

        <body style="
        background:#070b18;
        color:white;
        font-family:Arial;
        padding:50px">

        <h1>
        FAISU AI LAB Admin
        </h1>

        <p>
        Admin panel will be connected
        to verified users.
        </p>

        </body>

        </html>
        """
    )