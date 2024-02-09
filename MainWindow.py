from tkinter import*
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
import xml.dom.minidom as xdm
from bs4 import BeautifulSoup
import lxml
import pandas as pd


def onlyvalues(list):
    newlist = []
    for l in list:
        if type(l) == str:
            newlist.append(l)
        elif l != None:
            newlist.append(l.text)
        else:
            newlist.append('-')
    return newlist


def coolpower(dlist):
    for li in dlist:

        if 'Гликолевый рекуператор' in li[0]:
            li[9] = li[13]
            li[13] = "-"
    return dlist


def createAHU(list):
    correctlist = []
    for l in list[0]:
        m = len(list) - 1
        if l == "-":
            nc = list[0].index(l)
            for i in range(m):
                if list[i][nc] != '-':
                    list[0][nc] = list[i][nc]
    correctlist = list[0][1:]
    return correctlist
ahulist=[]
def createcsv(prettyfile):
    print(prettyfile)
    dlist = []

    # file3='prettyxml.xml'
    # file4 ='prettyxml2.xml'

    itemdatas = []
    #ahulist = []
    #for fil in prettyfiles:
        #print(fil)
        #name=f'{fil}'
    with (open(str(prettyfile), 'r') as file):
        soups = BeautifulSoup(file, 'xml').find_all('item')
        totallist = []
        for soup in soups:
            list = []
            #sign = file.name
            sign = file.name.split('/')[-1].split('.')[0]
            chaneltype = soup.find('chaneltype')
            name = soup.find('name')
            flowwork = soup.find('flowwork')
            pressurework = soup.find('pressurework')
            revnominalwheel = soup.find('revnominalwheel')
            revwork = soup.find('revwork')
            nominalpower = soup.find('nominalpower')
            ifrequency = soup.find('ifrequency')
            tglycolinflow = soup.find('tglycolinflow')
            tglycoloutflow = soup.find('tglycoloutflow')
            qneed = soup.find('qneed')
            kpd = soup.find('kpd')
            glycoldp = soup.find('glycoldp')
            tinairinflow = soup.find('tinairinflow')
            toutairoutflow = soup.find('toutairoutflow')
            tairmax = soup.find('tairmax')
            droppressurewater = soup.find('droppressurewater')
            cleaningclass = soup.find('cleaningclass')
            glneed = None
            list = (name, sign, flowwork, pressurework, revnominalwheel, nominalpower, revwork, tinairinflow, \
                    toutairoutflow, glneed, kpd, toutairoutflow, tairmax, qneed, droppressurewater, cleaningclass)
                # print(list)
            newlist = onlyvalues(list)
            totallist.append(newlist)
            totallist = coolpower(totallist)
            # print (totallist)

            # print (totallist[4])
    ahulist.append(createAHU(totallist))

    #print(df)

    #df.to_csv('res.csv')
    return ahulist

def savefile():
    columns = ['Номер системы', 'AirVolume', 'Pressure', 'FanRotation', 'NominalPower', 'RotationMotor', 'T in Recup',
               'T out Recup', \
               'Q chill', 'KPD', 'TinHeatI', 'ToutHeatII', 'QHeat', 'PresDropHeatI', 'Filter']
    df = pd.DataFrame(data=ahulist, columns=columns)
    filename=fd.asksaveasfilename()
    df.to_csv(filename)
    ahulist.clear()
def prettify(files):
    prettyfile=""
    preparedfiles=[]
    count = 0
    for fi in files:
        with (open(fi, 'r') as file):
            filename =fi
            #print(fi)
            #filename = f'{'file'}{count}{'.xml'}'
            dom = xdm.parse(file)
            prettyxml = dom.toprettyxml()
        with open(filename, 'w') as wfile:
            wfile.write(prettyxml)
            prettyfile=filename
            count += 1
    createcsv(prettyfile)
def xlexport():
    os.system('py')
    os.system('newfile.py')
    return
def openfiles():
    files=[]
    filetypes=(
        ('text.files','*.xml'),
        ('All files','*.*')
    )
    filenames = fd.askopenfilenames(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)


    showinfo(
        title='Selected Files',
        message=filenames
    )
    for i in filenames:
        files.append(i)
        prettify(files)


root=Tk()
root.title('NEDparse')
#root.iconbitmap('/Users/stanislavdidenko/PycharmProjects/pythonProject2/capibara.ico')
icon=PhotoImage(file="capibara.png")
root.iconphoto(False,icon)
root.geometry('300x250')

label = Label(text="Hello dude, let's make some HOVS")
openfilebtn = Button(root,text="Choose files", command = openfiles)
prettifybtn = Button(text="Prepare datas",command=prettify)
xlbtn = Button(text="Export in Excel",command=savefile)

label.pack()
openfilebtn.pack()
xlbtn.pack()
root.mainloop()