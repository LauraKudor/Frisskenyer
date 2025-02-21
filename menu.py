from tkinter import *
import tkinter as tk
from tkinter import messagebox
from klaszter import *


# INDITAS-----------------------------------------------------------------------------------------------------------
def ut():
    global aklaszter
    gykonyvtar = utvonal_bemenet.get()
    aklaszter=Klaszter(gykonyvtar)
    utvonal.destroy()
    utvonal_bemenet.destroy()
    ind.destroy()
    allapot=aklaszter.kl_ellenorzes()
    if allapot[0]=='Klaszter állapota megfelelő.':
        messagebox.showinfo(message=allapot[0])
    else:
        messagebox.showwarning(message='Klaszter állapota nem megfelelő.')
    menu_pack()

def enter(event):
    global enter_b
    if not enter_b:
        ut()
        enter_b=True

# menu megjelenitese------------------------------------------------------------------------------------------------
def menu_pack():
    klaframe.pack(pady=5)
    kla.pack(pady=10)
    gepframe.pack(pady=5)
    gepek.pack(pady=10)
    progframe.pack(pady=5)
    programok.pack(pady=10)
    uzenet=''
    allapot=aklaszter.kl_ellenorzes()
    for i in allapot:
        uzenet=uzenet+i+'\n'
    allapot_label.config(text=uzenet, font=('TkDefaultFont', 11),bg=hsz)
    allapot_label.pack(side=BOTTOM)

# menu eltuntetese--------------------------------------------------------------------------------------------------
def menu_hide():
    klaframe.pack_forget()
    gepframe.pack_forget()
    progframe.pack_forget()

# menu gomb-------------------------------------------------------------------------------------------------------------------
def menu():
    global v
    global vn
    global gepb
    global klab
    global progb
    if gepb:
        gepek_forget()
        gepb = False
    if klab:
        kla_forget() 
        klab = False
    if progb:
        program_forget()
        progb=False
    v[vn]()
    menu_pack()
    menu_button.pack_forget()


#MONITORING---------------------------------------------------------------------------------------------------------------------------
    
# monitoring gombok megjelenitese/eltuntetese
def kla_pack():
    kla1.pack(side=LEFT, padx=7)
    kla2.pack(side=LEFT, padx=7)
    kla3.pack(side=LEFT, padx=7)
    kla4.pack(side=LEFT, padx=7)
    kla5.pack(side=LEFT, padx=7)
def kla_forget():
    kla1.pack_forget()
    kla2.pack_forget()
    kla3.pack_forget()
    kla4.pack_forget()
    kla5.pack_forget()
    
def kladef():
    global klab
    global progb
    global gepb
    if gepb:
        gepek_forget()
        gepb = False
    if progb:
        program_forget()
        progb=False
    if klab:
        kla_forget()
        klab = False
    else:
        kla_pack()
        klab = True

#------------------------------------------------------------- 1 ----- szamitogep adatok ------------------
def kla1def(n):
    global vn
    global kla1_1
    global kla1_2
    global kla1_3
    kla1def_destroy()
    vn = 0
    valasz=vn+1
    kla1_list=aklaszter.monitoring(valasz,'')
    menu_hide()
    menu_button.pack(pady=20)
    sz_szam=len(aklaszter.szamitogepek)
    for i in range(3):
        frame = Frame(ablak,bg=hsz)
        frame.pack(side=TOP)
        kla1_1.append(frame)
        for j in range(3):
            if i*3+j<=sz_szam-9*n-1:
                frame = Frame(kla1_1[i], highlightbackground="black", highlightthickness=1,bg=hsz)
                frame.pack(side=LEFT, padx=8, pady=8)
                kla1_2.append(frame)
    for i in range(9):
        if 9*n+i+1<=sz_szam:
            p=kla1_list[2*i+18*n]
            m=kla1_list[2*i+1+18*n]
            label1 = Label(kla1_2[i], text=aklaszter.szamitogepek[i+9*n].get("nev"),bg=hsz)
            label2 = Label(kla1_2[i], text='Processzor: maximális - '+str(aklaszter.szamitogepek[i+9*n].get("processzorok"))+'\n szabad - '+str(aklaszter.szamitogepek[i+9*n].get("processzorok")-p))
            label3 = Label(kla1_2[i], text='Memória: maximális - '+str(aklaszter.szamitogepek[i+9*n].get("memoria"))+'\n szabad - '+str(aklaszter.szamitogepek[i+9*n].get("memoria")-m))
            label2.config(bg=hsz)
            label3.config(bg=hsz)
            kla1_3.append(label1)
            kla1_3.append(label2)
            kla1_3.append(label3)
            label1.pack(padx=5, pady=1)
            label2.pack(padx=5, pady=1)
            label3.pack(padx=5, pady=1)
    frame=Frame(ablak,bg=hsz)
    frame.pack()
    kla1_3.append(frame)
    if n>0:
        vissza=Button(frame,text='Vissza',command=lambda n=n: kla1def(n-1),bg='#fae1ca',activebackground='#fae1ca')
        vissza.pack(side=LEFT,padx=5)
        kla1_3.append(vissza)
    if sz_szam % 9 == 0:
        oldalak = sz_szam // 9
    else:
        oldalak = (sz_szam+9) // 9
    if oldalak>n+1:
        tovabb=Button(frame,text='Tovább',command=lambda n=n: kla1def(n+1),bg='#fae1ca',activebackground='#fae1ca')
        tovabb.pack(side=LEFT,padx=5)
        kla1_3.append(tovabb)

