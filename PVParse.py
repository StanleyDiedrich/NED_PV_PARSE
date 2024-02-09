from tkinter import*
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
import xml.dom.minidom as xdm
from bs4 import BeautifulSoup
import lxml
import pandas as pd

import lxml

dlist=[]
ahulist=[]
#file = 'Result.csv'

itemdatas=[]
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

def groupparts(list):
    grouplist=[]
    supply=[]
    exhaust=[]
    for lis in list:
        if lis[2] == "inflow":
            supply.append(lis)
        else:
            exhaust.append(lis)
        grouplist=[supply,exhaust]
    #print(grouplist)
    ahuunit(grouplist)


def ahuunit(grouplist):

    for lis in grouplist:

        unitlist = []
        for li in lis:

            string = li[0]
            global name
            global systemname
            global channeltype
            # вентилятор
            global flowwork
            global pressurework
            global revnominalwheel
            global reserveengine
            global hasdoublefan
            # электродвигатель
            global type
            global revwork
            global nominalpower
            # рекуператор
            global heatexchangetemperaturewinter
            global heatexchangetemperaturewinterout
            global qrecneed
            global thermalefficiencyofheatrecovery
            # нагреватель 1 ступень
            global h1carriertype
            global h1quantity
            global tinairinflow
            global tairmax
            global qh1need
            global droppressurewaterh1
            # нагреватель 2 ступени
            global h2carriertype
            global h2quantity
            global h2airintemp
            global h2airouttemp
            global h2need
            global h2droppressurewater
            # охладитель
            global glcarriertype
            global glquantity
            global tglycolinflowair
            global tglycoloutflowair
            global inentalpy
            global outentalpy
            global glneed
            global kpd
            global glycoldp
            # ороситель
            global humidifyinirrigation
            global humidifyoutirrigation
            global waterconsumption
            global daywaterconsumption
            # фильтр
            global cleaningclass
            global filterlist

            if "Вентилятор" in string.split():
                name=li[0]
                systemname=li[1]
                channeltype=li[2]
                flowwork = li[3]
                pressurework=li[4]
                revnominalwheel=li[5]
                reserveengine=li[6]
                hasdoublefan=li[7]
                fanlist=[name,systemname,channeltype,flowwork,pressurework,revnominalwheel,reserveengine,hasdoublefan]

                #return print(fandata)
            if 'АИР' in string:
                type=li[0]
                revwork=li[9]
                nominalpower=li[10]
                motorlist=[type,revwork,nominalpower]
            if "рекуператор" in string:
                heatexchangetemperaturewinter=li[11]
                heatexchangetemperaturewinterout=li[12]
                qrecneed=li[13]
                thermalefficiencyofheatrecovery=li[14]
                reqlist=[heatexchangetemperaturewinter,heatexchangetemperaturewinterout,qrecneed,thermalefficiencyofheatrecovery]


            if  "нагрев" and "3" in string:

                h1carriertype = li[15]
                h1quantity = '1'
                tinairinflow = li[17]
                tairmax = li[18]
                qh1need = li[19]
                droppressurewaterh1 = li[20]
                heater1list = [h1carriertype, h1quantity, tinairinflow, tairmax, qh1need, droppressurewaterh1]

            if "нагр" and "2" in string:
                h2carriertype=li[30]
                h2quantity=1
                h2airintemp=li[32]
                h2airouttemp=li[33]
                h2need=li[34]
                h2droppressurewater=li[35]
                heater2list=[h2carriertype, h2quantity, h2airintemp, h2airouttemp, h2need, h2droppressurewater]


            if "хла" in string:
                glcarriertype=li[21]
                glquantity=li[22]
                tglycolinflowair=li[23]
                tglycoloutflowair=li[24]
                inentalpy=li[25]
                outentalpy=li[26]
                glneed=li[27]
                kpd=li[28]
                glycoldp=li[29]
                coollist=[glcarriertype,glquantity,tglycolinflowair,tglycoloutflowair,inentalpy,outentalpy,glneed,kpd,glycoldp]

            if "орошения" in string:
                humidifyinirrigation=li[36]
                humidifyoutirrigation=li[37]
                waterconsumption=li[38]
                daywaterconsumption=str(int(waterconsumption)*24)
                humlist=[humidifyinirrigation,humidifyoutirrigation,waterconsumption,daywaterconsumption]
        reslist=(fanlist+motorlist+reqlist+heater1list+coollist+heater2list+humlist)
        ahulist.append(reslist)
    return ahulist
        #return ahulist.append(reslist)
            #reslist = fanlist+motorlist+reqlist+heater1list+coollist+heater2list+humlist
    # return print(reslist)
    #unitlist.append(reslist)
    #return print(reslist)





def onlyvalues(list):
    newlist=[]

    for l in list:
        try:
            if l != None:
                newlist.append(l.text)
            else:
                newlist.append('-')
        except:
            newlist.append(l)

    return newlist

def coolpower(dlist):
    for li in dlist:

        if 'Гликолевый рекуператор' in li[0]:
            li[9]=li[13]
            li[13]="-"
    return dlist

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


# def createAHU(list): это не надо
#     correctlist=[]
#     for l in list[0]:
#         m = len(list) - 1
#         if l=="-":
#             nc=list[0].index(l)
#             for i in range(m):
#                 if list[i][nc]!='-':
#                     list[0][nc]=list[i][nc]
#     correctlist=list[0][1:]
#     return correctlist

