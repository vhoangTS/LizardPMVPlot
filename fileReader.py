import os

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

def PMVsort


comfortpts = Readb18(b18file)
hours, occupation = ReadTemperature(temperaturePRN)
comfortdict = ReadComfort(comfortPRN)

pickedID = 1
PMV = comfortdict[pickedID]