def kla1def_destroy():
    global kla1_1
    global kla1_2
    global kla1_3
    for i in range(len(kla1_3)):
        kla1_3[i].destroy()
    for i in range(len(kla1_2)):
        kla1_2[i].destroy()
    for i in range(len(kla1_1)):
        kla1_1[i].destroy()
    kla1_1 = []
    kla1_2 = []
    kla1_3 = []

#------------------------------------------------------------- 2 ---- programpeldanyok adatai ---------------------
def kla2def_1():
    global vn
    global kla2_1
    global kla2_2
    vn=1
    menu_hide()
    menu_button.pack(pady=20)
    kla2def_destroy()
    prog_szam=len(aklaszter.kl_adatok)
    if (prog_szam) % 5==0:
        sor=(prog_szam)//5
    else:
        sor=(prog_szam+5)//5
    for i in range(sor):
        frame=Frame(ablak,bg=hsz)
        frame.pack(side=TOP,pady=10)
        kla2_1.append(frame)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                k=i*5+j
                frame=Button(kla2_1[i],text=aklaszter.kl_adatok[k].get("nev"),command=lambda k=k: kla2def_2(k),bg=gsz1,activebackground=gsz1)
                frame.pack(side=LEFT,padx=5,pady=4)
                kla2_2.append(frame)

def kla2def_2(k):
    global kla2_3
    global kla2_4
    global kla2_5
    global vn
    valasz=vn+1
    kla2def_1_destroy()
    kla2_list_2=[]
    kla2_list=aklaszter.monitoring(valasz,aklaszter.kl_adatok[k].get("nev"))
    for program in kla2_list:
        if program.get('azonosito').startswith(aklaszter.kl_adatok[k].get('nev')):
            kla2_list_2.append(program)
    prog_szam=len(kla2_list_2)
    if prog_szam % 5 == 0:
        sor = prog_szam // 5
    else:
        sor = (prog_szam + 5) // 5
    for i in range(sor):
        frame = Frame(ablak,bg=hsz)
        frame.pack(side=TOP)
        kla2_3.append(frame)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                frame = Frame(kla2_3[i], highlightbackground="black", highlightthickness=1,bg=hsz)
                frame.pack(side=LEFT, padx=8, pady=8)
                kla2_4.append(frame)
    for i in range(prog_szam):
        label2 = Label(kla2_4[i], text=kla2_list_2[i].get('azonosito'),bg=hsz)
        label2.pack(padx=5, pady=1)
        kla2_5.append(label2)
        label3 = Label(kla2_4[i], text=kla2_list_2[i].get('statusz'),bg=hsz)
        label3.pack(padx=5, pady=1)
        kla2_5.append(label3)
    vissza=Button(ablak,text='Vissza',command=kla2def_1, font=('TkDefaultFont', 10),bg='#fae1ca',activebackground='#fae1ca')
    vissza.pack(pady=10)
    kla2_5.append(vissza)

def kla2def_destroy():
    kla2def_1_destroy()
    kla2def_2_destroy()

def kla2def_1_destroy():
    global kla2_1
    global kla2_2
    for i in range(len(kla2_1)):
        kla2_1[i].destroy()
    for i in range(len(kla2_2)):
        kla2_2[i].destroy()
    kla2_1 = []
    kla2_2 = []

def kla2def_2_destroy():
    global kla2_3
    global kla2_4
    global kla2_5
    for i in range(len(kla2_3)):
        kla2_3[i].destroy()
    for i in range(len(kla2_4)):
        kla2_4[i].destroy()
    for i in range(len(kla2_5)):
        kla2_5[i].destroy()
    kla2_3 = []
    kla2_4 = []
    kla2_5 = []

#------------------------------------------------------------- 3 ---- aktiv-inaktiv folyamatok ----------
def kla3def():
    global vn
    global kla3A
    global kla3I
    menu_hide()
    menu_button.pack(pady=20)
    vn = 2
    valasz=vn+1
    kla3_list=aklaszter.monitoring(valasz,'')
    kla3A = Label(ablak, text='AKTÍV folyamatok száma: '+str(kla3_list[0]), width=30, relief='sunken',
                  highlightbackground="black", highlightthickness=1, pady=4,bg=hsz)
    kla3I = Label(ablak, text='INAKTÍV folyamatok száma: '+str(kla3_list[1]), width=30, relief='sunken',
                  highlightbackground="black", highlightthickness=1, pady=4,bg=hsz)
    
    kla3A.pack(pady=4, padx=5)
    kla3I.pack(pady=4, padx=5)

def kla3def_destroy():
    global kla3A
    global kla3I
    kla3A.destroy()
    kla3I.destroy()
    
#------------------------------------------------------------- 4 ---- klaszter allapota ------------
def kla4def():
    global vn
    global kla4_1
    vn = 3
    menu_hide()
    menu_button.pack(pady=20)
    ok=aklaszter.kl_ellenorzes()
    if ok[0]=='Klaszter állapota megfelelő.':
        label=Label(ablak,text=ok[0],bg=hsz)
        label.pack(pady=20)
        kla4_1.append(label)
    else:
        label=Label(ablak,text='Klaszter állapota nem megfelelő.',bg=hsz)
        label.pack(pady=10)
        kla4_1.append(label)
        for i in ok:
            label=Label(ablak,text=i,bg=hsz)
            label.pack(pady=10)
            kla4_1.append(label)

