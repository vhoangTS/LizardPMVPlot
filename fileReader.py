import os
import plotly as py
import plotly.graph_objs as go

b18file = 'c:\\Users\\vhoang\\Desktop\\_TEMP\Model\\BASIS\\BASIS.b18'
temperaturePRN = 'c:\\Users\\vhoang\\Desktop\\_TEMP\\Model\\BASIS\\Results\\temp_1h_Z1.prn'
comfortPRN = 'c:\\Users\\vhoang\\Desktop\\_TEMP\\Model\\BASIS\\Results\\Comfort_1h.prn'

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
    for item in hours:
        dummyY = (item-1) % 24 + 1
        Yvalue.append(dummyY)
        dummyX = (item-1)//24 +1
        Xvalue.append(dummyX)
    return Xvalue,Yvalue

def colorAssign(PMV):
    '''assigining color values based on PMV'''
    color = []
    for item in PMV:
        if item == "":
            color.append(color_Unoccupied)
        else:
            if item < -3:
                dummycolor = color_ExtremeCold
            elif item >= -3 and item < -1.5:
                dummycolor = color_Cold
            elif item >= -1.5 and item < -0.5:
                dummycolor = color_SlightlyCold
            elif item >= -0.5 and item <= 0.5:
                dummycolor = color_Comfortable
            elif item > 0.5 and item <= 1.5:
                 dummycolor = color_SlightlyWarm
            elif item > 1.5 and item <= 3:
                dummycolor = color_Hot
            elif item > 3:
                dummycolor = color_ExtremeHot
            color.append(dummycolor)
    return color

color_Unoccupied = 'rgb(137,137,137)'
color_ExtremeCold = 'rgb(74,0,255)'
color_Cold = 'rgb(0,80,255)'
color_SlightlyCold = 'rgb(0,196,255)'
color_Comfortable = 'rgb(0,255,0)'
color_SlightlyWarm = 'rgb(255,190,0)'
color_Hot = 'rgb(255,54,0)'
color_ExtremeHot = 'rgb(255,255,0'

comfortpts = Readb18(b18file)
hours, occupation = ReadTemperature(temperaturePRN)
comfortdict = ReadComfort(comfortPRN) #{ID:8760 values}
#pick out 1 pts to make graph based on ptsID
pickedID = 1
Occufilter = 1
PMV = comfortdict[pickedID] #wholeyear
if Occufilter:
    PMVresult = ComfortOcc(PMV,occupation) #filtered
else:
    PMVresult = PMV

colorPMV = colorAssign(PMVresult)
xvalues,yvalues= getXY(hours)

#plotting
trace1 = go.Scatter(
    x = xvalues,
    y= yvalues,
    mode='markers',
    marker=dict(
        size='6',
        color = colorPMV, #set color equal to a variable
        showscale=True
    )
)

data = [trace1]

py.offline.plot(data, filename='basic-heatmap.html')
