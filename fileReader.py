import os
from PMVPlotting import *
import plotly as py
import plotly.graph_objs as go
import datetime


def checkfile(b18, tempPRN, comfPRN):
    if not os.path.isfile(b18):
        print("Building file *.b18 not found!")
    if not os.path.isfile(tempPRN):
        print("Temperature file *.prn not found!")
    if not os.path.isfile(comfPRN):
        print("Comfort file *.prn not found!")


# checkfile(b18file, temperaturePRN, comfortPRN)


def Readb18(b18file):
    """returns comfort pts dictionary {ID:[X,Y,Z]}"""
    geoposdict = {}
    b18 = open(b18file, "r")
    lines = b18.readlines()
    for line in lines:
        if "cgeopos" in line:
            newline = line.split()
            ptsid = int(newline[1])
            ptsX, ptsY, ptsZ = float(newline[2]), float(newline[3]), float(newline[4])
            pts = []
            pts.append(ptsX), pts.append(ptsY), pts.append(ptsZ)
            geoposdict[ptsid] = pts
    b18.close()
    return geoposdict


def ReadTemperature(temperaturePRN):
    """return occupation schedule"""
    occu = []
    hour = []
    temp = open(temperaturePRN, "r")
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
    comf = open(comfortPRN, "r")
    lines = comf.readlines()
    lines.pop(0)
    lines.pop(0)
    # setting up blank dictionary
    dummyl = lines[0].split()
    dummyl.pop(0)
    for iid in range(len(dummyl)):
        key = iid + 1
        comfort[key] = []
    for line in lines:
        line = line.split()
        try:
            line.pop(0)
            for iid, lvalue in enumerate(line):
                dkey = int(iid) + 1
                comfort[dkey].append(float(lvalue))
        except:
            break
    comf.close()
    return comfort


def ComfortOcc(PMV, occupation):
    """return PMV values only during occupation time"""
    PMVOcc = []
    for iid, ovalue in enumerate(occupation):
        if ovalue == 0:
            PMVOcc.append("")
        else:
            PMVOcc.append(PMV[iid])
    return PMVOcc


def getXY(hours):
    """for plotting"""
    xvalue = []
    yvalue = []
    year = datetime.date.today().year
    for hrs in hours:
        dummyy = (hrs - 1) % 24 + 1
        yvalue.append(dummyy)
        dummyx = (hrs - 1) // 24 + 1
        todate = datetime.date(year, 1, 1) + datetime.timedelta(dummyx - 1)
        xvalue.append(todate)
    return xvalue, yvalue


def colorAssign(PMV):
    """assigining color values based on PMV"""
    color = []
    pmvstat = []
    c_excold, c_cold, c_slcold, c_comf, c_slwarm, c_hot, c_exhot = 0, 0, 0, 0, 0, 0, 0
    for values in PMV:
        if values == "":
            color.append(color_Unoccupied)
            # c_unocc += 1
        else:
            dcolor = ''
            if values < -3:
                dcolor = color_ExtremeCold
                c_excold += 1
            elif -3 <= values < -1.5:
                dcolor = color_Cold
                c_cold += 1
            elif -1.5 <= values < -0.5:
                dcolor = color_SlightlyCold
                c_slcold += 1
            elif -0.5 <= values <= 0.5:
                dcolor = color_Comfortable
                c_comf += 1
            elif 0.5 < values <= 1.5:
                dcolor = color_SlightlyWarm
                c_slwarm += 1
            elif 1.5 < values <= 3:
                dcolor = color_Hot
                c_hot += 1
            elif values > 3:
                dcolor = color_ExtremeHot
                c_exhot += 1
            color.append(dcolor)
    pmvstat.append(c_excold), pmvstat.append(c_cold), pmvstat.append(c_slcold), pmvstat.append(c_comf), pmvstat.append(
        c_slwarm), pmvstat.append(c_hot), pmvstat.append(c_exhot)
    return color, pmvstat


color_Unoccupied = 'rgb(233,233,233)'
color_ExtremeCold = 'rgb(0,0,255)'
color_Cold = 'rgb(47,141,255)'
color_SlightlyCold = 'rgb(110,255,255)'
color_Comfortable = 'rgb(144,245,0)'
color_SlightlyWarm = 'rgb(255,204,0)'
color_Hot = 'rgb(255,111,71)'
color_ExtremeHot = 'rgb(255,0,0)'
statname = ['Extreme Cold', 'Cold', 'Slightly Cold', 'Comfortable', 'Slightly Warm', 'Hot', 'Extreme Hot']
statcolor = ['rgb(74,0,255)', 'rgb(0,80,255)', 'rgb(0,196,255)', 'rgb(0,255,0)', 'rgb(255,190,0)', 'rgb(255,54,0)',
             'rgb(255,255,0']


# if working from office, use this path
b18lst = []
tempPRNlst = []
comfPRNlst = []

modelPath = "p:\\_Akquise\\Stuttgart_KnippersHelbig\\TRNLizSim\\Model\\"
variants = ["V0_Basic", "V1_Shading", "V2_Screed", "V3_ShadingAndScreed", "V4_ShadingAndScreedAndFan"]

for vname in variants:
    b18lst.append(os.path.join(modelPath, vname, "%s.b18" % vname))
    tempPRNlst.append(os.path.join(modelPath, vname, "Results\\temp_1h_A1.prn"))
    comfPRNlst.append(os.path.join(modelPath, vname, "Results\\Comfort_1h.prn"))
pickedID = 1
Occufilter = 1  # occupation filter signal

for iid, var in enumerate(variants):
    b18file = b18lst[iid]
    temperaturePRN = tempPRNlst[iid]
    comfortPRN = comfPRNlst[iid]
    comfortpts = Readb18(b18file)
    hours, occupation = ReadTemperature(temperaturePRN)
    comfortdict = ReadComfort(comfortPRN)  # {ID:8760 values}
    PMV = comfortdict[pickedID]  # wholeyear for selected pts
    if Occufilter:
        PMVresult = ComfortOcc(PMV, occupation)  # filtered
    else:
        PMVresult = PMV
    colorPMV, stat = colorAssign(PMVresult)
    xvalues, yvalues = getXY(hours)
    # get statistic for 1 pts
    totalhour = sum(occupation) if Occufilter else 8760
    pers = []
    for item in stat:
        dummy = round(item / totalhour * 100, 1)
        pers.append(dummy)
    # get statistic for all the points
    statdict = {}  # {ptsID: [statistic1,statistic2,...]}
    for ptsID in range(1, len(comfortpts) + 1):
        PMVID = comfortdict[ptsID]
        if Occufilter:
            ptsPMV = ComfortOcc(PMVID, occupation)  # filtered
        else:
            ptsPMV = PMVID
        dummycolor, dummystat = colorAssign(ptsPMV)
        dummypers = []
        for item in dummystat:
            value = round(item / totalhour * 100, 1)
            dummypers.append(value)
        statdict[ptsID] = dummypers

    PMV_plotlyScatter(var, colorPMV, xvalues, yvalues, stat, pickedID)
    # PMV_BarStatALL(statdict,statname,statcolor)
    # PMV_BarStatID(pers,statname,statcolor,pickedID)
    # PMV_3DStatScatter(statdict,comfortpts)
