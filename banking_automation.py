
from tkinter import *
from tkinter.ttk import Combobox,Treeview,Style,Scrollbar
from PIL import Image,ImageTk
from datetime import datetime
import sqlite3
from tkinter import messagebox

con=sqlite3.connect(database="bank.sqlite")
cur=con.cursor()
table1="create table accounts(account_no integer primary key autoincrement,account_name text,account_pass text,account_email text,account_mob text,account_type text,account_bal float,account_opendate text)"
table2="create table txn(txn_account_no int,txn_amt float,txn_update_bal float,txn_date text,txn_type text)"
try:
    cur.execute(table1)
    cur.execute(table2)
    print("Tables created")
except:
    print("something went wrong in db,might be table(s) already exist")
    
con.commit()
con.close()

win=Tk()
win.state("zoomed")
win.configure(bg="orange")

lbl_title=Label(win,text="Banking Automation",bg="orange",font=('Arial',55,'bold','underline'))
lbl_title.place(relx=.25,rely=.01)

img=Image.open("logo1.png").resize((220,110))
imgtk=ImageTk.PhotoImage(img,master=win)

lbl_logo=Label(win,image=imgtk)
lbl_logo.place(x=0,y=0)


def login_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.9)

    def newuser():
        frm.destroy()
        newuser_screen()
    
    def forgot():
        frm.destroy()
        forgotpass_screen()
        
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
        
    def login_db():
        acn=e_acn.get()
        pwd=e_pass.get()
        if(acn=="" or pwd==""):
            messagebox.showwarning("Login","Please fill both fields")
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=? and account_pass=?",(acn,pwd))
            global tup
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showerror("login","Invalid ACN or pass")
            else:
                frm.destroy()
                welcome_screen()

    lbl_acn=Label(frm,text="Account No",bg='powder blue',font=('Arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.42,rely=.1)
    e_acn.focus()
    
    lbl_pass=Label(frm,text="Password",bg='powder blue',font=('Arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.22)
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.42,rely=.22)
    
    btn_login=Button(frm,text="login",command=login_db,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_login.place(relx=.42,rely=.34)
    
    btn_reset=Button(frm,text="reset",command=reset,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_reset.place(relx=.5,rely=.34)
    
    btn_fp=Button(frm,text="forgot password",command=forgot,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_fp.place(relx=.41,rely=.45)
    
    btn_new=Button(frm,text="open new account",command=newuser,width=17,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_new.place(relx=.3925,rely=.56)
    
    
def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.9)
    
    def back():
        frm.destroy()
        login_screen()
        
    def reset():
        e_name.delete(0,"end")
        e_pass.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_name.focus()
        
    def openacn_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        acn_type=cb_type.get()
        
        if(name=="" or pwd=="" or email=="" or mob==""):
            messagebox.showwarning("Login","Please fill all the fields")
            return
        else:
            pass
        if(acn_type=="Saving"):
            bal=1000
        else:
            bal=10000
        opendate=str(datetime.now().date())
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into accounts(account_name,account_pass,account_email,account_mob,account_type,account_bal,account_opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,acn_type,bal,opendate))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(account_no) from accounts")
        tup=cur.fetchone()
        con.close()
        messagebox.showinfo("Success",f"Account Opened with ACN :{tup[0]}")
        frm.destroy()
        login_screen()
            
        
    btn_back=Button(frm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_back.place(relx=.0,rely=0)
    
    
    lbl_name=Label(frm,text="Name",bg='powder blue',font=('Arial',20,'bold'))
    lbl_name.place(relx=.299,rely=.1)
    
    
    e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_name.place(relx=.42,rely=.1)
    e_name.focus()
    
    lbl_pass=Label(frm,text="Password",bg='powder blue',font=('Arial',20,'bold'))
    lbl_pass.place(relx=.299,rely=.22)
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.42,rely=.22)
    
    lbl_email=Label(frm,text="Email",bg='powder blue',font=('Arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.33)
    
    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.42,rely=.33)
    
    lbl_mob=Label(frm,text="Mob",bg='powder blue',font=('Arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.44)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.42,rely=.44)
    
    lbl_type=Label(frm,text="ACN Type",bg='powder blue',font=('Arial',20,'bold'))
    lbl_type.place(relx=.3,rely=.55)
    
    cb_type=Combobox(frm,values=['Saving','Current'],font=('Arial',20,'bold'))
    cb_type.current(0)
    cb_type.place(relx=.42,rely=.55)
    
    btn_open=Button(frm,text="open",command=openacn_db,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_open.place(relx=.42,rely=.66)
    
    btn_reset=Button(frm,text="reset",command=reset,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_reset.place(relx=.5,rely=.66)
    
    

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.9)
    
    def back():
        frm.destroy()
        login_screen()
        
    def reset():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        
    def get_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        
        if(acn=="" or email=="" or mob==""):
            messagebox.showwarning("Validation","Please fill all fields")
            return
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_pass from accounts where account_no=? and account_email=? and account_mob=?",(acn,email,mob))
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showerror("Forgot","Invalid details")
            else:
                messagebox.showinfo("Forgot",f"Your password is:{tup[0]}")
                frm.destroy()
                login_screen()
            
    btn_back=Button(frm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_back.place(relx=.0,rely=0)
    
    
    lbl_acn=Label(frm,text="ACN",bg='powder blue',font=('Arial',20,'bold'))
    lbl_acn.place(relx=.299,rely=.1)
    
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.42,rely=.1)
    e_acn.focus()
    
    
    lbl_email=Label(frm,text="Email",bg='powder blue',font=('Arial',20,'bold'))
    lbl_email.place(relx=.299,rely=.22)
    
    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.42,rely=.22)
    
    lbl_mob=Label(frm,text="Mob",bg='powder blue',font=('Arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.33)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.42,rely=.33)
    
    
    btn_get=Button(frm,text="open",command=get_db,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_get.place(relx=.42,rely=.44)
    
    btn_reset=Button(frm,text="reset",command=reset,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_reset.place(relx=.5,rely=.44)
    
    
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.9)
    
    def logout():
        frm.destroy()
        login_screen()
        
    def checkbal():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=3,highlightcolor='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.7)
        lbl_page.configure(text="This is Check bal Page")
        def back():
            ifrm.destroy()
            welcome_screen()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select account_name,account_bal,account_opendate from accounts where account_no=?",(tup[0],))
        row=cur.fetchone()
        
    
    
        lbl_acn=Label(ifrm,text=f"Account Number\t{tup[0]}",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_acn.place(relx=.3,rely=.1)
    
        lbl_name=Label(ifrm,text=f"Holder Name\t{row[0]}",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_name.place(relx=.3,rely=.3)
    
        lbl_bal=Label(ifrm,text=f"Available Bal\t{row[1]}",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_bal.place(relx=.3,rely=.5)
        
        lbl_date=Label(ifrm,text=f"ACN open date\t{row[2]}",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_date.place(relx=.3,rely=.7)
        
        btn_back=Button(ifrm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_back.place(relx=.43,rely=.82)
        
    def deposit():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=3,highlightcolor='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.7)
        lbl_page.configure(text="This is Deposit Page")
        
        def back():
            ifrm.destroy()
            welcome_screen()
        
        def deposit_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="CR."
            dt=str(datetime.now())
            
            if(amt<0):
                messagebox.showerror("Deposit","-ve amount can not be deposited")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(acn,))
                bal=cur.fetchone()[0]
                con.close()
                
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
                cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,acn))
                con.commit()
                con.close()
                
                messagebox.showinfo("Deposited","Amount deposited")
                ifrm.destroy()
                welcome_screen()
                
                
        
        lbl_amt=Label(ifrm,text="Enter Amount",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_amt.place(relx=.2,rely=.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
        e_amt.focus()
    
    
        btn_dep=Button(frm,text="deposit",command=deposit_db,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_dep.place(relx=.55,rely=.4)
        
        btn_back=Button(ifrm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_back.place(relx=.36,rely=.357)
        
    def withdraw():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=3,highlightcolor='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.7)
        lbl_page.configure(text="This is Withdraw Page")
        
        def back():
            ifrm.destroy()
            welcome_screen()
            
        def withdraw_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="DB."
            dt=str(datetime.now())
            
            if(amt<0):
                messagebox.showerror("Withdraw","-ve amount can not be withdrawal")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(acn,))
                bal=cur.fetchone()[0]
                con.close()
                
                if(bal>=amt):
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
                    cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,acn))
                    con.commit()
                    con.close()
                    
                    messagebox.showinfo("withdraw","Amount Withdrawn")
                    ifrm.destroy()
                    welcome_screen()
                else:
                    messagebox.showwarning("withdraw","insufficient balance")

        
        lbl_amt=Label(ifrm,text="Enter Amount",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_amt.place(relx=.2,rely=.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
        e_amt.focus()
    
    
        btn_dep=Button(frm,text="withdraw",command=withdraw_db,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_dep.place(relx=.55,rely=.4)
        
        btn_back=Button(ifrm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_back.place(relx=.36,rely=.357)
        
    def transfer():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=3,highlightcolor='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.7)
        lbl_page.configure(text="This is Transfer Page")
        
        def back():
            ifrm.destroy()
            welcome_screen()
            
        def transfer_db():
            t_acn=e_to.get()
            amt=float(e_amt.get())
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=?",(t_acn,))
            row=cur.fetchone()
            con.close()
            
            if(amt<0):
                messagebox.showerror("Transfer","-ve ammount cannot be transfered")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(t_acn,))
                bal=cur.fetchone()[0]
                con.close()
            
                if(row==None):
                    messagebox.showerror("Transfer","To account doesn't exist")
                else:
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
                    bal=cur.fetchone()[0]
                    con.close()

                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("select account_bal from accounts where account_no=?",(t_acn,))
                    t_bal=cur.fetchone()[0]
                    con.close()


                    if(bal>=amt):
                        con=sqlite3.connect(database="bank.sqlite")
                        cur=con.cursor()
                        dt=str(datetime.now())
                        cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,tup[0]))
                        cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,t_acn))
                        cur.execute("insert into txn values(?,?,?,?,?)",(tup[0],amt,bal-amt,dt,"DB."))
                        cur.execute("insert into txn values(?,?,?,?,?)",(t_acn,amt,t_bal+amt,dt,"CR."))

                        con.commit()
                        con.close()
                        messagebox.showinfo("Transfer","Txn done")
                        ifrm.destroy()
                        welcome_screen()
                    else:
                        messagebox.showwarning("Transfer","insufficient bal")
                    
                
        
    
        lbl_to=Label(ifrm,text="Enter To ACN",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_to.place(relx=.2,rely=.2)
        
        e_to=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_to.place(relx=.45,rely=.2)
        e_to.focus()
        
        lbl_amt=Label(ifrm,text="Enter Amount",bg='white',font=('Arial',20,'bold'),fg="purple")
        lbl_amt.place(relx=.2,rely=.4)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.4)
    
    
        
        btn_transfer=Button(frm,text="transfer",command=transfer_db,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_transfer.place(relx=.55,rely=.6)
        
        btn_back=Button(ifrm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_back.place(relx=.36,rely=.645)
        
        
    def update():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=3,highlightcolor='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.7)
        lbl_page.configure(text="This is Update Profile Page")
        
        def back():
            ifrm.destroy()
            welcome_screen()
            
        def update_profile():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set account_name=?,account_pass=?,account_email=?,account_mob=? where account_no=?",(name,pwd,email,mob,tup[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Update","Profile updated")
            ifrm.destroy()
            welcome_screen()
            
            
            
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select * from accounts where account_no=?",(tup[0],))
        row=cur.fetchone()
        con.close()
        
        lbl_name=Label(ifrm,text="Name",bg='white',font=('Arial',15,'bold'),fg="purple")
        lbl_name.place(relx=.08,rely=.2)
        
        e_name=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_name.place(relx=.2,rely=.2)
        e_name.insert(0,row[1])
        e_name.focus()
        
        lbl_pass=Label(ifrm,text="Pass",bg='white',font=('Arial',15,'bold'),fg="purple")
        lbl_pass.place(relx=.51,rely=.2)
        
        e_pass=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_pass.place(relx=.6,rely=.2)
        e_pass.insert(0,row[2])
        
        lbl_email=Label(ifrm,text="Email",bg='white',font=('Arial',15,'bold'),fg="purple")
        lbl_email.place(relx=.08,rely=.4)
        
        e_email=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_email.place(relx=.2,rely=.4)
        e_email.insert(0,row[3])
        
        lbl_mob=Label(ifrm,text="Mob",bg='white',font=('Arial',15,'bold'),fg="purple")
        lbl_mob.place(relx=.51,rely=.4)
        
        e_mob=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_mob.place(relx=.6,rely=.4)
        e_mob.insert(0,row[4])
    
        btn_update=Button(frm,text="update",command=update_profile,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_update.place(relx=.55,rely=.6)
        
        btn_back=Button(ifrm,text="Back",command=back,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
        btn_back.place(relx=.36,rely=.645)
    
    def txn_history():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=3,highlightcolor='brown')
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.15,relwidth=.6,relheight=.7)
        lbl_page.configure(text="This is txn history Page")
        
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,relheight=1,relwidth=1)
        
        style=Style()
        style.configure("Treeview.Heading",font=('Arial',10,'bold'),foreground='purple')
        
        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(relx=.98,y=0,relheight=1)
        
        tv['column']=('Txn date','Txn amount','Txn type','Updated balance')
        
        tv.column('Txn date',width=150,anchor='c')
        tv.column('Txn amount',width=100,anchor='c')
        tv.column('Txn type',width=100,anchor='c')
        tv.column('Updated balance',width=100,anchor='c')
        
        tv.heading('Txn date',text='Txn date')
        tv.heading('Txn amount',text='Txn amount')
        tv.heading('Txn type',text='Txn type')
        tv.heading('Updated balance',text='Updated balance')
        
        tv['show']='headings'
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur=con.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txn where txn_account_no=?",(tup[0],))
        for row in cur:
            tv.insert("","end",values=(row[0],row[1],row[2],row[3]))
        
    btn_logout=Button(frm,text="logout",command=logout,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_logout.place(relx=.923,rely=0)
    
    lbl_wel=Label(frm,text=f"Welcome,{tup[1]}",bg='powder blue',font=('Arial',16,'bold'),fg="brown2")
    lbl_wel.place(relx=0,rely=0)
    
    lbl_page=Label(frm,text="This is Home Page",bg='powder blue',font=('Arial',30,'bold',"underline"),fg="green")
    lbl_page.place(relx=.35,rely=0)
    
    
    
    btn_checkbal=Button(frm,text="check balance",command=checkbal,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_checkbal.place(relx=.001,rely=.12)
    
    btn_deposit=Button(frm,text="deposit amt",command=deposit,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_deposit.place(relx=.001,rely=.24)
    
    btn_withdraw=Button(frm,text="withdraw amt",command=withdraw,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_withdraw.place(relx=.001,rely=.36)
    
    btn_transfer=Button(frm,text="transfer",command=transfer,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_transfer.place(relx=.001,rely=.48)
    
    btn_update=Button(frm,text="update profile",command=update,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_update.place(relx=.001,rely=.6)
    
    btn_txnhist=Button(frm,text="txn history",command=txn_history,width=12,font=('Arial',20,'bold'),bd=5,bg="light goldenrod yellow")
    btn_txnhist.place(relx=.001,rely=.72)
    
    
    
    
login_screen() 
win.mainloop()


# In[ ]:




