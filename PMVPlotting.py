import plotly as py
import plotly.graph_objs as go

color_Unoccupied = 'rgb(220,220,220)'
color_ExtremeCold = 'rgb(74,0,255)'
color_Cold = 'rgb(0,80,255)'
color_SlightlyCold = 'rgb(0,196,255)'
color_Comfortable = 'rgb(0,255,0)'
color_SlightlyWarm = 'rgb(255,190,0)'
color_Hot = 'rgb(255,54,0)'
color_ExtremeHot = 'rgb(255,255,0)'

def traceseries(colorPMV,xvalues,yvalues,matchcolor,name):
    '''divided the color list to different list to use as different traces'''
    matchX = []
    matchY = []
    for id,color in enumerate(colorPMV):
        if color == matchcolor:
            matchX.append(xvalues[id])
            matchY.append(yvalues[id])
    trace = go.Scatter(
            name = name,
            x = matchX,
            y= matchY,
            mode='markers',
            marker=dict(
            size='4',
            color = matchcolor, #set color equal to a variable
            showscale=False,
            line = dict(width = 0.3, color = matchcolor)
                        )
                    )
    return trace

def PMV_plotlyScatter(colorPMV,xvalues,yvalues,stat):
    Unoccupied = traceseries(colorPMV,xvalues,yvalues,color_Unoccupied,"Unoccupied")
    ExtremeCold = traceseries(colorPMV,xvalues,yvalues,color_ExtremeCold,"Extreme Cold: %d hrs"%(stat[0]))
    Cold = traceseries(colorPMV,xvalues,yvalues,color_Cold,"Cold: %d hrs"%(stat[1]))
    SlightlyCold = traceseries(colorPMV,xvalues,yvalues,color_SlightlyCold,"Slightly Cold: %d hrs"%(stat[2]))
    Comfortable = traceseries(colorPMV,xvalues,yvalues,color_Comfortable,"Comfortable: %d hrs"%(stat[3]))
    SlightlyWarm = traceseries(colorPMV,xvalues,yvalues,color_SlightlyWarm,"Slightly Warm: %d hrs"%(stat[4]))
    Hot = traceseries(colorPMV,xvalues,yvalues,color_Hot,"Hot: %d hrs"%(stat[5]))
    ExtremeHot = traceseries(colorPMV,xvalues,yvalues,color_ExtremeHot,"Extreme Hot: %d hrs"%(stat[6]))

    data = [ExtremeHot,Hot,SlightlyWarm,Comfortable,SlightlyCold,Cold,ExtremeCold,Unoccupied]
    layout = go.Layout(
        width= 1900,height = 330,
        title = "Hourly Comfort",
        xaxis = dict(
            zeroline = False,
            showline = False,
            showgrid = False,
            tick0 = 0,
            dtick = "M1",
            tickformat = "%b",
            ticklen = 3,
            tickwidth = 1,
            ),
        yaxis = dict(
            autotick = False,
            showgrid = False,
            zeroline = False,
            showline = False,
            ticks = 'outside',
            tick0 = 0,
            dtick = 8,
            ticklen = 0,
            tickwidth = 1,
            tickcolor = '#000'
        )
        )

    fig = go.Figure(data = data, layout= layout)
    py.offline.plot(fig, filename='Yearly_PMV_ptsID.html')

def PMV_BarStatID(pers,statname,statcolor,pickedID):
    def stattrace(pickedID,statvalue,color,name):
        trace = go.Bar(
            x= [pickedID],
            y= [statvalue],
            name= name,
            width = [0.1],
            text = name,
            marker = dict(color = color),
            )
        return trace
    excold = stattrace(pickedID,pers[0],statcolor[0],statname[0])
    cold = stattrace(pickedID,pers[1],statcolor[1],statname[1])
    slcold = stattrace(pickedID,pers[2],statcolor[2],statname[2])
    comf = stattrace(pickedID,pers[3],statcolor[3],statname[3])
    slwarm = stattrace(pickedID,pers[4],statcolor[4],statname[4])
    hot = stattrace(pickedID,pers[5],statcolor[5],statname[5])
    exhot = stattrace(pickedID,pers[6],statcolor[6],statname[6])
    data = [excold,cold,slcold,comf,slwarm,hot,exhot]
    layout = go.Layout(barmode = 'stack',title='PMV Statistic on C%s'%(str(pickedID)),width= 1920,height = 1080)
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename='PMV_Stat_PtsID.html')

def PMV_BarStatALL(statdict,statname,statcolor):
    def traceassign(statdict,statname,nameID):
        xtrace = []
        ytrace = []
        for key in statdict.keys():
            xtrace.append(key)
            ytrace.append(statdict[key][nameID])
        trace = go.Bar(
            x= xtrace,
            y= ytrace,
            #width = [0.1],
            name= statname[nameID],
            marker = dict(color = statcolor[nameID]))
        return trace
    excold = traceassign(statdict,statname,0)
    cold = traceassign(statdict,statname,1)
    slcold = traceassign(statdict,statname,2)
    comf =  traceassign(statdict,statname,3)
    slwarm =  traceassign(statdict,statname,4)
    hot =  traceassign(statdict,statname,5)
    exhot =  traceassign(statdict,statname,6)
    data = [excold,cold,slcold,comf,slwarm,hot,exhot]
    layout = go.Layout(
                    barmode = 'stack',
                    title='PMV Statistic',
                    width= 1920,height = 1080)
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename='PMV_Stat_All.html')