def kla4def_destroy():
    global kla4_1
    for i in range(len(kla4_1)):
        kla4_1[i].destroy()
    kla4_1=[]

#------------------------------------------------------------- 5 ---- adott program peldany adatai ----
def kla5def_1():
    global vn
    global kla5_1
    global kla5_2
    vn=4
    menu_hide()
    menu_button.pack(pady=20)
    kla5def_2_destroy()
    prog_szam=len(aklaszter.kl_adatok)
    if (prog_szam) % 5==0:
        sor=(prog_szam)//5
    else:
        sor=(prog_szam+5)//5
    for i in range(sor):
        frame=Frame(ablak,bg=hsz)
        frame.pack(side=TOP,pady=10)
        kla5_1.append(frame)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                k=i*5+j
                frame=Button(kla5_1[i],text=aklaszter.kl_adatok[k].get("nev"),command=lambda k=k: kla5def_2(k),bg=gsz1,activebackground=gsz1)
                frame.pack(side=LEFT,padx=5,pady=4)
                kla5_2.append(frame)

def kla5def_2(k):
    global vn
    valasz=vn+1
    kla5def_1_destroy()
    kla5_label = Label(ablak,text=aklaszter.kl_adatok[k].get("nev")+' példányai:',bg=hsz)
    kla5_label.pack(pady=20)
    kla5_list=aklaszter.monitoring(valasz,aklaszter.kl_adatok[k].get("nev"))
    prog_szam=len(kla5_list)
    if prog_szam % 5 == 0:
        sor = prog_szam // 5
    else:
        sor = (prog_szam + 5) // 5
    for i in range(sor):
        frame = Frame(ablak,bg=hsz)
        frame.pack(side=TOP)
        kla5_3.append(frame)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                frame = Frame(kla5_3[i], highlightbackground="black", highlightthickness=1,bg=hsz)
                frame.pack(side=LEFT, padx=8, pady=8)
                kla5_4.append(frame)
    for i in range(prog_szam):
        label1 = Label(kla5_4[i], text=kla5_list[i].get('azonosito'),bg=hsz)
        label2 = Label(kla5_4[i], text=kla5_list[i].get('szamitogep'),bg=hsz)
        label3 = Label(kla5_4[i], text='Processzorok - '+str(kla5_list[i].get('processzorok')),bg=hsz)
        label4 = Label(kla5_4[i], text='Memória - '+str(kla5_list[i].get('memoria')),bg=hsz)
        kla5_5.append(label1)
        kla5_5.append(label2)
        kla5_5.append(label3)
        kla5_5.append(label4)
        label1.pack(padx=5, pady=1)
        label2.pack(padx=5, pady=1)
        label3.pack(padx=5, pady=1)
        label4.pack(padx=5, pady=1)
        menu_button.pack(pady=4)
    vissza=Button(ablak,text='Vissza',command=kla5def_1, font=('TkDefaultFont', 10),bg='#fae1ca',activebackground='#fae1ca')
    vissza.pack(pady=10)
    kla5_5.append(vissza)
    kla5_5.append(kla5_label)

def kla5def_destroy():
    kla5def_1_destroy()
    kla5def_2_destroy()

def kla5def_1_destroy():
    global kla5_1
    global kla5_2
    for i in range(len(kla5_1)):
        kla5_1[i].destroy()
    for i in range(len(kla5_2)):
        kla5_2[i].destroy()
    kla5_1 = []
    kla5_2 = []

def kla5def_2_destroy():
    global kla5_3
    global kla5_4
    global kla5_5
    for i in range(len(kla5_3)):
        kla5_3[i].destroy()
    for i in range(len(kla5_4)):
        kla5_4[i].destroy()
    for i in range(len(kla5_5)):
        kla5_5[i].destroy()
    kla5_3 = []
    kla5_4 = []
    kla5_5 = []

#SZAMITOGEPEK------------------------------------------------------------------------------------------------------------------------
    
# szamitogep gombok megjelenitese/eltuntetese
def gepek_pack():
    gep1.pack(side=LEFT, padx=7)
    gep2.pack(side=LEFT, padx=7)
def gepek_forget():
    gep1.pack_forget()
    gep2.pack_forget()
    
def gepdef():
    global gepb
    global klab
    global progb
    if progb:
        program_forget()
        progb=False
    if klab:
        kla_forget()
        klab = False
    if gepb:
        gepek_forget()
        gepb = False
    else:
        gepek_pack()
        gepb = True
#-------------------------------------------------------- 1 ---- szamitogep hozzaadasa --------------------------------
def sz_hozzaad_1():
    global vn
    global sz2_1
    menu_hide()
    menu_button.pack(pady=20)
    for i in range(3):
        frame=Frame(ablak,bg=hsz)
        frame.pack(pady=5)
        sz2_1.append(frame)
    label1=Label(sz2_1[0],text='Számítógép neve: ',width=20,bg=hsz)
    label1.pack(side=LEFT)
    sz2_1.append(label1)
    label2=Label(sz2_1[1],text='Processzor: ',width=20,bg=hsz)
    label2.pack(side=LEFT)
    sz2_1.append(label2)
    label3=Label(sz2_1[2],text='Memória: ',width=20,bg=hsz)
    label3.pack(side=LEFT)
    sz2_1.append(label3)
    for i in range(3):
        entry=Entry(sz2_1[i],width=20)
        entry.pack()
        sz2_1.append(entry)
    button=Button(ablak, text='Hozzáadás',command=sz_hozzaad_2,bg=gsz2,activebackground=gsz2)
    button.pack(pady=20)
    sz2_1.append(button)
    vn=5

