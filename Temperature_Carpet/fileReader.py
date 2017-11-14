import os
from TempPlotting import *
import plotly as py
import plotly.graph_objs as go
import datetime

tPRN_A1_07 = 'p:\\Walldorf_SAP_170123\\Sim_Thermal\\20171115_SAP_update\\PLOTS\\RESULTS\\REAL_V980ACT\\Results\\temp_1h_Z1.prn'
tPRN_A1_13 = 'p:\\Walldorf_SAP_170123\\Sim_Thermal\\20171115_SAP_update\\PLOTS\\RESULTS\\REAL_V980ACT\\Results\\temp_1h_Z2.prn'
tPRN_A2_19_V0 = 'p:\\Walldorf_SAP_170123\\Sim_Thermal\\20171115_SAP_update\\PLOTS\\RESULTS\\V0_01\\Results\\temp_1h_Z1.prn'
tPRN_A2_19_V1 = 'p:\\Walldorf_SAP_170123\\Sim_Thermal\\20171115_SAP_update\\PLOTS\\RESULTS\\V1_SIA\\Results\\temp_1h_Z1.prn'
tPRN_C3_17 = 'p:\\Walldorf_SAP_170123\\Sim_Thermal\\20171115_SAP_update\\PLOTS\\RESULTS\\V5_SV2_MEET\\Results\\temp_1h_MEET.prn'

tempPRNs = [tPRN_A1_07,tPRN_A1_13,tPRN_A2_19_V0,tPRN_A2_19_V1,tPRN_C3_17]
namePRNs = ["A1_07","A1_13","A2_19_V0","A2_19_V1","C3_17"]

def PlotTempPRN(temperaturePRN,AirnodeName):
    def ReadTemperature(temperaturePRN):
        '''return occupation schedule'''
        occu = []
        hour = []
        Atop = []
        temp = open(temperaturePRN,"r")
        lines = temp.readlines()
        lines.pop(0)
        line0 = lines[0].split()
        for id,value in enumerate(line0):
            if "ATop_" in value:
                idloc = id

        lines.pop(0)
        for line in lines:
            line = line.split()
            try:
                Atop.append(float(line[idloc]))
                hour.append(int(float(line[0])))
                occu.append(int(float(line[1])))
            except:
                break
        temp.close()
        #print(Atop)
        return hour, occu, Atop

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

    def colorAssign(ATop):
        '''assigining color values based on ATop'''
        color = []
        stat = []
        c_below20, c_2022, c_2224, c_2426, c_above26= 0,0,0,0,0
        for item in ATop:
            if item == 0:
                color.append(color_unoccupied)
            else:
                if item < 20:
                    dummycolor = color_below20
                    c_below20 += 1
                elif item >= 20 and item < 22:
                    dummycolor = color_2022
                    c_2022 += 1
                elif item >= 22 and item <= 24:
                    dummycolor = color_2224
                    c_2224 += 1
                elif item > 24 and item <= 26:
                    dummycolor = color_2426
                    c_2426 += 1
                elif item > 26:
                     dummycolor = color_above26
                     c_above26 += 1
                color.append(dummycolor)
        stat.append(c_below20),stat.append(c_2022),stat.append(c_2224),stat.append(c_2426),stat.append(c_above26)
        return color, stat

    color_unoccupied = 'rgb(220,220,220)'
    color_below20 = 'rgb(0,80,255)'
    color_2022 = 'rgb(0,196,255)'
    color_2224 = 'rgb(0,255,0)'
    color_2426 = 'rgb(255,190,0)'
    color_above26 = 'rgb(255,54,0)'

    statname = ['below20', '20-22', '22-24', '24-26','above26']
    statcolor = ['rgb(0,80,255)','rgb(0,196,255)','rgb(0,255,0)','rgb(255,190,0)','rgb(255,54,0)']

    hours, occupation, ATop = ReadTemperature(temperaturePRN)
    colorATop,stat = colorAssign(ATop)
    xvalues,yvalues= getXY(hours)

    #get statistic for 1 pts
    totalhour = sum(occupation)

    pers = []
    for item in stat:
        dummy = round(item/totalhour*100,1)
        pers.append(dummy)

    #print(statdict)
    PMV_plotlyScatter(colorATop,xvalues,yvalues,stat,AirnodeName)

for id,item in enumerate(tempPRNs):
    PlotTempPRN(item,namePRNs[id])
