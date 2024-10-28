import mysql.connector as con
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# session user id 
uid = st.session_state.uid

# session person id
if "pid" not in st.session_state:
    st.session_state.pid = 0
pid = st.session_state.pid

# connect the database
mydb = con.connect(host="localhost",user="root",passwd="pass",port=3307,database="event_lister")
# create a cursor object to execute SQL queries
mycursor = mydb.cursor(buffered=True)


# sql user data
qry = "SELECT * from users where user_id = %s"
mycursor.execute(qry,(uid,))
data = mycursor.fetchone()

# sql user data check
def profile_check():
    qry = "SELECT * from users where user_id = %s"
    mycursor.execute(qry, (uid,))
    check_data = mycursor.fetchone()
    if check_data !=None:
        return True
    else:
        return False

# sql update user data
def update(fname,lname):
    qry = "UPDATE users set first_name = %s, last_name = %s where user_id = %s"
    val = (fname,lname,uid)
    mycursor.execute(qry,val)
    mydb.commit()

# sql password check
def pass_check(cp):
    qry = "SELECT password from users where user_id = %s"
    mycursor.execute(qry, (uid,))
    pass_data = mycursor.fetchone()
    if pass_data[0] == cp:
        return True
    else:
        return False

# sql update password
def change_pass(np):
    qry = "UPDATE users set password = %s where user_id = %s"
    val = (np,uid)
    mycursor.execute(qry,val)
    mydb.commit()


# sql add person data
def add_data(fname,lname,address,phone,amount):
    qry = "INSERT into "+uid+"(first_name, last_name, address, phone, amount) values (%s, %s, %s, %s, %s)"
    val = (fname,lname,address,phone,amount)
    mycursor.execute(qry,val)
    mydb.commit()

# sql check person id exists
def person_check(id):    
    qry = "SELECT * from "+uid+" where id = %s"
    val = (id,)
    mycursor.execute(qry,val)
    result = mycursor.fetchone()
    if result != None:
        return True
    else:
        return False

# sql get person details
def person_get(id):    
    qry = "SELECT * from "+uid+" where id = %s"
    val = (id,)
    mycursor.execute(qry,val)
    return mycursor.fetchone()

# sql delete person details
def person_delete(id):    
    qry = "DELETE from "+uid+" where id = %s"
    val = (id,)
    mycursor.execute(qry,val)
    mydb.commit()

# sql search person data
def data_check(qry,val):
    mycursor.execute(qry,val)
    result = mycursor.fetchone()
    if result != None:
        return True
    else:
        return False

# sql show person data
def search_data(qry,val):
    mycursor.execute(qry,val)
    result = mycursor.fetchall()
    return result

# sql update data
def data_edit(fname,lname,address,phone,amount,id,uid):
    qry = "UPDATE "+uid+" set first_name=%s,last_name=%s,address=%s,phone=%s,amount=%s where id = %s"
    val = (fname,lname,address,phone,amount,id)
    mycursor.execute(qry,val)
    mydb.commit()

# sql mark paid
def payment(id,):
    qry = "UPDATE "+uid+" set payment = 'paid' where id = %s"
    val = (id,)
    mycursor.execute(qry,val)
    mydb.commit()

# sql paid check
def paid_check():
    qry = "SELECT * from "+uid+" where payment ='paid'"
    mycursor.execute(qry)
    result = mycursor.fetchone()
    if result != None:
        return True
    else:
        return False

def pending_check():
    qry = "SELECT * from "+uid+" where payment ='pending'"
    mycursor.execute(qry)
    result = mycursor.fetchone()
    if result != None:
        return True
    else:
        return False

# sql payment check
def payment_check():
    qry = "SELECT sum(amount) from "+uid+" group by payment order by payment"
    mycursor.execute(qry)
    result = mycursor.fetchone()
    if result != None:
        return True
    else:
        return False

# sql payment status
def payment_status():
    qry = "SELECT sum(amount) from "+uid+" group by payment order by payment"
    mycursor.execute(qry,)
    result = mycursor.fetchall()
    return result