def sz_hozzaad_2():
    global sz2_1
    global sz2_2
    sz_ok=0
    sz_voltmar=False
    sz_hozzaad_destroy_2()
    sz_szam=len(aklaszter.szamitogepek)
    if sz2_1[6].get()=='':
        label=Label(ablak,text='Hiányzik a számítógép neve!',bg=hsz)
        label.pack()
        sz2_2.append(label)
    else:
        for i in sz2_1[6].get():
            if ord(i) not in range(48,58):
                if ord(i) not in range(65,91):
                     if ord(i) not in range(97,123):
                          sz_ok=sz_ok+1
    if sz_ok>0:
        label=Label(ablak,text='A számítógép neve érvénytelen karaktert tartalmaz!',bg=hsz)
        label.pack()
        sz2_2.append(label)
    for i in range(sz_szam):
        if aklaszter.szamitogepek[i].get('nev')==sz2_1[6].get():
             label=Label(ablak,text='Ez a név már foglalt!',bg=hsz)
             label.pack()
             sz2_2.append(label)
    sz_ok2=0
    if sz2_1[7].get()=='':
        label=Label(ablak,text='Hiányzik a processzor!',bg=hsz)
        label.pack()
        sz2_2.append(label)
    else:
        for i in sz2_1[7].get():
            if ord(i) not in range(48,58):
                sz_ok2=sz_ok2+1
    if sz_ok2>0:
        label=Label(ablak,text='Hibás processzor szám!',bg=hsz)
        label.pack()
        sz2_2.append(label)
    sz_ok3=0
    if sz2_1[8].get()=='':
        label=Label(ablak,text='Hiányzik a memória!',bg=hsz)
        label.pack()
        sz2_2.append(label)
    else:
        for i in sz2_1[8].get():
            if ord(i) not in range(48,58):
                sz_ok3=sz_ok3+1
    if sz_ok3>0:
        label=Label(ablak,text='Hibás memória szám!',bg=hsz)
        label.pack()
        sz2_2.append(label)
    if len(sz2_2)==0:
        sz_hozzaad_3()

def sz_hozzaad_3():
    global sz2_2
    global sz2_1
    sz_uj_mem=sz2_1[8].get()
    sz_uj_cpu=sz2_1[7].get()
    sz_uj_nev=sz2_1[6].get()
    aklaszter.szamitogep_hozzaad(sz_uj_nev, int(sz_uj_cpu), int(sz_uj_mem))
    sz_hozzaad_destroy()
    label=Label(ablak,text='Új számítógép sikeresen hozzáadva a klaszterhez.',bg=hsz)
    label.pack(pady=20)
    sz2_2.append(label)
    

def sz_hozzaad_destroy():
    global sz2_1
    for i in range(len(sz2_1)):
        sz2_1[i].destroy()
    sz2_1=[]
    sz_hozzaad_destroy_2()

def sz_hozzaad_destroy_2():
    global sz2_2
    for i in range(len(sz2_2)):
        sz2_2[i].destroy()
    sz2_2=[]
#------------------------------------------------------------- 2 ---- szamitogep torlese ----------------------        
def sz_torol_1():
    global sz_1
    global sz_2
    global vn
    menu_hide()
    menu_button.pack(pady=3)
    sz_szam=len(aklaszter.szamitogepek)
    if sz_szam % 5==0:
        sz2=sz_szam//5
    else:
        sz2=(sz_szam+5)//5
    for i in range(sz2):
        frame=Frame(ablak,bg=hsz)
        sz_1.append(frame)
        frame.pack(side=TOP,pady=10)
        for j in range(5):
            if i*5+j<=sz_szam-1:
                k=i*5+j
                frame=Button(sz_1[i],text=aklaszter.szamitogepek[i*5+j].get("nev"),command=lambda k=k: sz_torol_2(k),bg=gsz2,activebackground=gsz2)
                sz_2.append(frame)
                frame.pack(side=LEFT,padx=5,pady=4)
    vn=6

