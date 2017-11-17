import plotly as py
import plotly.graph_objs as go

color_Unoccupied = 'rgb(220,220,220)'
color_ExtremeCold = 'rgb(74,0,255)'
color_Cold = 'rgb(0,80,255)'
color_SlightlyCold,color_Below5 = 'rgb(0,196,255)','rgb(0,196,255)'
color_Comfortable,color_5to10 = 'rgb(0,255,0)','rgb(0,255,0)'
color_SlightlyWarm, color_10to25 = 'rgb(255,190,0)','rgb(255,190,0)'
color_Hot,color_25to75 = 'rgb(255,54,0)','rgb(255,54,0)'
color_ExtremeHot,color_75to100 = 'rgb(255,255,0)','rgb(255,255,0)'

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

def PMV_plotlyScatter(colorPMV,xvalues,yvalues,stat,IDname,image):
    """Plotting yearly comfort values"""
    Unoccupied = traceseries(colorPMV,xvalues,yvalues,color_Unoccupied,"Unoccupied")
    ExtremeCold = traceseries(colorPMV,xvalues,yvalues,color_ExtremeCold,"Cold: %d hrs"%(stat[0]))
    Cold = traceseries(colorPMV,xvalues,yvalues,color_Cold,"Cool: %d hrs"%(stat[1]))
    SlightlyCold = traceseries(colorPMV,xvalues,yvalues,color_SlightlyCold,"Slightly Cool: %d hrs"%(stat[2]))
    Comfortable = traceseries(colorPMV,xvalues,yvalues,color_Comfortable,"Comfortable: %d hrs"%(stat[3]))
    SlightlyWarm = traceseries(colorPMV,xvalues,yvalues,color_SlightlyWarm,"Slightly Warm: %d hrs"%(stat[4]))
    Hot = traceseries(colorPMV,xvalues,yvalues,color_Hot,"Warm: %d hrs"%(stat[5]))
    ExtremeHot = traceseries(colorPMV,xvalues,yvalues,color_ExtremeHot,"Hot: %d hrs"%(stat[6]))

    data = [ExtremeHot,Hot,SlightlyWarm,Comfortable,SlightlyCold,Cold,ExtremeCold,Unoccupied]
    layout = go.Layout(
        width= 1900,height = 330,
        title = "Predicted Mean Vote (PMV)",
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
    if image == 0:
        py.offline.plot(fig, filename='PMV_%s.html'%(IDname))
    elif image == 1:
        py.offline.plot(fig, filename='PMV_%s.html'%(IDname),image="png",image_filename="image_PMV_%s"%(IDname),image_width=1900,image_height=330)

def PPD_plotlyScatter(colorPPD,xvalues,yvalues,stat,IDname,image):
    """Plotting yearly PPD values"""
    Unoccupied = traceseries(colorPPD,xvalues,yvalues,color_Unoccupied,"Unoccupied")
    Below5 = traceseries(colorPPD,xvalues,yvalues,color_Below5,"0-5 PPD: %d hrs"%(stat[0]))
    F5to10 = traceseries(colorPPD,xvalues,yvalues,color_5to10,"5-10 PPD: %d hrs"%(stat[1]))
    F10to25 = traceseries(colorPPD,xvalues,yvalues,color_10to25,"10-25 PPD: %d hrs"%(stat[2]))
    F25to75 = traceseries(colorPPD,xvalues,yvalues,color_25to75,"25-75 PPD: %d hrs"%(stat[3]))
    F75to100 = traceseries(colorPPD,xvalues,yvalues,color_75to100,"75-100 PPD: %d hrs"%(stat[4]))

    data = [Below5,F5to10,F10to25,F25to75,F75to100,Unoccupied]
    layout = go.Layout(
        width= 1900,height = 330,
        title = "Predicted Percentage of Dissatisfied (PPD)",
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
    if image == 0:
        py.offline.plot(fig, filename='PPD_%s.html'%(IDname))
    elif image == 1:
        py.offline.plot(fig, filename='PPD_%s.html'%(IDname),image="png",image_filename="image_PPD_%s"%(IDname),image_width=1900,image_height=330)
