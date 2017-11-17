import os
from Func_PMVPlotting import *
import plotly as py
import plotly.graph_objs as go
import datetime
import glob,sys

#### PRNs input mode
mode = 1 # 0:manual - 1:automatic

#### AUTO SAVE IMAGES?
CreateImages = 0 #0:not auto save image - 1: autosave images

### PLOT ALL?
PlotAll = 1 #1: will plot everything, be careful
plotPMV,plotPPD = 1,1

timesig = "Time" #for getting time value 1-8760
Occufilter = 1 #0:show whole year - 1:show only during occupation

if mode == 0:
    #MANUAL MODE: inputing each PRN by yourself
    VAMTempPRN1 = 's:\\VuHoang\\__TRNLizard_is_Life\\_TRNLizard_dev\\_Supporting_Functions\\PyFunctions\\VAMPMVPlot\\temp_1h.prn'
    VAMTempPRN2 = 's:\\VuHoang\\__TRNLizard_is_Life\\_TRNLizard_dev\\_Supporting_Functions\\PyFunctions\\VAMPMVPlot\\temp_1h.prn'
    VAMPRNs = [VAMTempPRN1,VAMTempPRN2]
    tempsig = ["ATOP_BUE","ATOP_BUE"]
    comfortsig = ["PMVLW_C1","PMVLW_C1"]
    PPDsig = ["PPDLW_C1","PPDLW_C1"]
    varinantname = ["V1","V2"]
elif mode == 1:
    #AUTOMATIC: extract all temp_1h.PRN from massive VAM folder
    VAMPRNs,varinantname,tempsig,comfortsig,PPDsig = [],[],[],[],[]
    VAMFolder = "p:\\Budapest_Liget_150242\\Sim-Thermal\\171110_VAM_alpha_whole_building\\RES\\PROJECT_1\\IWEC20_BUDAPEST-PESTSZENTL_128430\\YEAR\\"
    for root,dirs,files in os.walk(VAMFolder):
        for file in files:
            if file.endswith("temp_1h.prn"):
                rname = root.split("\\")
                varinantname.append(rname[-1])
                VAMPRNs.append(os.path.join(root,file))
    for value in range(0,len(VAMPRNs)):
        tempsig.append("ATOP_BUE")
        comfortsig.append("PMVLW_C1")
        PPDsig.append("PPDLW_C1")

def checkfile(VAMPRNs):
    """Check if temp_1h.prn exist or not"""
    for path in VAMPRNs:
        if not os.path.isfile(path):
            print("File not found!")
            sys.exit()

def getID(line0,signal):
    """Get position of val"""
    line0 = line0.split()
    returnID = None
    for sID, item in enumerate(line0):
        if signal == item:
            returnID = sID
    return returnID

def ReadVAMTemp1h(VAMPRNfile,timesig,tempsig,comfortsig,PPDsig):
    '''return time, temperature, comfort'''
    occu,hour,pmv,ppd = [],[],[],[]
    temp = open(VAMPRNfile,"r")
    lines = temp.readlines()
    timeID = getID(lines[0],timesig)
    tempID = getID(lines[0],tempsig)
    pmvID = getID(lines[0],comfortsig)
    ppdID = getID(lines[0],PPDsig)
    lines.pop(0)
    lines.pop(0)
    for line in lines:
        line = line.split()
        try:
            hour.append(int(float(line[timeID])))
            if float(line[tempID]) == 0:
                occu.append(0)
            else:
                occu.append(1)
            pmv.append(float(line[pmvID]))
            ppd.append(float(line[ppdID]))
        except:
            break
    temp.close()
    return hour, occu, pmv, ppd

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

def PMVcolorAssign(PMV):
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
            elif item >= -3 and item < -2:
                dummycolor = color_Cold
                c_cold += 1
            elif item >= -2 and item < -1:
                dummycolor = color_SlightlyCold
                c_slcold += 1
            elif item >= -1 and item <= 1:
                dummycolor = color_Comfortable
                c_comf += 1
            elif item > 1 and item <= 2:
                 dummycolor = color_SlightlyWarm
                 c_slwarm += 1
            elif item > 2 and item <= 3:
                dummycolor = color_Hot
                c_hot += 1
            elif item > 3:
                dummycolor = color_ExtremeHot
                c_exhot += 1
            color.append(dummycolor)
    stat.append(c_excold),stat.append(c_cold),stat.append(c_slcold),stat.append(c_comf),stat.append(c_slwarm),stat.append(c_hot),stat.append(c_exhot)
    return color, stat

def PPDcolorAssign(PPD):
    '''assigining color values based on PPD'''
    color = []
    stat = []
    c_below5, c_5to10, c_10to25, c_25to75, c_75to100 = 0, 0, 0, 0, 0
    for item in PPD:
        if item == "":
            color.append(color_Unoccupied)
            #c_unocc += 1
        else:
            if item <= 5:
                dummycolor = color_Below5
                c_below5 += 1
            elif item > 5 and item <= 10:
                dummycolor = color_5to10
                c_5to10 += 1
            elif item >10 and item <= 25:
                dummycolor = color_10to25
                c_10to25 += 1
            elif item > 25 and item <= 75:
                dummycolor = color_25to75
                c_25to75 += 1
            elif item > 75 and item <= 100:
                 dummycolor = color_75to100
                 c_75to100 += 1
            color.append(dummycolor)
    stat.append(c_below5),stat.append(c_5to10),stat.append(c_10to25),stat.append(c_25to75),stat.append(c_75to100)
    return color, stat
checkfile(VAMPRNs)

def PlotVAMPRN(variantID):
    hour, occu, pmv,ppd = ReadVAMTemp1h(VAMPRNs[variantID],timesig,tempsig[variantID],comfortsig[variantID],PPDsig[variantID])
    pmvPlot,ppdPlot = [],[]
    if Occufilter == 1:
        for sid,item in enumerate(pmv):
            if occu[sid] == 0:
                pmvPlot.append("")
                ppdPlot.append("")
            else:
                pmvPlot.append(item)
                ppdPlot.append(ppd[sid])
    else:
        pmvPlot = pmv
        ppdPlot = ppd
    #print(ppdPlot)
    colorPMV,PMVstat = PMVcolorAssign(pmvPlot)
    colorPPD,PPDstat = PPDcolorAssign(ppdPlot)
    xvalues,yvalues= getXY(hour)

    #get statistic for 1 pts
    totalhour = sum(occu) if Occufilter else 8760

    pmvpers,ppdpers = [],[]
    for item in PMVstat:
        pmvdummy = round(item/totalhour*100,1)
        pmvpers.append(pmvdummy)
    for item in PPDstat:
        ppddummy = round(item/totalhour*100,1)
        ppdpers.append(ppddummy)
    if plotPMV == 1:
        PMV_plotlyScatter(colorPMV,xvalues,yvalues,PMVstat,varinantname[variantID],CreateImages)
    if plotPPD == 1:
        PPD_plotlyScatter(colorPPD,xvalues,yvalues,PPDstat,varinantname[variantID],CreateImages)

#PlotVAMPRN(0)

if PlotAll:
    for vID in range(0,len(VAMPRNs)):
        PlotVAMPRN(vID)