def sz_torol_2(k):
    global sz_3
    global sz_4
    global sz_5
    global sz_2
    sz_torol_destroy_2()
    if len(aklaszter.szamitogepek[k].get("alkalmazasok"))==0:
        sz_torol_3(k)
    else:
        messagebox.showwarning(message='A '+aklaszter.szamitogepek[k].get("nev")+'-t nem lehet törölni mivel még futnak rajta folyamatok.')
        label=Label(ablak,text='A '+aklaszter.szamitogepek[k].get("nev")+'-n még ezek a folyamatok futnak:',bg=hsz)
        label.pack()
        sz_3.append(label)
        k2=len(aklaszter.szamitogepek[k].get("alkalmazasok"))
        if k2 % 2==0:
            sz2=k2//2
        else:
            sz2=(k2+2)//2
        for i in range(sz2):
            frame=Frame(ablak,bg=hsz)
            sz_3.append(frame)
            frame.pack(side=TOP)
            for j in range(2):
                if i*2+j<=k2-1:
                    frame=Frame(sz_3[i+1],highlightbackground="black",highlightthickness=1,bg=hsz)
                    sz_4.append(frame)
                    frame.pack(side=LEFT,padx=5,pady=10)
        for i in range(k2):
            label1=Label(sz_4[i],text=aklaszter.szamitogepek[k].get("alkalmazasok")[i].get('program'),bg=hsz)
            label2=Label(sz_4[i],text='Indítás ideje: '+aklaszter.szamitogepek[k].get("alkalmazasok")[i].get('datum'),bg=hsz)
            label3=Label(sz_4[i],text='Státusz: '+aklaszter.szamitogepek[k].get("alkalmazasok")[i].get('statusz'),bg=hsz)
            label1.pack(padx=3,pady=4)
            label2.pack(padx=3,pady=4)
            label3.pack(padx=3,pady=4)
            sz_5.append(label1)
            sz_5.append(label2)
            sz_5.append(label3)

def sz_torol_3(k):
    if messagebox.askyesno(message='Biztos törli a '+aklaszter.szamitogepek[k].get("nev")+' számítógépet?'):
        sz_2[k].destroy()
        sz_torol_destroy()
        aklaszter.szamitogep_torles(aklaszter.szamitogepek[k].get("nev"))
        sz_torol_1()
        
        

def sz_torol_destroy_2():
    global sz_3
    global sz_4
    global sz_5
    for i in range(len(sz_5)):
        sz_5[i].destroy()
    for i in range(len(sz_4)):
        sz_4[i].destroy()
    for i in range(len(sz_3)):
        sz_3[i].destroy()
    sz_3=[]
    sz_4=[]
    sz_5=[]
            
def sz_torol_destroy():
    global sz_1
    global sz_2
    global sz_3
    global sz_4
    global sz_5
    for i in range(len(sz_2)):
        sz_2[i].destroy()
    for i in range(len(sz_1)):
        sz_1[i].destroy()
    for i in range(len(sz_5)):
        sz_5[i].destroy()
    for i in range(len(sz_4)):
        sz_4[i].destroy()
    for i in range(len(sz_3)):
        sz_3[i].destroy()
    sz_1=[]
    sz_2=[]
    sz_3=[]
    sz_4=[]
    sz_5=[]
#PROGRAMOK---------------------------------------------------------------------------------------------------------------------------
    
# program gombok megjelenitese/eltuntetese
def program_pack():
    prog1.pack(side=LEFT, padx=7)
    prog2.pack(side=LEFT, padx=7)
    prog3.pack(side=LEFT, padx=7)
    prog4.pack(side=LEFT, padx=7)
def program_forget():
    prog1.pack_forget()
    prog2.pack_forget()
    prog3.pack_forget()
    prog4.pack_forget()


def programdef():
    global progb
    global klab
    global gepb
    if gepb:
        gepek_forget()
        gepb = False
    if klab:
        kla_forget()
        klab = False
    if progb:
        program_forget()
        progb = False
    else:
        program_pack()
        progb = True
#------------------------------------------------------- 1 ---- program leallitasa ------------------------------------------      
def prog_leallit_1():
    global vn
    global prog1_1
    global prog1_2
    menu_hide()
    menu_button.pack(pady=5)
    prog_szam=len(aklaszter.kl_adatok)
    vn=7
    if (prog_szam) % 5==0:
        sz2=(prog_szam)//5
    else:
        sz2=(prog_szam+5)//5
    for i in range(sz2):
        frame=Frame(ablak,bg=hsz)
        prog1_1.append(frame)
        frame.pack(side=TOP,pady=10)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                k=i*5+j
                frame=Button(prog1_1[i],text=aklaszter.kl_adatok[k].get("nev"),command=lambda k=k: prog_leallit_2(k),bg=gsz3,activebackground=gsz3)
                prog1_2.append(frame)
                frame.pack(side=LEFT,padx=5,pady=4)

def prog_leallit_2(k):
    if messagebox.askyesno(message='Biztos leállítja a '+aklaszter.kl_adatok[k].get("nev")+' programot?'):
        aklaszter.program_leallit(aklaszter.kl_adatok[k].get("nev"))
        prog1_2[k].destroy()
        prog_leallit_destroy()
        prog_leallit_1()

def prog_leallit_destroy():
    global prog1_1
    global prog1_2
    for i in range(len(prog1_2)):
        prog1_2[i].destroy()
    for i in range(len(prog1_1)):
        prog1_1[i].destroy()
    prog1_1=[]
    prog1_2=[]
#------------------------------------------------------- 2 ---- program adatainak modositasa ------------------
def prog_modosit_1():
    global vn
    global prog2_1
    global prog2_2
    prog_modosit_destroy_2()
    prog_szam=len(aklaszter.kl_adatok)
    menu_hide()
    menu_button.pack(pady=5)
    vn=8
    if (prog_szam) % 5==0:
        sz2=(prog_szam)//5
    else:
        sz2=(prog_szam+5)//5
    for i in range(sz2):
        frame=Frame(ablak,bg=hsz)
        prog2_1.append(frame)
        frame.pack(side=TOP,pady=10)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                k=i*5+j
                frame=Button(prog2_1[i],text=aklaszter.kl_adatok[k].get("nev"),command=lambda k=k: prog_modosit_2(k),bg=gsz3,activebackground=gsz3)
                prog2_2.append(frame)
                frame.pack(side=LEFT,padx=5,pady=4)