def createcsv(file):
    ahulist=[]
    filename=file
    with (open (filename, 'r') as file):
        soups=BeautifulSoup(file,'xml').find_all('item')
        totallist=[]
        for soup in soups:
            list=[]
            systemname = file.name.split('/')[-1].split('.')[0]

                #print(systemname)
            name = soup.find('name')
            channeltype = soup.find('channeltype')

                #Вентилятор
            flowwork = soup.find('flowwork')
            pressurework = soup.find('pressurework')
            revnominalwheel=soup.find('revnominalwheel')
            reserveengine=soup.find('isreserveengine')
            hasdoublefan=soup.find('hasdoublefan')
                #Электродвигатель
            type ='-'
            revwork = soup.find('revwork')
            nominalpower = soup.find('nominalpower')
            ifrequency=soup.find('ifrequency')
                # Пластинчатый рекуператор
            heatexchangetemperaturewinter = soup.find('heatexchangetemperaturewinter')
            heatexchangetemperaturewinterout = soup.find('heatexchangetemperaturewinterout')
            qrecneed = soup.find('qneed')
            thermalefficiencyofheatrecovery = soup.find('thermalefficiencyofheatrecovery')
                #Нагреватель первой ступени
            h1carriertype = soup.find('carriertype')
            h1quantity='-'
            tinairinflow = soup.find('tinairinflow')
                #toutairoutflow = soup.find('toutairoutflow')
            tairmax=soup.find('tairmax')
            qh1need=soup.find('qneed')
            droppressurewaterh1 = soup.find('droppressurewater')
                # Воздухоохладитель гликолевый был в файлах с одинарными приточками
            glcarriertype=soup.find('carriertype')
            glquantity='-'
            tglycolinflowair = "-"
            tglycoloutflowair = soup.find('toutmax')
            inentalpy='-'
            outentalpy='-'
            glneed = soup.find('qneed')
            kpd = soup.find('kpd')
            glycoldp = soup.find('droppressurewater')
                #Нагреватель второй ступени
            h2carriertype=soup.find('carriertype')
            h2quantity='-'
            h2airintemp='-'
            h2airouttemp=soup.find('tairmax')
            h2need=soup.find('qneed')
            h2droppressurewater=soup.find('droppressurewater')
                #Увлажнитель
            humidifyinirrigation = soup.find('humidifyinirrigation')
            humidifyoutirrigation=soup.find('humidifyoutirrigation')
            waterconsumption = soup.find('waterconsumption')
            daywaterconsumption = soup.find('waterconsumption')
                #Фильтр
            cleaningclass=soup.find('cleaningclass')

            list=(name,systemname,channeltype,\
                      flowwork,pressurework,revnominalwheel,reserveengine,hasdoublefan,\
                      type,revwork,nominalpower,\
                      heatexchangetemperaturewinter,heatexchangetemperaturewinterout,qrecneed,thermalefficiencyofheatrecovery,\
                      h1carriertype,h1quantity,tinairinflow,tairmax,qh1need,droppressurewaterh1,\
                      glcarriertype,glquantity,tglycolinflowair,tglycoloutflowair,inentalpy,outentalpy,glneed,kpd,glycoldp,\
                      h2carriertype,h2quantity,h2airintemp,h2airouttemp,h2need,h2droppressurewater,\
                      humidifyinirrigation,humidifyoutirrigation,waterconsumption,daywaterconsumption,\
                      cleaningclass
                      )
                #print(list)
            newlist=onlyvalues(list)
                #print(newlist)
            totallist.append(newlist)
        groupparts(totallist)
                    #totallist= coolpower(totallist)
        #print(groupparts(totallist))
    #groupparts(totallist)
        #
        #ahuunit(a)
    # ahulist.extend(a)
    # return print(a)

def savefile():
    columns=["Имя компонента",'Имя системы',"Приточный/Вытяжной",\
             "Расход воздуха","Давление","Обороты вентилятора","Резервный двигатель","Имеет два вентилятора",\
        "Тип эл/виг","Обороты","Мощность номинальная",\
            "Темп вх рекуп","Темп вых рекуп","Мощность","КПД",\
        "Нагр 1 тип","Кол-во","Нагр1 Темп вх","Нагр1 Темп вых","Нагр1 Мощность","Нагр1 dP",\
        "Тип","Кол-во","Охл Темп вх","Охл Темп вых","Охл энт вх","Охл энт вых","Охл мощность","КПД","Охл dP",\
        "Нагр 2 тип","Нагр 2 кол-во","Нагр2 Темп вх","Нагр2 Темп вых","Нагр2 Мощность","Нагр2 dP",\
        "Влаж вх","Влаж вых","Расход воды","Расход суточный"]
        #"Тип"]
    #df = pd.DataFrame(data=ahulist, columns=columns)
    df = pd.DataFrame(data=ahulist,columns=columns)
    filename = fd.asksaveasfilename()
    df.to_csv(filename)
    ahulist.clear()

root =Tk()
root.title('PVParse')
icon=PhotoImage(file="capibara.png")
root.iconphoto(False,icon)
root.geometry('300x250')

label = Label(text="Hello dude, let's make some HOVS")
openfilebtn = Button(root,text="Choose files",command=openfiles)
prettifybtn = Button(text="Prepare datas")
xlbtn = Button(text="Export in Excel",command=savefile)

label.pack()
openfilebtn.pack()
xlbtn.pack()
root.mainloop()