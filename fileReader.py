import os
from PMVPlotting import *
import plotly as py
import plotly.graph_objs as go
import datetime

#if working from office, use this path
b18file = 'c:\\Users\\vhoang\\Desktop\\_TEMP\Model\\BASIS\\BASIS.b18'
temperaturePRN = 'c:\\Users\\vhoang\\Desktop\\_TEMP\\Model\\BASIS\\Results\\temp_1h_Z1.prn'
comfortPRN = 'c:\\Users\\vhoang\\Desktop\\_TEMP\\Model\\BASIS\\Results\\Comfort_1h.prn'

pickedID = 1
Occufilter = 1 #occupation filter signal

#if working from home
#b18file = "E:\\WORK_IN_PROGRESS\\_Temp\\Model\\BASIS\\BASIS.b18"
#temperaturePRN = "E:\\WORK_IN_PROGRESS\\_Temp\\Model\\BASIS\\Results\\temp_1h_Z1.prn"
#comfortPRN = "E:\\WORK_IN_PROGRESS\\_Temp\\Model\\BASIS\\Results\\Comfort_1h.prn"

def checkfile(b18,tempPRN,comfPRN):
    if not os.path.isfile(b18):
        print("Building file *.b18 not found!")
    if not os.path.isfile(tempPRN):
        print("Temperature file *.prn not found!")
    if not os.path.isfile(comfPRN):
        print("Comfort file *.prn not found!")

checkfile(b18file,temperaturePRN,comfortPRN)

def Readb18(b18file):
    '''returns comfort pts dictionary {ID:[X,Y,Z]}'''
    geoposdict = {}
    b18 = open(b18file,"r")
    lines =  b18.readlines()
    for line in lines:
        if "cgeopos" in line:
            newline = line.split()
            ptsID = int(newline[1])
            ptsX, ptsY, ptsZ = float(newline[2]), float(newline[3]), float(newline[4])
            pts = []
            pts.append(ptsX), pts.append(ptsY), pts.append(ptsZ)
            geoposdict[ptsID] = pts
    b18.close()
    return geoposdict

def ReadTemperature(temperaturePRN):
    '''return occupation schedule'''
    occu = []
    hour = []
    temp = open(temperaturePRN,"r")
    lines = temp.readlines()
    lines.pop(0)
    lines.pop(0)
    for line in lines:
        line = line.split()
        try:
            hour.append(int(float(line[0])))
            occu.append(int(float(line[1])))
        except:
            break
    temp.close()
    return hour, occu

def ReadComfort(comfortPRN):
    """returns all comfort values as dictionary {ID:8760values}"""
    comfort = {}
    comf = open(comfortPRN,"r")
    lines = comf.readlines()
    lines.pop(0)
    lines.pop(0)
    #setting up blank dictionary
    dummy = lines[0].split()
    dummy.pop(0)
    for id in range(len(dummy)):
        key = id+1
        comfort[key] = []
    for line in lines:
        line = line.split()
        try:
            line.pop(0)
            for id,value in enumerate(line):
                dkey = int(id) + 1
                comfort[dkey].append(float(value))
        except:
            break
    comf.close()
    return comfort

def ComfortOcc(PMV,occupation):
    """return PMV values only during occupation time"""
    PMVOcc = []
    for id,value in enumerate(occupation):
        if value == 0:
            PMVOcc.append("")
        else:
            PMVOcc.append(PMV[id])
    return PMVOcc

def getXY(hours):
    """for plotting"""
    Xvalue = []
    Yvalue = []
    year = datetime.date.today().year
    for item in hours:
        dummyY = (item-1) % 24 +1
        Yvalue.append(dummyY)
        dummyX = (item-1)//24 +1
        todate = datetime.date(year, 1, 1) + datetime.timedelta(dummyX - 1)
        Xvalue.append(todate)
    return Xvalue,Yvalue

def colorAssign(PMV):
    '''assigining color values based on PMV'''
    color = []
    stat = []
    c_excold, c_cold, c_slcold, c_comf, c_slwarm, c_hot,c_exhot = 0,0,0,0,0,0,0
    for item in PMV:
        if item == "":
            color.append(color_Unoccupied)
            #c_unocc += 1
        else:
            if item < -3:
                dummycolor = color_ExtremeCold
                c_excold += 1
            elif item >= -3 and item < -1.5:
                dummycolor = color_Cold
                c_cold += 1
            elif item >= -1.5 and item < -0.5:
                dummycolor = color_SlightlyCold
                c_slcold += 1
            elif item >= -0.5 and item <= 0.5:
                dummycolor = color_Comfortable
                c_comf += 1
            elif item > 0.5 and item <= 1.5:
                 dummycolor = color_SlightlyWarm
                 c_slwarm += 1
            elif item > 1.5 and item <= 3:
                dummycolor = color_Hot
                c_hot += 1
            elif item > 3:
                dummycolor = color_ExtremeHot
                c_exhot += 1
            color.append(dummycolor)
    stat.append(c_excold),stat.append(c_cold),stat.append(c_slcold),stat.append(c_comf),stat.append(c_slwarm),stat.append(c_hot),stat.append(c_exhot)
    return color, stat

color_Unoccupied = 'rgb(220,220,220)'
color_ExtremeCold = 'rgb(74,0,255)'
color_Cold = 'rgb(0,80,255)'
color_SlightlyCold = 'rgb(0,196,255)'
color_Comfortable = 'rgb(0,255,0)'
color_SlightlyWarm = 'rgb(255,190,0)'
color_Hot = 'rgb(255,54,0)'
color_ExtremeHot = 'rgb(255,255,0'
statname = ['Extreme Cold', 'Cold', 'Slightly Cold', 'Comfortable', 'Slightly Warm','Hot','Extreme Hot']
statcolor = ['rgb(74,0,255)','rgb(0,80,255)','rgb(0,196,255)','rgb(0,255,0)','rgb(255,190,0)','rgb(255,54,0)','rgb(255,255,0']

comfortpts = Readb18(b18file)
hours, occupation = ReadTemperature(temperaturePRN)
comfortdict = ReadComfort(comfortPRN) #{ID:8760 values}

PMV = comfortdict[pickedID] #wholeyear for selected pts
if Occufilter:
    PMVresult = ComfortOcc(PMV,occupation) #filtered
else:
    PMVresult = PMV
colorPMV,stat = colorAssign(PMVresult)
xvalues,yvalues= getXY(hours)

#get statistic for 1 pts
totalhour = sum(occupation) if Occufilter else 8760

pers = []
for item in stat:
    dummy = round(item/totalhour*100,1)
    pers.append(dummy)

#get statistic for all the points
statdict = {} #{ptsID: [statistic1,statistic2,...]}
for ptsID in range(1,len(comfortpts)+1):
    PMVID = comfortdict[ptsID]
    if Occufilter:
        ptsPMV = ComfortOcc(PMVID,occupation) #filtered
    else:
        ptsPMV = PMVID
    dummycolor,dummystat = colorAssign(ptsPMV)
    dummypers = []
    for item in dummystat:
        value = round(item/totalhour*100,1)
        dummypers.append(value)
    statdict[ptsID] = dummypers

#print(statdict.keys())
print(statdict)

PMV_plotlyScatter(colorPMV,xvalues,yvalues,stat)
#PMV_BarStatALL(statdict,statname,statcolor)
#PMV_BarStatID(pers,statname,statcolor,pickedID)
#PMV_3DStatScatter(statdict,comfortpts)