# sql show all data
def display_all():
    qry = "SELECT id,first_name,last_name,address,phone,amount,payment from "+uid
    mycursor.execute(qry)
    result = mycursor.fetchall()
    return result


# full page
st.set_page_config(page_title="Event Lister", page_icon=r"images\chz.png", layout="wide")


# css
with open(r"css\main.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


# Selected page
if "page" not in st.session_state:
    st.session_state.page = "Table"
selected = st.session_state.page


# Table pages
if "sel1" not in st.session_state:
    st.session_state.sel1 = "View"
sel1 = st.session_state.sel1
# Table page default
if selected != "Table":
    st.session_state.sel1 = "View"
sel1 = st.session_state.sel1
# Table page changes
def view():
    sel1 = "View"
    st.session_state.sel1 = sel1
def add():
    sel1 = "Add"
    st.session_state.sel1 = sel1
def search():
    sel1 = "Search"
    st.session_state.sel1 = sel1
def change():
    sel1 = "Change"
    st.session_state.sel1 = sel1


# Table change page
if "sel2" not in st.session_state:
    st.session_state.sel2 = "Find"
sel2 = st.session_state.sel2
# Table change page default
if sel1 != "Change":
    st.session_state.sel2 = "Find"
sel2 = st.session_state.sel2
# Table change page changes
def find():
    sel2 = "Find"
    st.session_state.sel2 = sel2
def change_edit():
    sel2 = "Edit"
    st.session_state.sel2 = sel2


# Profile pages
if "sel3" not in st.session_state:
    st.session_state.sel3 = "Display"
sel3 = st.session_state.sel3
# Profile page default
if selected != "Profile":
    st.session_state.sel3 = "Display"
sel3 = st.session_state.sel3
# profile page changes
def prof():
    sel3 = "Display"
    st.session_state.sel3 = sel3
def edit():
    sel3 = "Edit"
    st.session_state.sel3 = sel3
def password():
    sel3 = "Password"
    st.session_state.sel3 = sel3


# header container
header = st.container()
# content container
content = st.container(height = 502, border = True)


# Header
with header:
    b1,logo,table,chart,profile,signout = st.columns([0.1,4,0.5,0.5,0.6,0.6], vertical_alignment="bottom")
    # logo
    logo.image(r"images\logo.png")
    # table
    if table.button("table"):
        selected = "Table"
        st.session_state.page = selected
        view()
    # chart
    if chart.button("chart"):
        selected = "Chart"
        st.session_state.page = selected
    # profle 
    if profile.button("profile"):
        selected = "Profile"
        st.session_state.page = selected
        prof()
    # signout
    if signout.button("signout"):
        st.session_state.uid = None
        st.session_state.select = "Home"
        st.session_state.page = "Table"
        st.switch_page(r"main.py")


# layout class
class Layout:

    # Table Content
    def table(self):
        with content:
            b1,rows,btn1,btn2,btn3,btn4,b2 = st.columns([2,2,0.6,0.5,0.7,0.6,2], vertical_alignment="bottom")
            rows.image(r"images\table.png")

            # buttons in table page
            if btn1.button("view"):
                view()
            if btn2.button("add"):
                add()
            if btn3.button("search"):
                search()
            if btn4.button("edit"):
                change()
                find()
                

            # b1,rows,b2 = st.columns([2,3,2])
            # View table
            if sel1 == "View": 
                result = display_all()

                # Dataframe creation
                df = pd.DataFrame(result,columns=("ID","First Name","Last Name","Address","Phone","Amount","Payment"))
                st.dataframe(df,width=1240,height=370,hide_index=True) 

            # Add table
            if sel1 == "Add":
                with st.form("add",clear_on_submit=True,enter_to_submit=False,border=False):
                    b1,first,last,b2 = st.columns([2,1.5,1.5,2])
                    fname = first.text_input("First Name")
                    lname = last.text_input("Last Name")

                    b1,rows,b2 = st.columns([2,3,2])
                    address = rows.text_area("Address",height=2)
                    
                    b1,phn,amo,b2 = st.columns([2,1.5,1.5,2])
                    phone = phn.text_input("Phone")
                    amount = amo.text_input("Amount")

                    # add new person to the list
                    b1,btn,stat,b2 = st.columns([2,0.6,2.4,2])
                    if btn.form_submit_button("submit"):
                        if fname != "" and amount != "":
                            if amount.isnumeric():
                                if phone == "" and amount != "":
                                    add_data(fname,lname,address,phone,amount)
                                    stat.success("Data added successfully.")
                                elif phone != "" and phone.isnumeric():
                                    add_data(fname,lname,address,phone,amount)
                                    stat.success("Data added successfully.")
                                else:
                                    stat.error("Invalid Input. Enter a number.")
                            else:
                                stat.error("Invalid Input. Enter a number.")
                        else:
                            stat.error("Fill in the required fields.")

            # Search table
            if sel1 == "Search": 
                with st.form("search",enter_to_submit=False,border=False):

                    b1,opt,inp,btn,b2 = st.columns([2,1.3,1.7,1,1.5], vertical_alignment="bottom")
                    b1,stat,b2 = st.columns([2,3.5,2], vertical_alignment="bottom")

                    user_op = opt.selectbox("SELECT Search", ("First Name:","Last name:","Address:","Phone:","Amount:"),index=0,placeholder="Choose one:",label_visibility="collapsed")

                    user_inp = inp.text_input("Search",label_visibility="collapsed")

                    # search table
                    if btn.form_submit_button("find"):
                        if user_op != "":
                            # search first name
                            if user_op == "First Name:":
                                qry = "SELECT id,first_name,last_name,address,phone,amount from "+uid+" where first_name = %s"
                                val = (user_inp,)
                                if data_check(qry,val):
                                    result = search_data(qry,val)
                                    df = pd.DataFrame(result,columns=("ID","First Name","Last Name","Address","Phone","Amount"))
                                    st.dataframe(df,width=1240,height=300,hide_index=True)
                                else:
                                    stat.error("No data found.")

                            # search last name
                            elif user_op == "Last name:":
                                qry = "SELECT id,first_name,last_name,address,phone,amount from "+uid+" where last_name = %s"
                                val = (user_inp,)
                                if data_check(qry,val):
                                    result = search_data(qry,val)
                                    df = pd.DataFrame(result,columns=("ID","First Name","Last Name","Address","Phone","Amount"))
                                    st.dataframe(df,width=1240,height=300,hide_index=True)
                                else:
                                    stat.error("No data found.")

                            # search address
                            elif user_op == "Address:":
                                qry = "SELECT id,first_name,last_name,address,phone,amount from "+uid+" where address = %s"
                                val = (user_inp,)
                                if data_check(qry,val):
                                    result = search_data(qry,val)
                                    df = pd.DataFrame(result,columns=("ID","First Name","Last Name","Address","Phone","Amount"))
                                    st.dataframe(df,width=1240,height=300,hide_index=True)
                                else:
                                    stat.error("No data found.")

                            # search phone
                            elif user_op == "Phone:":
                                if user_inp.isnumeric():
                                    qry = "SELECT id,first_name,last_name,address,phone,amount from "+uid+" where phone = %s"
                                    val = (user_inp,)
                                    if data_check(qry,val):
                                        result = search_data(qry,val)
                                        df = pd.DataFrame(result,columns=("ID","First Name","Last Name","Address","Phone","Amount"))
                                        st.dataframe(df,width=1240,height=300,hide_index=True)
                                    else:
                                        stat.error("No data found.")
                                else:
                                    stat.error("Invalid phone number.")

                            # search amount
                            elif user_op == "Amount:":
                                if user_inp.isnumeric():
                                    qry = "SELECT id,first_name,last_name,address,phone,amount from "+uid+" where amount = %s"
                                    val = (int(user_inp),)
                                    if data_check(qry,val):
                                        result = search_data(qry,val)
                                        df = pd.DataFrame(result,columns=("ID","First Name","Last Name","Address","Phone","Amount"))
                                        st.dataframe(df,width=1240,height=300,hide_index=True)
                                    else:
                                        stat.error("No data found.")
                                else:
                                    stat.error("Invalid amount.")

                        else:
                            stat.error("Please SELECT a search option.")

            # Change table
            if sel1 == "Change": 
                with st.form("change",enter_to_submit=False,border=False):
                    b1,entry,opt,btn,b2 = st.columns([3,1,1,1,3], vertical_alignment="bottom")
                    b1,stat,b2 = st.columns([2.7,2.5,3])
                    id = entry.text_input("ID Number:",placeholder="Enter ID:",label_visibility="collapsed")

                    option = opt.selectbox("Operation",("find","edit","delete"),index=0,placeholder="Choose one:",label_visibility="collapsed")

                    # list data operations call
                    if btn.form_submit_button("submit"):
                        if id != "":
                            if id.isnumeric():
                                if person_check(id):
                                    if option == "find":
                                        find()
                                    elif option == "edit":
                                        change_edit()
                                    elif option == "delete":
                                        person_delete(id)
                                        stat.error("Data deleted.")
                                else:
                                    stat.error("No data found.")
                            else:
                                stat.error("Invalid ID number.")
                        else:
                            stat.error("Please enter a valid ID number.")

                    # list data operations
                    if id != "":
                        if person_check(id):
                            # find operation
                            if sel2 == "Find":
                                list_data = person_get(id)

                                b1,first,last,b2 = st.columns([2,1.5,1.5,2])
                                fname = first.text_input("First Name",value=list_data[1],disabled=True)
                                lname = last.text_input("Last Name",value=list_data[2],disabled=True)

                                b1,rows,b2 = st.columns([2,3,2])
                                address = rows.text_input("Address",value=list_data[3],disabled=True)
                                
                                b1,phn,amo,b2 = st.columns([2,1.5,1.5,2])
                                phone = phn.text_input("Phone",value=list_data[4],disabled=True)
                                amount = amo.text_input("Amount",value=list_data[5],disabled=True)

                                b1,btn,stat,b2 = st.columns([2,0.6,2.4,2])
                                if btn.form_submit_button("paid"):
                                    payment(id)
                                    stat.success("Marked as Paid.")
                            
                            # edit operation
                            elif sel2 == "Edit":
                                list_data = person_get(id)

                                b1,first,last,b2 = st.columns([2,1.5,1.5,2])
                                fname = first.text_input("First Name",value=list_data[1])
                                lname = last.text_input("Last Name",value=list_data[2])

                                b1,rows,b2 = st.columns([2,3,2])
                                address = rows.text_input("Address",value=list_data[3])
                                
                                b1,phn,amo,b2 = st.columns([2,1.5,1.5,2])
                                phone = phn.text_input("Phone",value=list_data[4])
                                amount = amo.text_input("Amount",value=list_data[5])

                                b1,btn,stat,b2 = st.columns([2,0.6,2.4,2])
                                if btn.form_submit_button("change"):
                                    if fname != "" and address != "" and amount != "":
                                        data_edit(fname,lname,address,phone,amount,id,uid)
                                        stat.success("Data updated successfully.")
                                    else:
                                        stat.error("Fill in the required fields.")

    # Chart Content
    def chart(self):
        with content:
            b1,rows,val,b2 = st.columns([2,3,1,1])
            rows.image(r"images\chart.png") 
            
            if pending_check():
                if paid_check():
                    if payment_check():
                        # paid and unpaid
                        status = payment_status()
                        paid = status[0][0]
                        unpaid = status[1][0]
                        total = paid + unpaid


                        val.text_input("Total:",value=total,disabled=True)
                        val.text_input("Paid:",value=paid,disabled=True)
                        val.text_input("Unpaid:",value=unpaid,disabled=True)

                        # pie chart values
                        sizes = [paid, unpaid]
                        label = ["Paid", "Unpaid"]
                        color = ["#5CA041","#D75959"]
                        exp = [0.001,0.0]
                        
                        # pie chart creation
                        pie_chart,ax = plt.subplots() 
                        ax.pie(sizes, labels=label, colors=color, explode=exp, autopct="%1.2f%%", radius=0.01, textprops = {"fontsize":12})
                        ax.axis("equal")
                        pie_chart.set_facecolor('#e7dfd8')
                        plt.legend(loc="upper left", facecolor="#C9C2C0")
                        rows.pyplot(pie_chart)
                else:
                    status = payment_status()
                    paid = 0
                    unpaid = status[0][0]
                    total = paid + unpaid

                    val.text_input("Total:",value=total,disabled=True)
                    val.text_input("Paid:",value=paid,disabled=True)
                    val.text_input("Unpaid:",value=unpaid,disabled=True)

                    # pie chart values
                    sizes = [paid, unpaid]
                    label = ["Paid", "Unpaid"]
                    color = ["#5CA041","#D75959"]
                    exp = [0.001,0.0]
                    
                    # pie chart creation
                    pie_chart,ax = plt.subplots() 
                    ax.pie(sizes, labels=label, colors=color, explode=exp, autopct="%1.2f%%", radius=0.01, textprops = {"fontsize":12})
                    ax.axis("equal")
                    pie_chart.set_facecolor('#e7dfd8')
                    plt.legend(loc="upper left", facecolor="#C9C2C0")
                    rows.pyplot(pie_chart)
            else:
                new_title = '<p style="font-family:monospace; color:#7d7d7d; font-size: 30px;">No Data Available.</p>'
                rows.markdown(new_title, unsafe_allow_html=True)
                val.text_input("Total:",value=0,disabled=True)
                val.text_input("Paid:",value=0,disabled=True)
                val.text_input("Unpaid:",value=0,disabled=True)

    # Profile Content
    def profile(self):
        # Display profile
        if profile_check():
            if sel3 == "Display": 
                with content:
                    b1,rows,b2 = st.columns([2,3,2])
                    with rows:
                        st.image(r"images\profile.png")
                        st.text_input("First Name",value=data[1],disabled=True)
                        st.text_input("Last Name",value=data[2],disabled=True)
                        st.text_input("User ID",value=data[3],disabled=True)
                        if st.button("edit"):
                            edit()
            
            # Edit profile
            elif sel3 == "Edit":
                with content: 
                    with st.form("edit",clear_on_submit=True,enter_to_submit=False,border=False):
                        b1,rows,b2 = st.columns([2,3,2], )
                        with rows:
                            st.image(r"images\edit.png")
                            fname = st.text_input("First Name",value=data[1])
                            lname = st.text_input("Last Name",value=data[2])
                            uid = st.text_input("User ID",value=data[3],disabled=True)
                        b1,btn1,btn2,stat,b2 = st.columns([1.8,0.5,1,1,2], )
                        if btn1.form_submit_button("submit"):
                            if fname != "" and lname != "":
                                update(fname,lname)
                                stat.success("Updation Successful")
                                prof()
                            else:
                                stat.error("All fields are required")
                        if btn2.form_submit_button("change password"):
                            password()

            # Password change
            elif sel3 == "Password":
                with content:  
                    with st.form("pass",clear_on_submit=True,enter_to_submit=False,border=False):
                        b1,rows,b2 = st.columns([2,3,2], )
                        with rows:
                            st.image(r"images\change.png")
                            cp = st.text_input("Current Password",type="password")
                            np = st.text_input("New Password",type="password")
                            cnp = st.text_input("Confirm Password",type="password")
                        b1,sub,stat,b2 = st.columns([2,0.6,2.4,2], ) 
                        if sub.form_submit_button("submit"):
                            if cp != "" and np != "" and cnp != "":
                                if pass_check(cp):
                                    if np == cnp:
                                        change_pass(np)
                                        stat.success("Password changed successfully")
                                        prof()
                                    else:
                                        stat.error("New Passwords doesn't match") 
                                else:
                                    stat.error("Incorrect Password")   
                            else:
                                stat.error("All fields are required")


# Load Object called
load = Layout()

# Page Loader
if selected == "Table":
    load.table()

elif selected == "Chart":
    load.chart()

elif selected == "Profile":
    load.profile()