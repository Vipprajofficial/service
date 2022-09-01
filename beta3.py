#import streamlit as st
import sqlite3
import streamlit as st
global sff

conn=sqlite3.connect("database07.db")
conn.execute("PRAGMA foreign_keys = 1")
cur=conn.cursor()

def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS company_info 
            (
             company_name NVARCHAR(50) NOT NULL PRIMARY KEY ,
             company_add NVARCHAR(50) NOT NULL,
             company_gst NVARCHAR(50) NOT NULL UNIQUE)''')
            #company_id INTEGER NOT NULL UNIQUE AUTOINCREMENT,
    cur.execute('''CREATE TABLE IF NOT EXISTS machinetable
            ( 
            
             machine_name NVARCHAR(50) NOT NULL  PRIMARY KEY)''')
             #machine_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            
    # cur.execute('''CREATE TABLE IF NOT EXISTS machineinfotable
    #         ( 
    #          machineinfo_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #          mmachine_name NVARCHAR(50) NOT NULL ,
    #          mcompany_name NVARCHAR(50) NOT NULL, 
    #          FOREIGN KEY (mcompany_name) REFERENCES company_info(company_name),
    #          FOREIGN KEY (mmachine_name) REFERENCES machinetable(machine_name))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS purchaseorder
            ( 
             po_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             pcompany_name NVARCHAR(50) NOT NULL ,
             po_no INTEGERNVARCHAR(50) NOT NULL,
             pmachine_name NVARCHAR(50) NOT NULL, 
             pmquantity INTEGER NOT NULL,
             pmcost REAL NOT NULL,
             FOREIGN KEY (pcompany_name) REFERENCES company_info(company_name),
             FOREIGN KEY (pmachine_name) REFERENCES machinetable(machine_name))''')
            
    cur.execute('''CREATE TABLE IF NOT EXISTS machine_estimate_by_sfood
                ( 
                 machine_estimate_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 mecompany_name NVARCHAR(50) NOT NULL,
                 po_no NVARCHAR(50) NOT NULL,
                 memachine_name NVARCHAR(50) NOT NULL,
                 memquantity INTEGER NOT NULL,
                 memcost REAL NOT NULL,
                 FOREIGN KEY (mecompany_name) REFERENCES company_info(company_name),
                 FOREIGN KEY (memachine_name) REFERENCES machinetable(machine_name))''')
                #
                # FOREIGN KEY (cname) REFERENCES company_info(c_name),
                # FOREIGN KEY (machine_name) REFERENCES machinetable(mch_name)


    cur.execute('''CREATE TABLE IF NOT EXISTS collection
            (
             collection_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             ccompany_name NVARCHAR(50) NOT NULL,
             cpo_no NVARCHAR(50) NOT NULL,
             cmachine_name NVARCHAR(50) NOT NULL ,
             cdatetime TEXT NOT NULL,
             ccustomer_name NVARCHAR(50) NOT NULL,
             cmobile_number INTEGER(10) NOT NULL,
             ctransaction_type NVARCHAR(50) NOT NULL,
             ctransaction_id NVARCHAR(50) NOT NULL, 
             cmachine_cost NVARCHAR(50) NOT NULL,
             FOREIGN KEY (ccompany_name) REFERENCES company_info(company_name),
             FOREIGN KEY (cmachine_name) REFERENCES machinetable(machine_name)
             )''')
            
    cur.execute('''CREATE TABLE IF NOT EXISTS vendor_info 
            (
             v_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             v_name NVARCHAR(50) NOT NULL UNIQUE ,
             v_add NVARCHAR(50) NOT NULL,
             gstno NVARCHAR(50) NOT NULL UNIQUE) ''')     
            
    cur.execute('''CREATE TABLE IF NOT EXISTS materialinfo 
            (material_info_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             v_name NVARCHAR(50) NOT NULL ,
             co_name NVARCHAR(50) NOT NULL,
             mname NVARCHAR(50) NOT NULL,
             mat_name NVARCHAR(50) NOT NULL,
             cost REAL NOT NULL,
             m_quantity REAL NOT NULL,
             m_gst REAL NOT NULL,
             m_total REAL NOT NULL,
             FOREIGN KEY (v_name) REFERENCES vendor_info(v_name)) ''')
    
    conn.commit()
def add_company(cname1,address1,gst1):
    try:
        cur.execute('''INSERT INTO company_info(company_name,company_add,company_gst) VALUES(?,?,?)''',(name1,address1, gst1))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Company Already Exist")
                return 0
def show_company():
    
    query1=cur.execute('''SELECT *FROM company_info''')
    st.table(query1.fetchall())

def add_machine(machine1):
    try:
        cur.execute('''INSERT INTO machinetable(machine_name) VALUES(?)''',(machine1))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Machine Already Exist")
                return 0
def show_machine():
    
    query2=cur.execute('''SELECT *FROM machinetable''')
    st.table(query2.fetchall())
def add_purchase_order_info(cname2,po2,mname2,mqut2,mcost2):
    try:
        cur.execute('''INSERT INTO purchaseorder(pcompany_name,po_no,pmachine_name,pmquantity,pmcost) VALUES(?,?,?,?,?)''',(cname2,po2,mname2,mqut2,mcost2))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Error")
                return 0
def show_purchase_order_info():
    
    m=cur.execute('''SELECT *FROM purchaseorder''')
    st.table(m.fetchall())
    
def add_machine_estimate(cname3,po3,mname3,mquantity3,mcost3):
    try:
        
        cur.execute('''INSERT INTO machine_estimate_by_sfood(mecompany_name,po_no,memachine_name,memquantity,memcost) VALUES(?,?,?,?,?)''',(cname3,po3,mname3,mquantity3,mcost3))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Machine Already Exist")
                return 0
            

def show_machine_estimate():
        query3=cur.execute('''SELECT *FROM machine_estimate_by_sfood''')
        st.table(query3.fetchall())
        
def add_collection(cname4,po4,mname4,cusname4,mobno4,tran_type4,tran_id4,mcost4):
    
        d1=cur.execute("SELECT datetime('now','localtime')")
        d2=d1.fetchall()
        date1=d2[0][0]
        cur.execute('''INSERT INTO collection(ccompany_name,cpo_no,cmachine_name,cdatetime,ccustomer_name,cmobile_number,ctransaction_type,ctransaction_id,cmachine_cost) VALUES(?,?,?,?,?,?,?,?,?)''', (cname4,po4,mname4,date1,cusname4,mobno4,tran_type4,tran_id4,mcost4))
        conn.commit()
    
def show_machine_collection():
    m1 = cur.execute('''SELECT *FROM collection''')
    st.table(m1.fetchall())
    
def add_vendor(vname,address,gstno):
    try:
        cur.execute('''INSERT INTO vendor_info(v_name,v_add,gstno) VALUES(?,?,?)''',( vname,address,gstno))
        conn.commit()
        
    except sqlite3.IntegrityError:
                st.info("Vendor Already Exist")
                return 0
def show_vendor():
    
    m=cur.execute('''SELECT *FROM vendor_info''')
    st.table(m.fetchall())
    
def add_material(vendorname,co_name,machinename,materialname,mcost,qn,mgst,mtotal) :
    try:
        
        cur.execute('''INSERT INTO materialinfo(v_name,co_name,mname,mat_name,cost,m_quantity,m_gst,m_total) VALUES(?,?,?,?,?,?,?,?)''',(vendorname,co_name,machinename,materialname,mcost,qn,mgst,mtotal))
        conn.commit()
    except sqlite3.IntegrityError:
                st.info("Material Already Exist")
                return 0

def show_material():
    
    m=cur.execute('''SELECT *FROM materialinfo''')
    st.table(m.fetchall())





def company_info_entry():
    m2=cur.execute("SELECT company_name FROM  company_info")
    pairs = [x[0] for x in m2.fetchall()]
    return pairs

def machine_info_entry():
    m2=cur.execute("SELECT machine_name FROM  machinetable")
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def purchase_no_entry(company):
    m2=cur.execute('SELECT po_no FROM purchaseorder WHERE pcompany_name="{}"'.format(company))
    pairs = [x[0] for x in m2.fetchall()]
    return pairs

def purchase_nmachine_entry(po):
    m2=cur.execute('SELECT pmachine_name FROM purchaseorder WHERE po_no="{}"'.format(po))
    pairs = [x[0] for x in m2.fetchall()]
    return pairs

def machineinfotable_entry(name1):
    m2=cur.execute('SELECT mch_name FROM  machineinfotable WHERE c_name="{}"'.format(name1))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machineinfotable_entry_comp():
    m2=cur.execute('SELECT c_name FROM  machineinfotable')
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machine_estimate_entry():
    m2=cur.execute('SELECT cname FROM  machine_estimate')
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def machine_estimate_entry2(com_name):
    m2=cur.execute('SELECT machine_name FROM  machine_estimate WHERE cname="{}"'.format(com_name))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def vendor_info_entry():
    m2=cur.execute("SELECT v_name FROM  vendor_info")
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def collection_comp_entry():
    m2=cur.execute('SELECT company_name FROM  collection')
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def collection_entry(com_name):
    m2=cur.execute('SELECT machine_name1 FROM  collection WHERE company_name="{}"'.format(com_name))
# data=m2.fetchall()
# st.write(data)
    pairs = [x[0] for x in m2.fetchall()]
    return pairs
def select_po(cname1):
     m2=cur.execute('SELECT po_no FROM  purchaseorder WHERE pcompany_name="{}"'.format(cname1))
# data=m2.fetchall()
# st.write(data)
     pairs = [x[0] for x in m2.fetchall()]
     return pairs
def select_po_machine(po):
     m2=cur.execute('SELECT pmachine_name FROM  purchaseorder WHERE po_no="{}"'.format(po))
# data=m2.fetchall()
# st.write(data)
     pairs = [x[0] for x in m2.fetchall()]
     return pairs
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
    base_cost=float(cost1)*float(quantity1)
    gst_cost= float(base_cost)*(float(gst1)/100)
    
    total1=float(base_cost) + float(gst_cost)
    return float(total1)

def Bills():
     try:
        cur.execute('SELECT * FROM materialinfo')
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_total) FROM materialinfo')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def machinebill():
     try:
        cur.execute('SELECT * FROM purchaseorder')
        data = cur.fetchall()
        cur.execute('SELECT SUM(pmcost) FROM purchaseorder')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def machinebill_by_company():
     try:
        cur.execute('SELECT * FROM machine_estimate')
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_cost) FROM machine_estimate')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def machinebill_by_installments():
     try:
        cur.execute('SELECT * FROM collection')
        data = cur.fetchall()
        cur.execute('SELECT SUM(cmachine_cost) FROM collection')
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def profit_loss(cname2):
    try:
        cur.execute('SELECT SUM(memcost) FROM machine_estimate_by_sfood WHERE  mecompany_name="{}"'.format(cname2))
        data = cur.fetchall()
        cur.execute('SELECT SUM(m_total) FROM materialinfo WHERE co_name="{}"'.format(cname2))
        data1 = cur.fetchall()
        return data,data1
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def outstanding_bills(cname1):
     try:
        cur.execute('SELECT SUM(pmcost) FROM purchaseorder WHERE pcompany_name="{}"'.format(cname1))
        data = cur.fetchall()
        cur.execute('SELECT SUM(cmachine_cost) FROM collection WHERE ccompany_name="{}"'.format(cname1))
        data1 = cur.fetchall()
        return data,data1
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def vendor_wise_bill(vname):
    
      try:
        cur.execute('SELECT * FROM materialinfo WHERE v_name="{}"'.format(vname))
        data = cur.fetchall()
        
        cur.execute('SELECT SUM(m_total) FROM materialinfo WHERE v_name="{}"'.format(vname))
        data1 = cur.fetchall()
        return data,data1
      except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
    
    
def column_wise_bill(cname):
    
      try:
        cur.execute('SELECT * FROM materialinfo WHERE co_name="{}"'.format(cname))
        data = cur.fetchall()
        
        cur.execute('SELECT SUM(m_total) FROM materialinfo WHERE co_name="{}"'.format(cname))
        data1 = cur.fetchall()
        return data,data1
      except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
def by_vendor_wise():
     try:
        m2=cur.execute('SELECT v_name FROM  vendor_info')
        pairs = [x[0] for x in m2.fetchall()]
        return pairs
        
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0

def by_company_wise():
     try:
        m2=cur.execute('SELECT company_name FROM  company_info')
        pairs = [x[0] for x in m2.fetchall()]
        return pairs
        
     except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
    
def drop_tables():
    try:
        cur.execute('''DROP TABLE machineinfotable''')
        conn.commit()
        cur.execute('''DROP TABLE companyinfo''')
        conn.commit()
        cur.execute('''DROP TABLE vendor_info''')
        conn.commit()
        cur.execute('''DROP TABLE materialinfo''')
        conn.commit()
        
    except sqlite3.IntegrityError:
        st.write(" User Not Found")
        return 0
# -----------------------------------------------------------------------------------------------
st.title("Management ")

create_table()
select1=["Home","COMPANY","VENDOR"]
select2=st.sidebar.selectbox("Choose",select1)
if select2=="HOME":
    st.write("WELCOME")
elif select2=="COMPANY":
    menu = ["Add Company","Add Machine","Purchase Order","Machine Estimation","Add Collection","Show Details","Search","Company Payments"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    if choice == "Add Company":
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
            
         
    elif choice == "Add Machine":
        machine=st.text_input("MACHINE NAME")
        submit1 = st.button(label='Submit')
        if submit1:
            s1 =add_machine(machine)
            print(s1)
            if s1 == 0:
                st.error("Not Added")
            else:
                st.success("MACHINE Successfully added")
            
       
    elif choice == "Purchase Order":  
       
            company_list=company_info_entry()
            cname2=st.selectbox('Select company', company_list)
            purchase_no=st.text_input("Purchase Order No.")
            machine_list=machine_info_entry()
            mname2=st.selectbox('Select machine', machine_list)
            machine_qty=st.text_input("Machine Quantity")
            machine_cost=st.text_input("Cost")
            submit2 = st.button(label='Save')
            if submit2:
                s2=add_purchase_order_info(cname2,purchase_no,mname2,machine_qty,machine_cost)
                if s2==0:
                    st.error("Not Added")      
                else :
                   st.success("Successfully added")
    
    elif choice == "Machine Estimation":
    
            company_list=company_info_entry()
            cname2=st.selectbox('Select company', company_list)
            po_list=purchase_no_entry(cname2)
            purchase_no=st.selectbox('Select po', po_list)
            machine_list=machine_info_entry()
            mname2=st.selectbox('Select machine', machine_list)
            machine_qty=st.text_input("Machine Quantity")
            machine_cost=st.text_input("Cost")
            submit2 = st.button(label='Save')
            if submit2:
                s3=add_machine_estimate(cname2,purchase_no,mname2,machine_qty,machine_cost)
                if s3==0:
                    st.error("Not Added")      
                else :
                   st.success("Successfully added")
    
    elif choice == "Add Collection":
    
            data = company_info_entry()
            cname3 = st.selectbox('Select company', data)
            po1=select_po(cname3)
            po2=st.selectbox("Select po",po1)
            data1 = select_po_machine(po2)
            mname3 = st.selectbox('Select machine', data1)
    
            staffname = st.text_input("Staff name")
            mobno = st.text_input("Mobile Number")
            t_type = st.text_input("Transaction Type")
            t_id= st.text_input("Transaction_id")
            t_cost = st.text_input("Total cost")
            submit2 = st.button('Save')
            if submit2:
                s2 = add_collection(cname3,po2, mname3,staffname,mobno,t_type,t_id,t_cost)
                if s2 == 0:
                    st.error("Not Added")
                else:
                    st.success("Successfully added")
    
    elif choice== "Show Details":
           st.write("Company Information")
           show_company()
           st.write("Machine Information")
           show_machine()
           st.write("Purchase Order")
           show_purchase_order_info()
           st.write("Machine Estimation")
           show_machine_estimate()
           st.write("Collection Information")
           show_machine_collection()
           st.write("Vendor Information")
           show_vendor()
           st.write("Material Information")
           show_material()
    

    elif choice=="Company Payments":
            bill1,total1=machinebill()
            st.table(bill1)
            st.write("TOTAL MACHINE COST")
            st.write(total1[0][0])
            bill2,total2=machinebill_by_installments()
            st.table(bill2)
            st.write("TOTAL PAID MACHINE COST")
            st.write(total2[0][0])
            list2=by_company_wise()
            op2=st.selectbox("Company", list2)
            if op2:
                bill3,total3=outstanding_bills(op2)
                st.write("TOTAL COST")
                st.write(bill3[0][0])
                st.write("TOTAL PAID COST")
                st.write(total3[0][0])
                st.write("OUTSTANDING")
                amount=bill3[0][0]-total3[0][0]
                st.write(amount)
                st.write("TOTAL Material Cost")
                result1,amount2=column_wise_bill(op2)
                st.write(amount2[0][0])
        
                res1,res2=profit_loss(op2)
                profit=res1[0][0]-res2[0][0]
                st.write("profit")
                st.write(profit)
elif select2=="VENDOR":
    menu = ["Add Vendor","Add Material","Search","Vendor Bills"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add Vendor":
             with st.form(key='Machine_form'):
                # vdata=vendor_info_entry()
                 name3 = st.text_input('enter vendor')
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
            data2=vendor_info_entry()
            vendorn=st.selectbox('Select Vendor', data2)
            data3=company_info_entry()
            coname=st.selectbox('Select company', data3)
            data4=select_po(coname)
            po4=st.selectbox('Select po', data4)
            mdata4=select_po_machine(po4)
            machine4=st.selectbox('Select machine', mdata4)
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
                    s4=add_material(vendorn,coname,machine4,mname2,cost2,quantity,gst2,amount) 
                    if s4==0:
                        st.error("Not Added")      
                    else :
                       st.success("Successfully added")
                      

    elif choice=="Search":
                name2 = st.text_input("Enter Company Name to search" )
                searched_data1=search_by_cname(name2)
                searched_data2=search_by_mcname(name2)
                st.table(searched_data1)
                st.table(searched_data2)
        
    elif choice=="Vendor Bills":
            bill,total=Bills()
            st.table(bill)
            st.write(total[0][0])
            
            option=st.radio("SELECT OPTION",["BY VENDOR WISE","BY COMPANY WISE"])
            if option=="BY VENDOR WISE":
                list1=by_vendor_wise()
                op1=st.selectbox("VENDOR", list1)
                if op1:
                    result,amount1=vendor_wise_bill(op1)
                    st.table(result)
                    st.write("TOTAL AMOUNT ",amount1[0][0])
            elif option=="BY COMPANY WISE": 
                list2=by_company_wise()
                op2=st.selectbox("Company", list2)
                if op2:
                    result1,amount2=column_wise_bill(op2)
                    st.table(result1)
                    st.write("TOTAL AMOUNT ",amount2[0][0])
        
        