def prog_modosit_2(k):
    global prog2_3
    global prog2_4
    prog_modosit_destroy_1()
    label1=Label(ablak,text=aklaszter.kl_adatok[k].get("nev"),bg=hsz)
    label1.pack(pady=20)
    for i in range(3):
        frame=Frame(ablak,bg=hsz)
        frame.pack(pady=4)
        prog2_3.append(frame)
    label=Label(prog2_3[0],text='Darabszám',width=12,bg=hsz)
    label.pack(side=LEFT)
    prog2_4.append(label)
    entry=Entry(prog2_3[0],width=20)
    entry.pack(side=LEFT)
    entry.insert(0,str(aklaszter.kl_adatok[k].get('szam')))
    prog2_4.append(entry)
    label=Label(prog2_3[1],text='Processzor',width=12,bg=hsz)
    label.pack(side=LEFT)
    prog2_4.append(label)
    entry=Entry(prog2_3[1],width=20)
    entry.pack(side=LEFT)
    entry.insert(0,str(aklaszter.kl_adatok[k].get('processzorok')))
    prog2_4.append(entry)
    label=Label(prog2_3[2],text='Memória',width=12,bg=hsz)
    label.pack(side=LEFT)
    prog2_4.append(label)
    entry=Entry(prog2_3[2],width=20)
    entry.pack(side=LEFT)
    entry.insert(0,str(aklaszter.kl_adatok[k].get('memoria')))
    prog2_4.append(entry)
    gombok_frame=Frame(ablak,bg=hsz)
    gombok_frame.pack()
    prog2_3.append(gombok_frame)
    button=Button(gombok_frame,text='Mentés',command=lambda k=k: prog_modosit_3(k),bg=gsz3,activebackground=gsz3)
    button.pack(pady=20,side=LEFT,padx=4)
    prog2_3.append(button)
    prog2_3.append(label1)
    vissza=Button(gombok_frame, text='Vissza',command=prog_modosit_1,bg=gsz3,activebackground=gsz3)
    vissza.pack(side=LEFT,pady=20,padx=4)
    prog2_3.append(vissza)
    
def prog_modosit_3(k):
    global prog2_4
    ok=0
    for i in prog2_4[1].get():
            if ord(i) not in range(48,58):
                ok=ok+1
    for i in prog2_4[3].get():
            if ord(i) not in range(48,58):
                ok=ok+1
    for i in prog2_4[5].get():
            if ord(i) not in range(48,58):
                ok=ok+1
    if ok==0:
        szam=int(prog2_4[1].get())
        cpu=int(prog2_4[3].get())
        mem=int(prog2_4[5].get())
        aklaszter.program_modosit(aklaszter.kl_adatok[k].get("nev"),szam,cpu,mem)
        messagebox.showinfo(message='Sikeresen elmentve.')
        prog_modosit_1()
    else:
        messagebox.showwarning(message='Hibás adatok!')
    
    
def prog_modosit_destroy_1():
    global prog2_1
    global prog2_2
    for i in range(len(prog2_2)):
        prog2_2[i].destroy()
    for i in range(len(prog2_1)):
        prog2_1[i].destroy()
    prog2_1=[]
    prog2_2=[]

def prog_modosit_destroy_2():
    global prog2_3
    global prog2_4
    global prog2_5
    for i in range(len(prog2_5)):
        prog2_5[i].destroy()
    for i in range(len(prog2_4)):
        prog2_4[i].destroy()
    for i in range(len(prog2_3)):
        prog2_3[i].destroy()
    prog2_3=[]
    prog2_4=[]
    prog2_5=[]

def prog_modosit_destroy():
    prog_modosit_destroy_1()
    prog_modosit_destroy_2()
#------------------------------------------------------- 3 ---- uj programpeldany futtatasa ------------
def prog_uj_1():
    global vn
    global prog3_1
    global prog3_2
    menu_hide()
    menu_button.pack(pady=5)
    vn=9
    prog_uj_destroy_2()
    prog_szam=len(aklaszter.kl_adatok)
    if (prog_szam) % 5==0:
        sz2=(prog_szam)//5
    else:
        sz2=(prog_szam+5)//5
    for i in range(sz2):
        frame=Frame(ablak,bg=hsz)
        prog3_1.append(frame)
        frame.pack(side=TOP,pady=10)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                k=i*5+j
                frame=Button(prog3_1[i],text=aklaszter.kl_adatok[k].get("nev"),command=lambda k=k: prog_uj_2(k),bg=gsz3,activebackground=gsz3)
                prog3_2.append(frame)
                frame.pack(side=LEFT,padx=5,pady=4)

