#import streamlit as st
import sqlite3
import streamlit as st
global sff

conn=sqlite3.connect("db21.db")
conn.execute("PRAGMA foreign_keys = 1")
cur=conn.cursor()

def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS company_info 
            (c_name NVARCHAR(50) NOT NULL PRIMARY KEY ,
             c_add NVARCHAR(50) NOT NULL,
             c_gst NVARCHAR(50) NOT NULL UNIQUE)''')      
    
    cur.execute('''CREATE TABLE IF NOT EXISTS machineinfotable
            ( 
             machine_name NVARCHAR(50) NOT NULL ,
             c_name NVARCHAR(50) NOT NULL, 
             FOREIGN KEY (c_name) REFERENCES company_info(c_name))''')
            
    cur.execute('''CREATE TABLE IF NOT EXISTS vendor_info 
            (
             v_name NVARCHAR(50) NOT NULL PRIMARY KEY ,
             v_add NVARCHAR(50) NOT NULL,
             gstno NVARCHAR(50) NOT NULL UNIQUE) ''')     
            
    cur.execute('''CREATE TABLE IF NOT EXISTS materialinfo 
            (
             v_name NVARCHAR(50) NOT NULL ,
             co_name NVARCHAR(50) NOT NULL,
             mname NVARCHAR(50) NOT NULL,
             mat_name NVARCHAR(50) NOT NULL,
             cost NVARCHAR(50) NOT NULL,
             m_quantity NVARCHAR(50) NOT NULL,
             m_gst NVARCHAR(50) NOT NULL,
             m_total REAL NOT NULL) ''')
    
    conn.commit()
def add_company(name,add,gst):
    try:
        cur.execute('''INSERT INTO company_info VALUES(?,?,?)''',( name,add, gst))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Company Already Exist")
                return 0
def show_company():
    
    m=cur.execute('''SELECT *FROM company_info''')
    st.table(m.fetchall())
def add_machine(m_name,cname):
    try:
        
        cur.execute('''INSERT INTO machineinfotable VALUES(?,?)''',(m_name,cname))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Machine Already Exist")
                return 0
def add_vendor(vname,address,gstno):
    try:
        cur.execute('''INSERT INTO vendor_info VALUES(?,?,?)''',( vname,address,gstno))
        conn.commit()
        
    except sqlite3.IntegrityError:
                st.info("Vendor Already Exist")
                return 0

def add_material(vendorname,co_name,machinename,materialname,mcost,qn,mgst,mtotal) :
    try:
        
        cur.execute('''INSERT INTO materialinfo VALUES(?,?,?,?,?,?,?,?)''',(vendorname,co_name,machinename,materialname,mcost,qn,mgst,mtotal))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Material Already Exist")
                return 0


def show_machine():
        m1=cur.execute('''SELECT *FROM machineinfotable''')
        st.table(m1.fetchall())


def show_company():
    
    m=cur.execute('''SELECT *FROM company_info''')
    st.table(m.fetchall())
def cname_entry():
    m2=cur.execute("SELECT c_name FROM  company_info")
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
# st.write(pairs)

def vendor_entry():
    m2=cur.execute("SELECT v_name FROM  vendor_info")
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs

def machine_entry(name1):
    m2=cur.execute('SELECT machine_name FROM  machineinfotable WHERE c_name="{}"'.format(name1))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def show_vendor():
    
    m=cur.execute('''SELECT *FROM vendor_info''')
    st.table(m.fetchall())
def search_by_cname(cnm):
    try:
        cur.execute('SELECT * FROM company_info WHERE c_name="{}"'.format(cnm))
        data = cur.fetchall()
        return data
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
    
def search_by_mcname(mcn):
    try:
        cur.execute('SELECT * FROM machineinfotable WHERE c_name="{}"'.format(mcn))
        data = cur.fetchall()
        return data
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
   
def total(cost1,quantity1,gst1):
    gst_cost= ((float(cost1)*float(gst1)/100))*float(quantity1)
    
    total1=float(cost1) + float(gst_cost)
    return float(total1)

def Bills():
     try:
        cur.execute('SELECT * FROM materialinfo')
        data = cur.fetchall()
        return data
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0

# -----------------------------------------------------------------------------------------------
st.title("Management ")

create_table()

menu = ["Home", "Add Company", "Add Machine","Add Vendor","Add Material","Show Details","Search","Bills"]
choice = st.sidebar.selectbox("Menu", menu)
if choice == "Home":
    st.write("WELCOME")

elif choice == "Add Company":
    with st.form(key='Company Information'):
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            name1 = st.text_input("Enter Company Name" )
        with col2:
            add1=st.text_input("Enter Address")
        with col3:
            gst1=st.text_input("Enter GST No. ")
        submit1 = st.form_submit_button(label='Save')
    if submit1:
        s = add_company(name1, add1, gst1)
        print(s)
        if s == 0:
            st.error("Not Added")
        else:
            st.success("Successfully added")


        # name1 = st.text_input("Enter Company Name" )

        # print(name1)
        # add1=st.text_input("Enter Address")
        # gst1=st.text_input("Enter GST No. ")
        # b=st.button("Save")
        # if b:
        #     s = add_company(name1, add1, gst1)
        #     print(s)
        #     if s == 0:
        #         st.error("Not Added")
        #     else:
        #         st.success("Successfully added")
     
elif choice == "Add Machine":  
    with st.form(key='Machine_form'):
   
        data=cname_entry()
        cname=st.selectbox('Select company', data)
        mname=st.text_input("Machine name")
        submit2 = st.form_submit_button(label='Save')
        if submit2:
            s2=add_machine(mname, cname) 
            if s2==0:
                st.error("Not Added")      
            else :
               st.success("Successfully added")


elif choice == "Add Vendor":
     with st.form(key='Machine_form'):
         
         name3 = st.text_input("Enter Vendor Name" )
         print(name3)
         add2=st.text_input("Enter Address")
         gst2=st.text_input("Enter GST No. ")

         submit3 = st.form_submit_button(label='Save')
         if submit3:
            s3 = add_vendor(name3, add2,gst2)
            print(s3)
            if s3 == 0:
                st.error("Not Added")
            else:
                st.success("Successfully added")           
                
elif choice == "Add Material":
    with st.form(key='Material Information'):
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            
            data2=vendor_entry()
            vendorn=st.selectbox('Select Vendor', data2)
        with col2:
            
            data3=cname_entry()
            coname=st.selectbox('Select company', data3)
            
        with col3:
            
            data4=machine_entry(coname)
            machine=st.selectbox('Select machine', data4)
        submit4 = st.form_submit_button(label='Add')
        
    with st.form(key='Material Information1'):
        col1,col2,col3,col4 = st.columns([1,1,1,1])
        with col1:
            
            mname2 = st.text_input("Enter material" )
        with col2:
            
            cost2=st.text_input("Enter cost")
        with col3:
            
            quantity=st.text_input("Enter quantity")
        with col4:
            gst2=st.text_input("Enter GST")
            
        submit5 = st.form_submit_button(label='Add')
        amount1=total(cost2,quantity,gst2)
        amount=float(amount1)
        if submit5:
            s4=add_material(vendorn,coname,machine,mname2,cost2,quantity,gst2,amount) 
            if s4==0:
                st.error("Not Added")      
            else :
               st.success("Successfully added")
              
              

     
elif choice== "Show Details":
   show_company()
   show_machine()
   show_vendor()



elif choice=="Search":
        name2 = st.text_input("Enter Company Name to search" )
        searched_data1=search_by_cname(name2)
        searched_data2=search_by_mcname(name2)
        st.table(searched_data1)
        st.table(searched_data2)

elif choice=="Bills":
    bill=Bills()
    st.table(bill)
    
    













