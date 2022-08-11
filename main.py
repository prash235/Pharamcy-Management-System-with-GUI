from tkinter import *
import time
import sqlite3
import random
import tempfile
import win32api
import win32print
from PIL import ImageTk, Image

f = ''
flag = ''
flags = ''

login = sqlite3.connect("admin.db")
l = login.cursor()

c = sqlite3.connect("medicine.db")
cur = c.cursor()

columns = ('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')


def open_win():
    global apt, flag
    flag = 'apt'
    apt = Tk()
    apt.title("Interface")
    apt.geometry('1600x1200')
    apt.configure(bg="#fff")
    bg = PhotoImage(file="ph.png")
    my_label = Label(apt, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    a = Label(apt, text="Welcome !",font=("comicsansms 30 bold"), bg='#47B5FF',fg='white')
    a.place(x=100, y=100)

    # Label(apt, text='*' * 80).grid(row=1, column=0, columnspan=3)
    # Label(apt, text='-' * 80).grid(row=3, column=0, columnspan=3)

    a1 = Label(apt, text="Stock Maintenance",font=("comicsansms 20 bold"), bg='green', fg='white')
    # a1.grid(row=2, column=0)
    a1.place(x=30, y=200)
    Button(apt, text='New V.C.',font=("comicsansms 16 bold"), width=20, bg='green', fg='white', command=val_cus).place(x=30, y=300)
    Button(apt, text='Add product to Stock',font=("comicsansms 16 bold"), bg='green', fg='white', width=20, command=stock).place(x=30, y=400)
    Button(apt, text='Delete product from Stock',font=("comicsansms 16 bold"), bg='green', fg='white', width=20, command=delete_stock).place(x=30, y=500)

    a2 = Label(apt, text="Access Database",font=("comicsansms 20 bold"), bg='blue', fg='white')
    a2.grid(row=2, column=1)
    a2.place(x=350,y=200)
    Button(apt, text='Modify',font=("comicsansms 16 bold"), width=20, bg='blue', fg='white', command=modify).place(x=350, y=500)
    Button(apt, text='Search',font=("comicsansms 16 bold"), width=20, bg='blue', fg='white', command=search).place(x=350, y=300)
    Button(apt, text='Expiry Check',font=("comicsansms 16 bold"), bg='blue', fg='white', width=20, command=exp_date).place(x=350, y=400)

    a3 = Label(apt, text="Handle Cash Flows",font=("comicsansms 20 bold"), bg='skyblue', fg='black')
    a3.grid(row=2, column=2)
    a3.place(x=650,y=200)
    Button(apt, text="Check Today's Revenue",font=("comicsansms 16 bold"), bg='skyblue', fg='black', width=20, command=show_rev).place(x=650, y=300)
    Button(apt, text='Billing',font=("comicsansms 16 bold"), width=20, bg='skyblue', fg='black', command=billing).place(x=650, y=400)
    Button(apt, text='Logout',font=("comicsansms 16 bold"), bg='red', fg='white', width=20, command=again).place(x=30, y=600)
    apt.mainloop()


def delete_stock():
    global cur, c, flag, lb1, d
    apt.destroy()
    flag = 'd'
    d = Tk()
    d.title("Delete a product from Stock")
    Label(d, text='Enter Product to delete:',font=("helvetica 12")).grid(row=0, column=0)
    Label(d, text='', width=30, bg='white').grid(row=0, column=1)
    Label(d, text='Product').grid(row=2, column=0)
    Label(d, text='Qty.  Exp.dt.     Cost                           ').grid(row=2, column=1)
    ren()
    b = Button(d, width=20, text='Delete',font=("helvetica 12") , bg='red', fg='black', command=delt).grid(row=0, column=3)
    b = Button(d, width=20, text='Main Menu',font=("helvetica 12"), bg='green', fg='white', command=main_menu).grid(row=5, column=3)
    d.mainloop()


def ren():
    global lb1, d, cur, c

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(d, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(d, width=30, yscrollcommand=vsb.set)
    vsb.grid(row=3, column=2, sticky=N + S)
    lb1.grid(row=3, column=0)
    lb2.grid(row=3, column=1)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx += 1
        s1 = [str(i[0]), str(i[1])]
        s2 = [str(i[3]), str(i[6]), str(i[4])]
        lb1.insert(cx, '. '.join(s1))
        lb2.insert(cx, '   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)


def sel_del(e):
    global lb1, d, cur, c, p, sl2
    p = lb1.curselection()
    print(p)
    x = 0
    sl2 = ''
    cur.execute("select * from med")
    for i in cur:
        print(x, p[0])
        if x == int(p[0]):
            sl2 = i[0]
            break
        x += 1
    c.commit()
    print(sl2)
    Label(d, text=' ', bg='white', width=20).grid(row=0, column=1)
    cur.execute('Select * from med')
    for i in cur:
        if i[0] == sl2:
            Label(d, text=i[0] + '. ' + i[1], bg='white').grid(row=0, column=1)
    c.commit()


def delt():
    global p, c, cur, d
    cur.execute("delete from med where sl_no=?", (sl2,))
    c.commit()
    ren()


def modify():
    global cur, c, accept, flag, att, up, n, name_, apt, st, col, col_n
    col = ('', '', 'type', 'qty_left', 'cost', 'purpose', 'expdt', 'loc', 'mfg')
    col_n = ('', '', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
    flag = 'st'
    name_ = ''
    apt.destroy()
    n = []
    cur.execute("select * from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    st = Tk()
    st.title('MODIFY')
    Label(st, text='-' * 48 + ' MODIFY DATABASE ' + '-' * 48).grid(row=0, column=0, columnspan=6)

    def onvsb(*args):
        name_.yview(*args)

    def onmousewheel():
        name_.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    vsb.grid(row=1, column=3, sticky=N + S)
    name_ = Listbox(st, width=43, yscrollcommand=vsb.set)
    cur.execute("select *from med")
    for i in cur:
        cx += 1
        name_.insert(cx, (str(i[0]) + '.  ' + str(i[1])))
        name_.grid(row=1, column=1, columnspan=2)
    c.commit()
    name_.bind('<MouseWheel>', onmousewheel)
    name_.bind('<<ListboxSelect>>', sel_mn)

    Label(st, text='Enter Medicine Name: ').grid(row=1, column=0)
    Label(st, text='Enter changed Value of: ').grid(row=2, column=0)
    att = Spinbox(st, values=col_n)
    att.grid(row=2, column=1)
    up = Entry(st)
    up.grid(row=2, column=2)
    Button(st, width=10, text='Submit', bg='green', fg='white', command=save_mod).grid(row=2, column=4)
    Button(st, width=10, text='Reset', bg='red', fg='white', command=res).grid(row=2, column=5)
    Button(st, width=10, text='Show data', bg='blue', fg='white', command=show_val).grid(row=1, column=4)
    Label(st, text='-' * 120).grid(row=3, column=0, columnspan=6)
    Button(st, width=10, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=5, column=5)
    st.mainloop()


def res():
    global st, up
    up = Entry(st)
    up.grid(row=2, column=2)
    Label(st, width=20, text='                         ').grid(row=5, column=i)


def sel_mn(e):
    global n, name_, name_mn, sl, c, cur
    name_mn = ''
    p = name_.curselection()
    print(p)
    x = 0
    sl = ''
    cur.execute("select * from med")
    for i in cur:
        print(x, p[0])
        if x == int(p[0]):
            sl = i[0]
            break
        x += 1
    c.commit()
    print(sl)
    name_nm = n[int(sl)]
    print(name_nm)


def show_val():
    global st, name_mn, att, cur, c, col, col_n, sl
    for i in range(3):
        Label(st, width=20, text='                         ').grid(row=5, column=i)
    cur.execute("select * from med")
    for i in cur:
        for j in range(9):
            if att.get() == col_n[j] and sl == i[0]:
                Label(st, text=str(i[0])).grid(row=5, column=0)
                Label(st, text=str(i[1])).grid(row=5, column=1)
                Label(st, text=str(i[j])).grid(row=5, column=2)
    c.commit()


def save_mod():  # save modified data
    global cur, c, att, name_mn, st, up, col_n, sl
    for i in range(9):
        if att.get() == col_n[i]:
            a = col[i]
    sql = "update med set '%s' = '%s' where sl_no = '%s'" % (a, up.get(), sl)
    cur.execute(sql)
    c.commit()
    Label(st, text='Updated!').grid(row=5, column=4)


def stock():
    global cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag = 'sto'
    accept = [''] * 10
    sto = Tk()

    sto.title('STOCK ENTRY')
    

    Label(sto, text='ENTER NEW PRODUCT DATA TO THE STOCK',font=("comicsansms 16")).grid(row=0, column=0, columnspan=2)
    Label(sto, text='-' * 50).grid(row=1, column=0, columnspan=2)
    for i in range(1, len(columns)):
        Label(sto, width=15, text=' ' * (14 - len(str(columns[i]))) + str(columns[i]) + ':',font=("comicsansms 12")).grid(row=i + 2, column=0, padx=5, pady=5)
        accept[i] = Entry(sto,font=("comicsansms 12"))
        accept[i].grid(row=i + 2, column=1)
    Button(sto, width=15, text='Submit',font=("comicsansms 12"), bg='blue', fg='white', command=submit).grid(row=12, column=1)
    Label(sto, text='-' * 165).grid(row=13, column=0, columnspan=7)
    Button(sto, width=15, text='Reset',font=("comicsansms 12"), bg='red', fg='white', command=reset).grid(row=12, column=0)
    Button(sto, width=15, text='Refresh stock',font=("comicsansms 12"), bg='skyblue', fg='black', command=ref).grid(row=12, column=4)
    for i in range(1, 6):

        Label(sto, text=columns[i]).grid(row=14, column=i - 1)
    Label(sto, text='Exp           Rack   Manufacturer                      ').grid(row=14, column=5)
    Button(sto, width=10, text='Main Menu',font=("comicsansms 12"), bg='green', fg='white', command=main_menu).grid(row=12, column=5)
    ref()
    sto.mainloop()


def ref():
    global sto, c, cur

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        lb3.ywiew = ('scroll', event.delta, 'units')
        lb4.ywiew = ('scroll', event.delta, 'units')
        lb5.ywiew = ('scroll', event.delta, 'units')
        lb6.ywiew = ('scroll', event.delta, 'units')

        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(sto, yscrollcommand=vsb.set)
    lb2 = Listbox(sto, yscrollcommand=vsb.set)
    lb3 = Listbox(sto, yscrollcommand=vsb.set, width=10)
    lb4 = Listbox(sto, yscrollcommand=vsb.set, width=7)
    lb5 = Listbox(sto, yscrollcommand=vsb.set, width=25)
    lb6 = Listbox(sto, yscrollcommand=vsb.set, width=37)
    vsb.grid(row=15, column=6, sticky=N + S)
    lb1.grid(row=15, column=0)
    lb2.grid(row=15, column=1)
    lb3.grid(row=15, column=2)
    lb4.grid(row=15, column=3)
    lb5.grid(row=15, column=4)
    lb6.grid(row=15, column=5)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    lb3.bind('<MouseWheel>', onmousewheel)
    lb4.bind('<MouseWheel>', onmousewheel)
    lb5.bind('<MouseWheel>', onmousewheel)
    lb6.bind('<MouseWheel>', onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx += 1
        seq = (str(i[0]), str(i[1]))
        lb1.insert(cx, '. '.join(seq))
        lb2.insert(cx, i[2])
        lb3.insert(cx, i[3])
        lb4.insert(cx, i[4])
        lb5.insert(cx, i[5])
        lb6.insert(cx, i[6] + '    ' + i[7] + '    ' + i[8])
    c.commit()


def reset():
    global sto, accept
    for i in range(1, len(columns)):
        Label(sto, width=15, text=' ' * (14 - len(str(columns[i]))) + str(columns[i]) + ':').grid(row=i + 2, column=0)
        accept[i] = Entry(sto)
        accept[i].grid(row=i + 2, column=1)


def submit():
    global accept, c, cur, columns, sto

    x = [''] * 10
    cur.execute("select * from med")
    for i in cur:
        y = int(i[0])
    for i in range(1, 9):
        x[i] = accept[i].get()
    sql = "insert into med values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
    y + 1, x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    cur.execute(sql)
    cur.execute("select * from med")
    c.commit()

    top = Tk()
    Label(top, width=20, text='Success!').pack()
    top.mainloop()
    main_menu()


def chk():
    global cur, c, accept, sto
    cur.execute("select * from med")
    for i in cur:
        if accept[6].get() == i[6] and i[1] == accept[1].get():
            sql = "update med set qty_left = '%s' where name = '%s'" % (
            str(int(i[3]) + int(accept[3].get())), accept[1].get())
            cur.execute(sql)
            c.commit()
            top = Tk()
            Label(top, width=20, text='Modified!').pack()
            top.mainloop()
            main_menu()
        else:
            submit()
    c.commit()


def exp_date():
    global exp, s, c, cur, flag, apt, flags
    apt.destroy()
    flag = 'exp'
    from datetime import date
    now = time.localtime()
    n = []
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    exp = Tk()
    exp.geometry('1000x667')
    exp.title('EXPIRY CHECK')

    bg = PhotoImage(file="med.png")
    my_label = Label(exp, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    Label(exp, text='Today : ' + str(now[2]) + '/' + str(now[1]) + '/' + str(now[0]),font=("comicsansms 20")).place(x=50,y=100)
    Label(exp, text='Selling Expired Medicines and Drugs is Illegal !',font=("comicsansms 20")).place(x=50, y=200)
    # Label(exp, text='-' * 80).grid(row=2, column=0, columnspan=3)
    s = Spinbox(exp, values=n,font=("comicsansms 20"))
    s.place(x=50, y=320)
    Button(exp, text='Check Expiry date',font=("comicsansms 12"), bg='red', fg='white', command=s_exp).place(x=50, y=420)
    # Label(exp, text='-' * 80).grid(row=4, column=0, columnspan=3)
    if flags == 'apt1':
        Button(exp, text='Main Menu', bg='green', fg='white', command=main_cus).place(x=250, y=620)
    else:
        Button(exp, width=20, text='Check Products expiring',font=("comicsansms 12"), bg='red', fg='white', command=exp_dt).place(x=50, y=520)
        Button(exp,width=15, text='Main Menu',font=("comicsansms 12"), bg='green', fg='white', command=main_menu).place(x=400, y=520)
    exp.mainloop()


def s_exp():
    global c, cur, s, exp, top
    from datetime import date
    now = time.localtime()
    d1 = date(now[0], now[1], now[2])
    cur.execute("select * from med")
    for i in cur:
        if (i[1] == s.get()):
            q = i[6]
            d2 = date(int('20' + q[8:10]), int(q[3:5]), int(q[0:2]))
            if d1 > d2:
                # Label(exp, text='EXPIRED! on ' + i[6],font=("helvetica 20")).place(x=400, y=320)
                top = Tk()
                Label(top, text='EXPIRED! on ' + i[6],font=("helvetica 20")).pack()
            else:
                Label(exp, text=i[6],font=("helvetica 20")).place(x=400, y=320)
    c.commit()


def exp_dt():
    global c, cur, exp, top
    x = 0
    z = 1
    from datetime import datetime, timedelta
    N = 7
    dt = datetime.now() + timedelta(days=N)
    d = str(dt)
    from datetime import date
    now = time.localtime()
    d1 = date(now[0], now[1], now[2])
    d3 = date(int(d[0:4]), int(d[5:7]), int(d[8:10]))
    # Label(exp, text='S.No' + '   ' + 'Name' + '     Qty.    ' + 'Exp_date').grid(row=6, column=0, columnspan=2)
    cur.execute("select * from med")
    for i in cur:
        s = i[6]
        d2 = date(int('20' + s[8:10]), int(s[3:5]), int(s[0:2]))

        if d1 < d2 < d3:
            Label(exp, text=str(z) + '.      ' + str(i[1]) + '    ' + str(i[3]) + '    ' + str(i[6])).grid(row=x + 7,
                                                                                                           column=0,
                                                                                                           columnspan=2)
            x += 1
            z += 1
        elif d1 > d2:
            top = Tk()
            Label(top, width=20, text=str(i[1]) + ' is EXPIRED!',font=("helvetica 16")).pack()
    c.commit()


def billing():
    global c, cur, apt, flag, t, name, name1, add, st, names, qty, sl, qtys, vc_id, n, namee, lb1
    t = 0
    vc_id = ''
    names = []
    qty = []
    sl = []
    n = []
    qtys = [''] * 10
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    if flag == 'st':
        st.destroy()
    else:
        apt.destroy()
    flag = 'st'
    st = Tk()
    st.title('BILLING SYSTEM')
    st.geometry('1000x600')

    # bg = PhotoImage(file="bill.png")
    # my_label = Label(st, image=bg)
    # my_label.place(x=0, y=0, relwidth=1, relheight=1)
    Label(st, text='BILLING SYSTEM',font=("helvetica 22")).grid(row=0, column=0, columnspan=7)
    Label(st, text='Enter Name: ',font=("helvetica 16")).grid(row=1, column=0)
    name1 = Entry(st,font=("helvetica 16"))
    name1.grid(row=1, column=1)
    Label(st, text='Enter Address: ',font=("helvetica 16")).grid(row=2, column=0)
    add = Entry(st,font=("helvetica 16"))
    add.grid(row=2, column=1)
    Label(st, text="Value Id (if available)",font=("helvetica 16")).grid(row=3, column=0)
    vc_id = Entry(st,font=("helvetica 16"))
    vc_id.grid(row=3, column=1)
    Button(st, text='Check V.C.',font=("helvetica 12"), bg='green', fg='white', command=blue).grid(row=5, column=0)
    Label(st, text='-' * 115).grid(row=6, column=0, columnspan=7)
    Label(st, text='SELECT PRODUCT', width=25, relief='ridge').grid(row=7, column=0)
    Label(st, text=' RACK  QTY LEFT     COST          ', width=25, relief='ridge').grid(row=7, column=1)
    Button(st, text='Add to bill',width=15,font=("helvetica 12"), bg='blue', fg='white', command=append2bill).grid(row=8, column=18)
    Label(st, text='QUANTITY', width=20, relief='ridge').grid(row=7, column=5)
    qtys = Entry(st,font=("helvetica 12"))
    qtys.grid(row=8, column=5)
    refresh()
    Button(st, width=15, text='Main Menu',font=("helvetica 12"), bg='green', fg='white', command=main_menu).grid(row=1, column=18)
    Button(st, width=15, text='Refresh Stock',font=("helvetica 12"), bg='skyblue', fg='black', command=refresh).grid(row=3, column=18)
    Button(st, width=15, text='Reset Bill', font=("helvetica 12"),bg='red', fg='white', command=billing).grid(row=5, column=18)
    Button(st, width=15, text='Print Bill',font=("helvetica 12"), bg='orange', fg='white', command=print_bill).grid(row=7, column=18)
    Button(st, width=15, text='Save Bill',font=("helvetica 12"), bg='blue', fg='white', command=make_bill).grid(row=9, column=18)

    st.mainloop()


def refresh():
    global cur, c, st, lb1, lb2, vsb

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(st, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(st, width=25, yscrollcommand=vsb.set)
    vsb.grid(row=8, column=2, sticky=N + S)
    lb1.grid(row=8, column=0)
    lb2.grid(row=8, column=1)
    lb1.bind('<MouseWheel>', onmousewheel)
    lb2.bind('<MouseWheel>', onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx += 1
        lb1.insert(cx, str(i[0]) + '. ' + str(i[1]))
        lb2.insert(cx, ' ' + str(i[7]) + '        ' + str(i[3]) + '             Rs ' + str(i[4]))
    c.commit()
    lb1.bind('<<ListboxSelect>>', select_mn)


def select_mn(e):
    global st, lb1, n, p, nm, sl1
    p = lb1.curselection()
    x = 0
    sl1 = ''
    from datetime import date
    now = time.localtime()
    d1 = date(now[0], now[1], now[2])
    cur.execute("select * from med")
    for i in cur:
        if x == int(p[0]):
            sl1 = int(i[0])
            break
        x += 1
    c.commit()
    print(sl1)
    nm = n[x]
    print(nm)


def append2bill():
    global st, names, nm, qty, sl, cur, c, sl1
    sl.append(sl1)
    names.append(nm)
    qty.append(qtys.get())
    print(qty)
    print(sl[len(sl) - 1], names[len(names) - 1], qty[len(qty) - 1])


def blue():
    global st, c, cur, named, addd, t, vc_id
    cur.execute("select * from cus")
    for i in cur:
        if vc_id.get() != '' and int(vc_id.get()) == i[2]:
            named = i[0]
            addd = i[1]
            Label(st, text=named, width=20).grid(row=1, column=1)
            Label(st, text=addd, width=20).grid(row=2, column=1)
            Label(st, text=i[2], width=20).grid(row=3, column=1)
            Label(st, text='Valued Customer!').grid(row=4, column=1)
            t = 1
            break
    c.commit()


def make_bill():
    global t, c, B, cur, st, names, qty, sl, named, addd, name1, add, det, vc_id
    price = [0.0] * 10
    q = 0
    det = ['', '', '', '', '', '', '', '']
    det[2] = str(sl)
    for i in range(len(sl)):
        print(sl[i], ' ', qty[i], ' ', names[i])
    for k in range(len(sl)):
        cur.execute("select * from med where sl_no=?", (sl[k],))
        for i in cur:
            price[k] = int(qty[k]) * float(i[4])
            print(qty[k], price[k])
            cur.execute("update med set qty_left=? where sl_no=?", (int(i[3]) - int(qty[k]), sl[k]))
        c.commit()
    det[5] = str(random.randint(100, 999))
    B = 'bill_' + str(det[5]) + '.txt'
    total = 0.00
    for i in range(10):
        if price[i] != '':
            total += price[i]  # totalling
    m = '\n\n\n'
    m += "===============================================\n"
    m += "                                  No :%s\n\n" % det[5]
    m += " COEP MEDICAL STORE COMPANY\n"
    m += " Wellesley Rd, Shivajinagar, Pune, Maharashtra 411005\n\n"
    m += "-----------------------------------------------\n"
    if t == 1:
        m += "Name: %s\n" % named
        m += "Address: %s\n" % addd
        det[0] = named
        det[1] = addd
        cur.execute('select * from cus')
        for i in cur:
            if i[0] == named:
                det[7] = i[2]
    else:
        m += "Name: %s\n" % name1.get()
        m += "Address: %s\n" % add.get()
        det[0] = name1.get()
        det[1] = add.get()
    m += "-----------------------------------------------\n"
    m += "prescribed by DR ______________________________\n"
    m += "Product                      Qty.       Price\n"
    m += "-----------------------------------------------\n"
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1 = ' '
            s1 = (names[i]) + (s1 * (27 - len(names[i]))) + s1 * (3 - len(qty[i])) + qty[i] + s1 * (
                        15 - len(str(price[i]))) + str(price[i]) + '\n'
            m += s1
    m += "\n-----------------------------------------------\n"
    if t == 1:
        ntotal = total * 0.8
        m += 'Total' + (' ' * 25) + (' ' * (15 - len(str(total)))) + str(total) + '\n'
        m += "Valued customer Discount" + (' ' * (20 - len(str(total - ntotal)))) + '-' + str(total - ntotal) + '\n'
        m += "-----------------------------------------------\n"
        m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(ntotal)))) + 'Rs ' + str(ntotal) + '\n'
        det[3] = str(ntotal)
    else:
        m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(total)))) + 'Rs ' + str(total) + '\n'
        det[3] = str(total)

    m += "-----------------------------------------------\n\n"
    m += "Dealer 's signature:___________________________\n"
    m += "===============================================\n"
    print(m)
    p = time.localtime()
    det[4] = str(p[2]) + '/' + str(p[1]) + '/' + str(p[0])
    det[6] = m
    bill = open(B, 'w')
    bill.write(m)
    bill.close()
    cb = ('cus_name', 'cus_add', 'items', 'Total_cost', 'bill_dt', 'bill_no', 'bill', 'val_id')
    cur.execute('insert into bills values(?,?,?,?,?,?,?,?)',
                (det[0], det[1], det[2], det[3], det[4], det[5], det[6], det[7]))
    c.commit()


def print_bill():
    win32api.ShellExecute(0, "print", B, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)


def show_rev():
    global c, cur, flag, rev
    apt.destroy()
    cb = ('cus_name', 'cus_add', 'items', 'Total_cost', 'bill_dt', 'bill_no', 'bill', 'val_id')
    flag = 'rev'
    rev = Tk()
    total = 0.0
    today = str(time.localtime()[2]) + '/' + str(time.localtime()[1]) + '/' + str(time.localtime()[0])
    Label(rev, text='Today: ' + today).grid(row=0, column=0)
    cur.execute('select * from bills')
    for i in cur:
        if i[4] == today:
            total += float(i[3])
    print(total)
    Label(rev, width=22, text='Total revenue: Rs ' + str(total), bg='blue', fg='white').grid(row=1, column=0)
    cx = 0
    vsb = Scrollbar(orient='vertical')
    lb1 = Listbox(rev, width=25, yscrollcommand=vsb.set)
    vsb.grid(row=2, column=1, sticky=N + S)
    lb1.grid(row=2, column=0)
    vsb.config(command=lb1.yview)
    cur.execute("select * from bills")
    for i in cur:
        if i[4] == today:
            cx += 1
            lb1.insert(cx, 'Bill No.: ' + str(i[5]) + '    : Rs ' + str(i[3]))
    c.commit()
    Button(rev, text='Main Menu', bg='green', fg='white', command=main_menu).grid(row=15, column=0)
    rev.mainloop()


def search():
    global c, cur, flag, st, mn, sym, flags
    flag = 'st'
    apt.destroy()
    cur.execute("Select * from med")
    symp = ['nil']
    med_name = ['nil']
    for i in cur:
        symp.append(i[5])
        med_name.append(i[1])
    st = Tk()
    st.title('SEARCH')
    st.geometry('1232x821')

    bg = PhotoImage(file="cust1.png")
    my_label = Label(st, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    Label(st, bg='green', fg='white', text=' SEARCH FOR MEDICINE ',font=("helvetica 40 bold")).place(x =20, y = 100)
    # Label(st, text='~' * 40).grid(row=1, column=0, columnspan=3)
    Label(st, text='Symptom Name',font=("helvetica 20")).place(x =50, y = 320)
    sym = Spinbox(st, values=symp,font=("helvetica 20"))
    sym.grid(row=3, column=1)
    sym.place(x=300, y=320)
    b = Button(st, width=15, text='Search',font=("helvetica 16"), bg='blue', fg='white', command=search_med)
    b.grid(row=3, column=2)
    b.place(x=50, y=420)
    # Label(st, text='-' * 70).grid(row=4, column=0, columnspan=3)
    if flags == 'apt1':
        Button(st, width=15, text='Main Menu',font=("helvetica 16"), bg='green', fg='white', command=main_cus).place(x=300, y=420)
    else:
        Button(st, width=15, text='Main Menu',font=("helvetica 16"), bg='green', fg='white', command=main_menu).place(x=300, y=420)
    st.mainloop()


def search_med():
    global c, cur, st, sym, columns
    cur.execute("select * from med")
    y = []
    x = 0
    for i in cur:
        if i[5] == sym.get():
            y.append(
                str(i[0]) + '. ' + str(i[1]) + '  Rs ' + str(i[4]) + '    Rack : ' + str(i[7]) + '    Mfg : ' + str(
                    i[8]))
            x = x + 1
    top = Tk()
    for i in range(len(y)):
        Label(top, text=y[i]).grid(row=i, column=0)
    Button(top, text='OK', command=top.destroy).grid(row=5, column=0)
    c.commit()
    top.mainloop()


def val_cus():
    global val, flag, dbt, name_vc, add_vc, cur, c, vc_id
    apt.destroy()
    cur.execute("select * from cus")
    flag = 'val'
    val = Tk()
    # val.geometry(612x408)
    val.geometry('1920x1080')
    val.title('New V.C.')
    # val.configure(bg="#CDF0EA")


    bg = PhotoImage(file="add.png")
    my_label = Label(val, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(val, text="ENTER VALUED CUSTOMER DETAILS",font=("comicsansms 32"),  bg='green', fg='white',).place(x=50, y=100)
    # Label(val, text="-" * 60).grid(row=1, column=0, columnspan=3)
    cd = Label(val, text='Name', font=("Helvetica 23 bold"))
    cd.place(x=50, y=300)
    # Label(val, text="Name: ").grid(row=2, column=0)
    name_vc = Entry(val, width=25,font=("Helvetica 23 bold"))
    name_vc.place(x=300, y=300)
    de = Label(val, text="Address",font=("Helvetica 23 bold"))
    de.place(x=50, y=400)
    add_vc = Entry(val, width=25,font=("Helvetica 23 bold"))
    add_vc.place(x=300, y=400)
    ef = Label(val, text="Value Id: ",font=("Helvetica 23 bold"))
    ef.place(x=50, y=500)
    vc_id = Entry(val, width=25,font=("Helvetica 23 bold"))
    vc_id.place(x=300, y=500    )
    Button(val, text='Submit', font=("Helvetica 20 bold"), bg='blue', fg='white', command=val_get).place(x=100, y=600)
    Button(val, text='Main Menu', font=("Helvetica 20 bold"), bg='green', fg='white', command=main_menu).place(x=400, y=600)
    # Label(val, text='-' * 60).grid(row=6, column=0, columnspan=3)
    val.mainloop()


def val_get():
    global name_vc, add_vc, val, dbt, c, cur, apt, vc_id
    cur.execute("insert into cus values(?,?,?)", (name_vc.get(), add_vc.get(), vc_id.get()))
    l.execute("insert into log values(?,?)", (name_vc.get(), vc_id.get()))
    cur.execute("select * from cus")
    for i in cur:
        print(i[0], i[1], i[2])
    c.commit()
    login.commit()


def again():
    global un, pwd, flag, root, apt
    if flag == 'apt':
        apt.destroy()
    root = Tk()
    root.geometry('1920x1080')
    # root.wm_attributes('-transparentcolor','black')
    root.configure(bg="#fff")
    # root.resizable(False,False)
    # frame = Frame(root, width=350, height=350, bg="white")
    # frame.place(x=480,y=100)
    bg = PhotoImage(file="med1.png")
    # root.wm_grid(row=1,column=0)
    my_label = Label(root, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.title('Pharmacy Management System')
    Label(root, text='RPPOOP', font=("Helvetica 16 bold")).place(x =20, y = 10)
    Label(root, text="Pharmacy Management System", font=("Helvetica 40 bold")).place(x =20, y = 100)


    cd = Label(root, text='Username',font=("Helvetica 23 bold"))
    # cd.grid(row=4, column=1)
    cd.place(x=100, y=320)

    # un.place(x=50, y=100)
    un = Entry(root, width=30,font=("Helvetica 23 bold") )
    # un.grid(row=3, column=1)
    un.place(x=300, y=320)
    Label(root, text='Password',font=("Helvetica 23 bold")).place(x=100, y=420)
    pwd = Entry(root, width=30,font=("Helvetica 23 bold"))
    # pwd.grid(row=4, column=1)
    pwd.place(x=300, y=420)
    Button(root, width=8, bg='#34B3F1', fg='black', text='Enter',font=("Helvetica 20 bold"), command=check).place(x=250, y=520)
    Button(root, width=8, bg='#FD5D5D', fg='white', text='Close',font=("Helvetica 20 bold"),  command=root.destroy).place(x=500, y=520)
    root.mainloop()


def check():
    global un, pwd, login, l, root
    u = un.get()
    p = pwd.get()
    l.execute("select * from log")
    for i in l:
        if i[0] == u and i[1] == p and u == 'admin':
            root.destroy()
            open_win()
        elif i[0] == u and i[1] == p:
            root.destroy()
            open_cus()
    login.commit()


def main_menu():
    global sto, apt, flag, root, st, val, exp, st1, rev
    if flag == 'sto':
        sto.destroy()
    if flag == 'rev':
        rev.destroy()
    elif flag == 'st':
        st.destroy()
    elif flag == 'st1':
        st1.destroy()
    elif flag == 'val':
        val.destroy()
    elif flag == 'exp':
        exp.destroy()
    elif flag == 'd':
        d.destroy()
    open_win()


def main_cus():
    global st, flag, exp
    if flag == 'exp':
        exp.destroy()
    elif flag == 'st':
        st.destroy()
    open_cus()


def open_cus():
    global apt, flag, flags
    flags = 'apt1'
    apt = Tk()
    apt.title("Interface")
    apt.geometry('1332x850')

    bg = PhotoImage(file="search.png")
    my_label = Label(apt, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Label(apt, text='*' * 40).grid(row=1, column=0)
    Label(apt, text='WELCOME CUSTOMER SERVICES', font=("helvetica 20"), bg='green', fg='white').place(x=50,y=100)
    # Label(apt, text='-' * 40).grid(row=3, column=0)

    # Label(apt, text='-' * 40).grid(row=5, column=0)
    Button(apt, text='Search',font=("helvetica 16"), bg='blue', fg='white', width=15, command=search).place(x=100, y=200)
    Button(apt, text='Expiry Check',font=("helvetica 16"), bg='red', fg='white', width=15, command=exp_date).place(x=100, y=320)


    Button(apt, text='Logout',font=("helvetica 16"),bg='red', fg='white', command=again1).place(x=100,y=400)
    apt.mainloop()


def again1():
    global flags
    apt.destroy()
    flags = ''
    again()


again()

