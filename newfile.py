from bs4 import BeautifulSoup

import lxml
import pandas as pd
dlist=[]
file1 = 'file0.xml'
file2 ='file1.xml'
# file3='prettyxml.xml'
# file4 ='prettyxml2.xml'
files=[file1,file2]
itemdatas=[]
def onlyvalues(list):
    newlist=[]
    for l in list:
        if type(l)==str:
            newlist.append(l)
        elif l !=None :
            newlist.append(l.text)
        else:
            newlist.append('-')
    return newlist

def coolpower(dlist):
    for li in dlist:

        if 'Гликолевый рекуператор' in li[0]:
            li[9]=li[13]
            li[13]="-"
    return dlist



def createAHU(list):
    correctlist=[]
    for l in list[0]:
        m = len(list) - 1
        if l=="-":
            nc=list[0].index(l)
            for i in range(m):
                if list[i][nc]!='-':
                    list[0][nc]=list[i][nc]
    correctlist=list[0][1:]
    return correctlist

ahulist=[]
for fil in files:
    with (open (fil, 'r') as file):
        soups=BeautifulSoup(file,'lxml').find_all('item')

        totallist=[]
        for soup in soups:
            list=[]

            sign = file.name.split('/')[-1].split('.')[0]
            chaneltype=soup.find('chaneltype')
            name = soup.find('name')
            flowwork = soup.find('flowwork')
            pressurework = soup.find('pressurework')
            revnominalwheel=soup.find('revnominalwheel')
            revwork = soup.find('revwork')
            nominalpower = soup.find('nominalpower')
            ifrequency=soup.find('ifrequency')
            tglycolinflow = soup.find('tglycolinflow')
            tglycoloutflow = soup.find('tglycoloutflow')
            qneed = soup.find('qneed')
            kpd=soup.find('kpd')
            glycoldp = soup.find('glycoldp')
            tinairinflow = soup.find('tinairinflow')
            toutairoutflow = soup.find('toutairoutflow')
            tairmax=soup.find('tairmax')
            droppressurewater = soup.find('droppressurewater')
            cleaningclass=soup.find('cleaningclass')
            glneed=None
            list=(name,sign,flowwork,pressurework,revnominalwheel, nominalpower,revwork,tinairinflow,\
                        toutairoutflow,glneed,kpd,toutairoutflow,tairmax,qneed,droppressurewater, cleaningclass)
            #print(list)
            newlist=onlyvalues(list)
            totallist.append(newlist)
        totallist= coolpower(totallist)
        #print (totallist)



        #print (totallist[4])
        ahulist.append(createAHU(totallist))
columns=['Номер системы','AirVolume','Pressure','FanRotation','NominalPower','RotationMotor','T in Recup','T out Recup',\
         'Q chill','KPD','TinHeatI','ToutHeatII','QHeat','PresDropHeatI','Filter']
df = pd.DataFrame(data=ahulist, columns=columns)
print(df)
    # try:
    #     for soup in soups:
    #         flowwork=soup.find('flowwork').text
    #         print(flowwork)
    #         pressurework = soup.find('pressurework').text
    #         print(pressurework)
    #         revnominalmotor = soup.find('revnominalmotor').text
    #         #print(revnominalmotor)
    #         ifrequency = soup.find('ifrequency').text
    #         #print(ifrequency)
    #         nominalpower = soup.find('nominalpower').text
    #         #print(nominalpower)
    #         tglycolinflow = soup.find('tglycolinflow').text
    #         #print(tglycolinflow)
    #         tglycoloutflow = soup.find('tglycoloutflow').text
    #         #print(tglycoloutflow)
    #         qneed = soup.find('qneed').text
    #         glneed = soup.find('qneed').find_next('qneed').text
    #         glycoldp = soup.find('glycoldp').text
    #         tinairinflow = soup.find('tinairinflow').text
    #         toutairoutflow = soup.find('toutairoutflow').text
    #         droppressurewater = soup.find('droppressurewater').text
    #         if droppressurewater==None:
    #             droppressurewater="-"
    #         print(droppressurewater)
    #
    #     data = [flowwork, pressurework, nominalpower, revnominalmotor, tglycolinflow, tglycoloutflow, qneed, \
    #             glycoldp, tinairinflow,\
    #             toutairoutflow, glneed, droppressurewater]
    #     itemdatas.append(data)
    #     df = pd.DataFrame(data=itemdatas)
    #     df.to_csv('dfres.csv', index=False, sep=";")
    # except:
    #     pass