def prog_uj_2(k):
    global prog3_3
    global prog3_4
    sz_szam=len(aklaszter.szamitogepek)
    prog_uj_destroy_1()
    prog_uj_destroy_3()
    if sz_szam % 5==0:
        sz2=sz_szam//5
    else:
        sz2=(sz_szam+5)//5
    for i in range(sz2):
        frame=Frame(ablak,bg=hsz)
        prog3_3.append(frame)
        frame.pack(side=TOP,pady=10)
        for j in range(5):
            if i*5+j<=sz_szam-1:
                k2=[k, i*5+j]
                frame=Button(prog3_3[i],text=aklaszter.szamitogepek[i*5+j].get("nev"),command=lambda k2=k2: prog_uj_3(k2),bg=gsz3,activebackground=gsz3)
                prog3_4.append(frame)
                frame.pack(side=LEFT,padx=5,pady=4)
    vissza=Button(ablak,text='Vissza',command=prog_uj_1,bg='#ffdac6',activebackground='#ffdac6')
    vissza.pack()
    prog3_4.append(vissza)
    vn=6

def prog_uj_3(k2):
    global prog3_5
    ok=aklaszter.hozzaad_ell(aklaszter.kl_adatok[k2[0]].get('nev'),aklaszter.szamitogepek[k2[1]].get('nev'))
    if ok:
        aklaszter.programpeldany_hozzaad(aklaszter.kl_adatok[k2[0]].get('nev'),aklaszter.szamitogepek[k2[1]].get('nev'))
        prog_uj_destroy_2()
        label=Label(ablak,text='Új programpéldány sikeresen hozzáadva.',bg=hsz)
        label.pack(pady=20)
        prog3_5.append(label)
    else:
        messagebox.showwarning(message='Nincs elég erőforráskapacitás a gépen.')

def prog_uj_destroy_1():
    global prog3_1
    global prog3_2
    for i in range(len(prog3_2)):
        prog3_2[i].destroy()
    for i in range(len(prog3_1)):
        prog3_1[i].destroy()
    prog3_1=[]
    prog3_2=[]

def prog_uj_destroy_2():
    global prog3_3
    global prog3_4
    for i in range(len(prog3_4)):
        prog3_4[i].destroy()
    for i in range(len(prog3_3)):
        prog3_3[i].destroy()
    prog3_3=[]
    prog3_4=[]

def prog_uj_destroy_3():
    global prog3_5
    for i in range(len(prog3_5)):
        prog3_5[i].destroy()
    prog3_5=[]

def prog_uj_destroy():
    prog_uj_destroy_1()
    prog_uj_destroy_2()
    prog_uj_destroy_3()
#------------------------------------------------------- 4 ---- programpeldany leallitasa -----------
def prog_peld_leallit_1():
    global vn
    global prog4_1
    global prog4_2
    prog_szam=len(aklaszter.kl_adatok)
    menu_hide()
    menu_button.pack(pady=5)
    vn=10
    if (prog_szam) % 5==0:
        sz2=(prog_szam)//5
    else:
        sz2=(prog_szam+5)//5
    for i in range(sz2):
        frame=Frame(ablak,bg=hsz)
        prog4_1.append(frame)
        frame.pack(side=TOP,pady=10)
        for j in range(5):
            if i*5+j<=prog_szam-1:
                k=i*5+j
                frame=Button(prog4_1[i],text=aklaszter.kl_adatok[k].get("nev"),command=lambda k=k: prog_peld_leallit_2(k),bg=gsz3,activebackground=gsz3)
                prog4_2.append(frame)
                frame.pack(side=LEFT,padx=5,pady=4)
                
def prog_peld_leallit_2(k):
    global prog4_3
    prog4_list=[]
    prog_peld_leallit_destroy_1()
    sz_szam=len(aklaszter.szamitogepek)
    for i in range(sz_szam):
        prog_szam=len(aklaszter.szamitogepek[i].get('alkalmazasok'))
        for j in range(prog_szam):
            if aklaszter.szamitogepek[i].get('alkalmazasok')[j].get('program').startswith(aklaszter.kl_adatok[k].get("nev")):
                prog4_list.append(aklaszter.szamitogepek[i].get('alkalmazasok')[j].get('program'))
    button=Button(ablak,text='Vissza',command=prog_peld_leallit_4,width=5,bg='#ffdac6',activebackground='#ffdac6')
    button.pack(pady=5)
    for i in range(len(prog4_list)):
        t=[prog4_list[i], i]
        frame=Button(ablak,text=prog4_list[i],command=lambda t=t: prog_peld_leallit_3(t),bg=gsz3,activebackground=gsz3)
        prog4_3.append(frame)
        frame.pack(padx=5,pady=4)
    prog4_3.append(button)

def prog_peld_leallit_3(k2):
    if messagebox.askyesno(message='Biztos leállítja a '+k2[0]+' programpéldányt?'):
        aklaszter.programpeldany_torles(k2[0])
        prog4_3[k2[1]].destroy()

def prog_peld_leallit_4():
    prog_peld_leallit_destroy_2()
    prog_peld_leallit_1()
    
def prog_peld_leallit_destroy_1():
    global prog4_1
    global prog4_2
    for i in range(len(prog4_2)):
        prog4_2[i].destroy()
    for i in range(len(prog4_1)):
        prog4_1[i].destroy()
    prog4_2=[]
    prog4_1=[]
    
def prog_peld_leallit_destroy_2():
    global prog4_3
    for i in range(len(prog4_3)):
        prog4_3[i].destroy()
    prog4_3=[]

def prog_peld_leallit_destroy():
    prog_peld_leallit_destroy_1()
    prog_peld_leallit_destroy_2()
# ==================================================================================================================================
# ==================================================================================================================================
# ABLAK
ablak = Tk()

