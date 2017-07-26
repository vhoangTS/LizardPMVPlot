import plotly as py
import plotly.graph_objs as go

color_Unoccupied = 'rgb(137,137,137)'
color_ExtremeCold = 'rgb(74,0,255)'
color_Cold = 'rgb(0,80,255)'
color_SlightlyCold = 'rgb(0,196,255)'
color_Comfortable = 'rgb(0,255,0)'
color_SlightlyWarm = 'rgb(255,190,0)'
color_Hot = 'rgb(255,54,0)'
color_ExtremeHot = 'rgb(255,255,0'

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
            size='6',
            color = matchcolor, #set color equal to a variable
            showscale=False,
            line = dict(width = 1,)

                        )
                    )
    return trace

def PMV_plotlyScatter(colorPMV,xvalues,yvalues):
    Unoccupied = traceseries(colorPMV,xvalues,yvalues,color_Unoccupied,"Unoccupied")
    ExtremeCold = traceseries(colorPMV,xvalues,yvalues,color_ExtremeCold,"Extreme Cold")
    Cold = traceseries(colorPMV,xvalues,yvalues,color_Cold,"Cold")
    SlightlyCold = traceseries(colorPMV,xvalues,yvalues,color_SlightlyCold,"Slightly Cold")
    Comfortable = traceseries(colorPMV,xvalues,yvalues,color_Comfortable,"Comfortable")
    SlightlyWarm = traceseries(colorPMV,xvalues,yvalues,color_SlightlyWarm,"Slightly Warm")
    Hot = traceseries(colorPMV,xvalues,yvalues,color_Hot,"Hot")
    ExtremeHot = traceseries(colorPMV,xvalues,yvalues,color_ExtremeHot,"Extreme Hot")

    data = [ExtremeHot,Hot,SlightlyWarm,Comfortable,SlightlyCold,Cold,ExtremeCold,Unoccupied]
    layout = go.Layout(
        xaxis = dict(
            autotick = False,
            ticks = 'outside',
            tick0 = 0,
            dtick = 36.5,
            ticklen = 1,
            tickwidth = 1,
            tickcolor = '#000'),
        yaxis = dict(
            autotick = False,
            ticks = 'outside',
            tick0 = 0,
            dtick = 8,
            ticklen = 1,
            tickwidth = 1,
            tickcolor = '#000'
        )
        )

    fig = go.Figure(data = data, layout= layout)
    py.offline.plot(fig, filename='basic-scatter.html')

def PMV_BarStat(pers,statname,statcolor,pickedID):
    def stattrace(pickedID,statvalue,color,name):
        trace = go.Bar(
            x= pickedID,
            y= statvalue,
            name= name,
            text = name,
            marker = dict(color = color),
            )
        return trace
    excold = stattrace(pickedID,pers[0],statcolor[0],statname[0])
    cold = stattrace(pickedID,pers[1],statcolor[1],statname[1])
    slcold = stattrace(pickedID,pers[2],statcolor[2],statname[2])
    data = [excold,cold,slcold]
    layout = go.Layout(title='PMV Statistic on C%s'%(str(pickedID)),)
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename='basic-bar.html')
