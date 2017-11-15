import plotly as py
import plotly.graph_objs as go

#default color scale
color_unoccupied = 'rgb(220,220,220)'
color_below20 = 'rgb(0,80,255)'
color_2022 = 'rgb(0,196,255)'
color_2224 = 'rgb(0,255,0)'
color_2426 = 'rgb(255,190,0)'
color_above26 = 'rgb(255,54,0)'

def traceseries(colorATop,xvalues,yvalues,matchcolor,name):
    '''divided the color list to different list to use as different traces'''
    matchX = []
    matchY = []
    for id,color in enumerate(colorATop):
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

def PMV_plotlyScatter(colorATop,xvalues,yvalues,stat,AirnodeName):
    """Plotting yearly comfort values"""
    Unoccupied = traceseries(colorATop,xvalues,yvalues,color_unoccupied,"Unoccupied")
    Below20 = traceseries(colorATop,xvalues,yvalues,color_below20,"Below 20°C: %d hrs"%(stat[0]))
    Between2022 = traceseries(colorATop,xvalues,yvalues,color_2022,"20°C-22°C: %d hrs"%(stat[1]))
    Between2224 = traceseries(colorATop,xvalues,yvalues,color_2224,"22°C-24°C: %d hrs"%(stat[2]))
    Between2426 = traceseries(colorATop,xvalues,yvalues,color_2426,"24°C-26°C: %d hrs"%(stat[3]))
    Above26 = traceseries(colorATop,xvalues,yvalues,color_above26,"Above 26°C: %d hrs"%(stat[4]))

    data = [Above26,Between2426,Between2224,Between2022,Below20,Unoccupied]
    layout = go.Layout(
        width= 1900,height = 330,
        title = "Hourly Comfort",
        xaxis = dict(
            #fixedrange = True,
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
            #fixedrange = True,
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
    py.offline.plot(fig, filename='%s.html'%(AirnodeName), image_filename="%s"%(AirnodeName), image_width=19000,image_height=3300) #image = 'png',
