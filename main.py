import mysql.connector as con
import streamlit as st
import time


# connect the database
mydb = con.connect(host="localhost",user="root",passwd="chz0188666",port=3307,database="event_lister")
# create a cursor object to execute SQL queries
mycursor = mydb.cursor()


# sql check if user already exists
def user_check(user):    
    qry = "SELECT * from users where user_id = %s"
    val = (user,)
    mycursor.execute(qry,val)
    result = mycursor.fetchone()
    if result == None:
        return True
    else:
        return False

def sql_create(user_id):
    qry="CREATE table if not exists "+user_id+"(`id` INT NOT NULL AUTO_INCREMENT,`first_name` VARCHAR(45) NOT NULL,`last_name` VARCHAR(45) NULL,`address` VARCHAR(45) NULL,`phone` VARCHAR(45) NULL,`amount` VARCHAR(45) NOT NULL,`payment` VARCHAR(45) NULL DEFAULT 'pending',PRIMARY KEY (`id`))"
    # val=(qry.formate(table=user_id))
    mycursor.execute(qry)
    mydb.commit()


# sql signup 
def sql_signup(first,last,user,password):
    qry = "INSERT into users(first_name,last_name,user_id,password) values(%s,%s,%s,%s)"
    val = (first,last,user,password)
    mycursor.execute(qry,val)
    mydb.commit()
    
    
# sql login
def sql_login(user,password):
    qry = "SELECT * from users where user_id = %s"
    val = (user,)
    mycursor.execute(qry,val)
    result = mycursor.fetchone()
    if result != None: 
        if result[4] == password:
            return True
        else:
            return False
    else:
        return False


# full page
st.set_page_config(page_title="Event Lister", page_icon=r"images\chz.png", layout="wide")


# css
with open(r"css\main.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


# Selected page
if "select" not in st.session_state:
    st.session_state.select = "Home"
selected = st.session_state.select


# header container
header = st.container()
# content container
content = st.container(height = 480, border = True)


# image reset
dis_img = st.empty()


# Header
with header:
    b1,logo,home,login,signup = st.columns([0.1,4,0.5,0.5,0.5], vertical_alignment="bottom")
    logo.image(r"images\logo.png")
    if home.button("home"):
        selected = "Home"
        st.session_state.select = selected
    if login.button("login"):
        selected = "Login"
        st.session_state.select = selected
    if signup.button("signup"):
        selected = "Signup"
        st.session_state.select = selected


# layout class
class Layout:

    # Home Page Content
    def home(self):
        with content:
            b1,intro,b3,img,b4 = st.columns([2,3,1,5,1])
            intro.image(r"images\heading1.png")
            intro.write("Introducing my new app, Event Lister. Here we aim to replace the traditional approach of listing event money collection with a simpler and modern approach. Here we can search & find the people who have contributed & also we can mark them as paid when we repay them. We can also see a chart of people who is yet to be repaid & of those who we already repaid.")
            while True:
                dis_img = img.image(r"images\home1.png")
                time.sleep(2)
                dis_img.empty()
                dis_img = img.image(r"images\home2.png")
                time.sleep(2)
                dis_img.empty()
                dis_img = img.image(r"images\home3.png")
                time.sleep(2)
                dis_img.empty()

    # Login Page Content
    def login(self):
        with content:
            with st.form("login",clear_on_submit=True,enter_to_submit=False,border=False):
                # Login Form
                b1,rows,b2 = st.columns([2,3,2])
                rows.image(r"images\heading3.png")

                # User Inputs
                user_id = rows.text_input("User ID")
                password = rows.text_input("Password",type="password")
                
                b1,sub,stat,b2 = st.columns([2,0.5,2.5,2])
                # Submit Button
                submit = sub.form_submit_button("Login")

                if submit:
                    if user_id != "" and password != "":
                        if sql_login(user_id, password):
                            stat.success("Login Success!")
                            if "uid" not in st.session_state:
                                st.session_state.uid = user_id
                            user_id = st.session_state.uid
                            st.switch_page(r"pages\page.py")
                        else:
                            stat.error("Invalid User ID or Password!")
                    else:
                        stat.error("Please enter User ID and Password!")

    # Signup Page Content
    def signup(self):
        with content:
            with st.form("signup",clear_on_submit=True,enter_to_submit=False,border=False):
                # Signup Heading
                b1,rows,b2 = st.columns([2,3,2])
                rows.image(r"images\heading4.png")

                # User Name
                b1,first,last,b2 = st.columns([2,1.5,1.5,2])
                first_name = first.text_input("First Name")
                last_name = last.text_input("Last Name")

                # User ID
                b1,user,b2 = st.columns([2,3,2])
                user_id = user.text_input("User ID")

                # User Password
                b1,pw,cpw,b2= st.columns([2,1.5,1.5,2])
                password = pw.text_input("Password",type="password")
                confirm_password = cpw.text_input("Confirm Password",type="password")
                
                # Submit Button
                b1,sign,stat,b2 = st.columns([2,0.6,2.4,2])
                submit = sign.form_submit_button("Signup")

                if submit:
                    if first_name != "" and last_name != "" and user_id != "" and password != "" and confirm_password != "":
                        if user_check(user_id):
                            if password == confirm_password:
                                sql_create(user_id)
                                sql_signup(first_name,last_name,user_id,password)
                                stat.success("Account Created!")
                            else:
                                stat.error("Passwords do not match!")
                        else:
                            stat.error("User ID already exists!")
                    else:
                        stat.error("All fields are required!")


# Load Object called
load = Layout()

# Page Loader
if selected == "Home":
    load.home()

elif selected == "Login":
    load.login()

elif selected == "Signup":
    load.signup()