hsz='#FFE0E6'
gsz1='#FFECEE'
gsz2='#FFDCDF'
gsz3='#FFC7CC'

ablak.title('Klaszter')
ablak.config(bg=hsz)

hossz = ablak.winfo_screenwidth()
mag = ablak.winfo_screenheight()
x = (hossz - 800) // 2
y = (mag - 600) // 2

ablak.geometry(f'800x600+{x}+{y}')

ablak.bind('<Return>', enter)
enter_b=False


# INDITAS----------------------------------------------------------------------------------------------------------------------------
frame=Frame(ablak)
frame.pack(pady=30)

utvonal = Label(ablak, text='Útvonal: ')
utvonal.config(font=('Times New Roman', 20),bg=hsz)
utvonal.pack(pady=20)

utvonal_bemenet = Entry(ablak)
utvonal_bemenet.config(font=('TkDefaultFont', 15),bg='#F7EEED')
utvonal_bemenet.pack()

ind = Button(ablak, text='Indítás', font=('TkDefaultFont', 13), command=ut,bg=gsz1,activebackground=gsz2)
ind.pack(pady=20)

# MENU--------------------------------------------------------------------------------------------------------------------------------

v = [kla1def_destroy, kla2def_destroy, kla3def_destroy, kla4def_destroy, kla5def_destroy, sz_hozzaad_destroy, sz_torol_destroy, prog_leallit_destroy, prog_modosit_destroy, prog_uj_destroy, prog_peld_leallit_destroy]
menu_button = Button(ablak, text='Menü', font=('TkDefaultFont', 11), command=menu,bg='#ffdab9',activebackground='#ffdab9')

allapot_label=Label(ablak)

#MONITORING--------------------------------------------------------------------------------------------------------------------------
klab = False

klaframe = Frame(ablak,bg=hsz)

kla = Button(klaframe, text='Monitoring', font=('TkDefaultFont', 12),bg=gsz1,activebackground=gsz1)
kla.config(command=kladef)

k1=0
kla1 = Button(klaframe, text='Számítógépek\n kihasználtsága', font=('TkDefaultFont', 9), command=lambda k1=k1: kla1def(k1),bg=gsz1,activebackground=gsz1)
kla2 = Button(klaframe, text='Program\n példányok', font=('TkDefaultFont', 9), command=kla2def_1,bg=gsz1,activebackground=gsz1)
kla3 = Button(klaframe, text='Folyamatok\n száma', font=('TkDefaultFont', 9), command=kla3def,bg=gsz1,activebackground=gsz1)
kla4 = Button(klaframe, text='Klaszter\n állapota', font=('TkDefaultFont', 9), command=kla4def,bg=gsz1,activebackground=gsz1)
kla5 = Button(klaframe, text='Program\n adatok', font=('TkDefaultFont', 9), command=kla5def_1,bg=gsz1,activebackground=gsz1)

kla1_1 = []
kla1_2 = []
kla1_3 = []

kla2_1 = []
kla2_2 = []
kla2_3 = []
kla2_4 = []
kla2_5 = []

kla4_1 = []

kla5_1 = []
kla5_2 = []
kla5_3 = []
kla5_4 = []
kla5_5 = []

#SZAMITOGEPEK------------------------------------------------------------------------------------------------------------------------
gepb = False

gepframe = Frame(ablak,bg=hsz)

gepek = Button(gepframe, text='Számítógépek', font=('TkDefaultFont', 12),bg=gsz2,activebackground=gsz2)
gepek.config(command=gepdef)

gep1 = Button(gepframe, text='Számítógép hozzáadása', font=('TkDefaultFont', 9), command=sz_hozzaad_1,bg=gsz2,activebackground=gsz2)
gep2 = Button(gepframe, text='Számítógép törlése', font=('TkDefaultFont', 9), command=sz_torol_1,bg=gsz2,activebackground=gsz2)

sz_1=[]
sz_2=[]
sz_3=[]
sz_4=[]
sz_5=[]

sz2_1=[]
sz2_2=[]

#PROGRAMOK---------------------------------------------------------------------------------------------------------------------------
progb = False

progframe = Frame(ablak,bg=hsz)

programok = Button(progframe, text='Programok', font=('TkDefaultFont', 12),bg=gsz3,activebackground=gsz3)
programok.config(command=programdef)

prog1 = Button(progframe, text='Program\n leállítása', font=('TkDefaultFont', 9), command=prog_leallit_1,bg=gsz3,activebackground=gsz3)
prog2 = Button(progframe, text='Program adatainak\n módosítása', font=('TkDefaultFont', 9), command=prog_modosit_1,bg=gsz3,activebackground=gsz3)
prog3 = Button(progframe, text='Új programpéldány\n futtatása', font=('TkDefaultFont', 9), command=prog_uj_1,bg=gsz3,activebackground=gsz3)
prog4 = Button(progframe, text='Programpéldány\n leállítása', font=('TkDefaultFont', 9), command=prog_peld_leallit_1,bg=gsz3,activebackground=gsz3)

prog1_1=[]
prog1_2=[]

prog2_1=[]
prog2_2=[]
prog2_3=[]
prog2_4=[]
prog2_5=[]

prog3_1=[]
prog3_2=[]
prog3_3=[]
prog3_4=[]
prog3_5=[]

prog4_1=[]
prog4_2=[]
prog4_3=[]

ablak.mainloop()
