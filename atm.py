import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class atm():
    def __init__(self,root):
        self.root = root
        self.root.title("Atm Machine Management")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Atm Machine Mangement System", bd=4, relief="groove", bg="light gray", font=("Arial",50,"bold"))
        title.pack(side="top", fill="x")

        # option frame

        optFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(160,200,250))
        optFrame.place(width=self.width/3 , height=self.height-180 , x=70 , y=100)

        atmLbl = tk.Label(optFrame, text="Atm_Card:", bg=self.clr(160,200,250), font=("Arial",15,"bold"))
        atmLbl.grid(row=0, column=0, padx=20, pady=30)
        self.atm = tk.Entry(optFrame, width=20, font=("Arial",15),bd=2)
        self.atm.grid(row=0, column=1, padx=10, pady=30)

        pwLbl = tk.Label(optFrame, text="Password:", bg=self.clr(160,200,250), font=("Arial",15,"bold"))
        pwLbl.grid(row=1, column=0, padx=20, pady=30)
        self.pw = tk.Entry(optFrame, width=20, font=("Arial",15), bd=2)
        self.pw.grid(row=1, column=1, padx=10, pady=30)

        inqLbl = tk.Label(optFrame, text="Balance Inquiry:", bg=self.clr(160,200,250), font=("Arial",12,"bold"))
        inqLbl.grid(row=2, column=0, padx=20, pady=30)
        inqBtn = tk.Button(optFrame,command=self.inqFun, text="Enter", width=10, bd=2, relief="raised", font=("Arial",15,"bold") )
        inqBtn.grid(row=2, column=1, padx=10, pady=30)

        wdLbl = tk.Label(optFrame, text="Cash Withdraw:", bg=self.clr(160,200,250), font=("Arial",12,"bold"))
        wdLbl.grid(row=3, column=0, padx=20, pady=30)
        wdBtn = tk.Button(optFrame,command=self.frameFun, text="Enter", width=10, bd=2, relief="raised", font=("Arial",15,"bold") )
        wdBtn.grid(row=3, column=1, padx=10, pady=30)


        transLbl = tk.Label(optFrame, text="Transaction:", bg=self.clr(160,200,250), font=("Arial",12,"bold"))
        transLbl.grid(row=4, column=0, padx=20, pady=30)
        transBtn = tk.Button(optFrame,command=self.transFrame, text="Enter", width=10, bd=2, relief="raised", font=("Arial",15,"bold") )
        transBtn.grid(row=4, column=1, padx=10, pady=30)



        # detail frame

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(240,180,150))
        self.detFrame.place(width=self.width/2, height= self.height-180, x=self.width/3+140, y=100)

        lbl = tk.Label(self.detFrame, text="Account Details", bd=3, font=("Arial",30,"bold"),bg=self.clr(230,210,155))
        lbl.pack(side="top", fill="x")
        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2-40, height=self.height-270, x=17, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("ac","name", "bal"))
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("ac", text="Account_No")
        self.table.heading("name", text="User_Name")
        self.table.heading("bal", text="Balance")
        self.table["show"] = "headings"
        
        self.table.pack(fill="both", expand=1)

    def inqFun(self):
        atm = self.atm.get()
        p = self.pw.get()

        if atm and p:
            atmNo = int(atm)
            pw = int(p)
            try:
                self.dbFun()
                self.cur.execute("select password from atm where atmNo=%s",atmNo)
                password = self.cur.fetchone()

                if password:
                    if pw==password[0]:
                        self.cur.execute("select accountNo, name, balance from atm where atmNo=%s", atmNo)
                        data = self.cur.fetchone()
                        self.tabFun()
                        self.table.delete(*self.table.get_children())
                        self.table.insert('',tk.END, values=data)

                        self.con.close()

                    else:
                        tk.messagebox.showerror("Error", "Invalid Password")
                else:
                    tk.messagebox.showerror("Error", "Invalid Atm_No")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def frameFun(self):
        self.amountFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(150,240,220))
        self.amountFrame.place(width=self.width/3, height=250, x=self.width/3+120, y=100)

        lbl = tk.Label(self.amountFrame, text="Amount:", bg=self.clr(150,240,220), font=("Arial",15,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=30)
        self.wdIn = tk.Entry(self.amountFrame, width=20,bd=2, font=("Arial",15))
        self.wdIn.grid(row=0, column=1, padx=10, pady=30)

        wdBtn = tk.Button(self.amountFrame,command=self.wdFun, text="Enter", bd=3, relief="raised", font=("Arial",20,"bold"),width=20)
        wdBtn.grid(row=1, column=0, padx=30, pady=40, columnspan=2)

    def wdFun(self):
        atm = self.atm.get()
        p = self.pw.get()

        if atm and p:
            atmNo = int(atm)
            pw = int(p)
            
            amount = int(self.wdIn.get())
            
            try:
                self.dbFun()
                self.cur.execute("select password from atm where atmNo=%s",atmNo)
                password = self.cur.fetchone()
                if password:
                    if pw==password[0]:
                        self.cur.execute("select accountNo,balance from atm where atmNo=%s",atmNo)
                        info = self.cur.fetchone()
                        if amount <=info[1]:
                            upd = info[1] - amount
                            self.cur.execute("update atm set balance=%s where atmNo=%s",(upd,atmNo))
                            self.con.commit()
                            self.desFrame()
                            tk.messagebox.showinfo("Success", "Operation was successful")
                            self.cur.execute("select accountNo,name,balance from atm where atmNo=%s",atmNo)
                            data = self.cur.fetchone()
                            self.tabFun()
                            self.table.delete(*self.table.get_children())
                            self.table.insert('', tk.END, values=data)
                            self.con.close()

                        else:
                            tk.messagebox.showerror("Error", f"You have insufficient balance in you account.{info[0]}")  
                            self.desFrame()  

                    else:
                        tk.messagebox.showerror("Error", "Invalid Password")
                        self.desFrame() 
                else:
                    tk.messagebox.showerror("Error", "Invalid Atm_No")
                    self.desFrame() 
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desFrame() 
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields")
            self.desFrame() 

    

    def desFrame(self):
        self.amountFrame.destroy()

    def transFrame(self):
        self.transFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(150,240,220))
        self.transFrame.place(width=self.width/3, height=350, x=self.width/3+120, y=100)

        amLbl = tk.Label(self.transFrame, text="Amount:", bg=self.clr(150,240,220), font=("Arial",15,"bold"))
        amLbl.grid(row=0, column=0, padx=20, pady=30)
        self.transIn = tk.Entry(self.transFrame, width=20,bd=2, font=("Arial",15))
        self.transIn.grid(row=0, column=1, padx=10, pady=30)

        user2Lbl = tk.Label(self.transFrame, text="Account_No:", bg=self.clr(150,240,220),font=("Arial",15,"bold"))
        user2Lbl.grid(row=1, column=0, padx=20, pady=30)
        self.user2In= tk.Entry(self.transFrame, width=20,bd=2, font=("Arial",15))
        self.user2In.grid(row=1, column=1, padx=10, pady=30)

        transBtn = tk.Button(self.transFrame,command=self.transFun, text="Enter", bd=3, relief="raised", font=("Arial",20,"bold"),width=20)
        transBtn.grid(row=2, column=0, padx=30, pady=40, columnspan=2)

    def desTrans(self):
        self.transFrame.destroy()

    def transFun(self):
        atm = self.atm.get()
        p = self.pw.get()


        if atm and p:
            atmNo = int(atm)
            pw = int(p)
            
            amount = int(self.transIn.get())
            user2 = int(self.user2In.get())

            try:
                self.dbFun()
                self.cur.execute("select password from atm where atmNo=%s",atmNo)
                password = self.cur.fetchone()
                if password:
                    if pw==password[0]:
                        self.cur.execute("select balance from atm where atmNo=%s",atmNo)
                        bal = self.cur.fetchone()
                        if amount <=bal[0]:
                            upd = bal[0] - amount
                            self.cur.execute("update atm set balance=%s where atmNo=%s",(upd,atmNo))
                            self.con.commit()

                            self.cur.execute("select balance from atm where accountNo=%s",user2)
                            user2Bal = self.cur.fetchone()
                            upd2 = user2Bal[0] + amount

                            self.cur.execute("update atm set balance=%s where accountNo=%s",(upd2,user2))
                            self.con.commit()
                            tk.messagebox.showinfo("Success","Operation was successful!")
                            self.desTrans()

                            self.cur.execute("select accountNo, name, balance from atm where atmNo=%s",atmNo)
                            data = self.cur.fetchone()
                            self.tabFun()
                            self.table.delete(*self.table.get_children())
                            self.table.insert('',tk.END, values=data)

                            self.con.close()
                            
                            
                        else:
                            tk.messagebox.showerror("Error", f"You have insufficient balance in you account") 
                            self.desTrans()
                    else:
                        tk.messagebox.showerror("Error", "Invalid Password")
                        self.desTrans()

                else:
                    tk.messagebox.showerror("Error", "Invalid Atm_No")
                    self.desTrans()

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desTrans()

        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields")
            self.desTrans()

    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"



root = tk.Tk()
obj = atm(root)
root.mainloop()