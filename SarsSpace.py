import sqlite3,csv
from caseItem import *
from lxml import etree




# 输出CASEXML
def writeErrorInfo(filePath,systemName,GroupID,GroupName):
    with open(filePath, 'a+',newline='') as f:
        csvwriter=csv.writer(f,quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([systemName,GroupID,GroupName])
    f.closed

def writeXML(CaseData,rootPath):
    root = etree.Element("XMLCaseData",version="1.0")
    flag_group=0
    flag_link=0
    for eartheStation in CaseData.earthStationList:


        stationObject=etree.SubElement(root, "Object",clsid = "EarthStation")
        stationName=etree.SubElement(stationObject, "Name")
        stationName.text=str(eartheStation.siteName)
        stationName=etree.SubElement(stationObject, "Latitude")
        stationName.text=str(eartheStation.siteLat)
        stationName=etree.SubElement(stationObject, "Longitude")
        stationName.text=str(eartheStation.siteLon)
        stationName=etree.SubElement(stationObject, "Altitude")
        stationName.text=str(eartheStation.siteAlt)
        stationName=etree.SubElement(stationObject, "Beamwidth_in_deg")
        stationName.text=str(eartheStation.siteBeamWidth)
        stationName=etree.SubElement(stationObject, "GainFile")
        stationName.text=str("GainReduction26.pattern")
        stationName=etree.SubElement(stationObject, "GroupID")
        stationName.text=str(eartheStation.groupID)
        flag_group+=1

    GEOObject=etree.SubElement(root, "Object",clsid = "GEO")
    stationName=etree.SubElement(GEOObject, "Name")
    stationName.text=str(CaseData.sysName)
    stationName=etree.SubElement(GEOObject, "Latitude")
    stationName.text=str(0)
    stationName=etree.SubElement(GEOObject, "Longitude")
    stationName.text=str(CaseData.lon)
    stationName=etree.SubElement(GEOObject, "Altitude")
    stationName.text=str(35786.055)
    stationName=etree.SubElement(GEOObject, "Beamwidth_in_deg")
    stationName.text=str(5)
    stationName=etree.SubElement(GEOObject, "GainFile")
    stationName.text=str("GainReduction5.0.pattern")

    for eartheStation in CaseData.earthStationList:
        for link in eartheStation.linkList:
            linkObject=etree.SubElement(root, "Object",clsid = "Link")
            stationName=etree.SubElement(linkObject, "Name")
            stationName.text=str(link.linkName)
            stationName=etree.SubElement(linkObject, "Txstation")
            stationName.text=str(link.networkName)
            stationName=etree.SubElement(linkObject, "Txeirp_in_dbw")
            stationName.text=str(link.Txeirp_in_dbw)
            stationName=etree.SubElement(linkObject, "Bandwidth_in_mhz")
            stationName.text=str(link.Bandwidth_in_mhz)
            stationName=etree.SubElement(linkObject, "OverlapBw_in_mhz")
            stationName.text=str(link.OverlapBw_in_mhz)
            stationName=etree.SubElement(linkObject, "Rxstation")
            stationName.text=str(link.RxstationName)
            stationName=etree.SubElement(linkObject, "Rxfreq_in_mhz")
            stationName.text=str(link.Rxfreq_in_mhz)
            stationName=etree.SubElement(linkObject, "Rxgain_in_db")
            stationName.text=str(link.Rxgain_in_db)
            stationName=etree.SubElement(linkObject, "Rxtemperature_in_kevin")
            stationName.text=str(link.Rxtemperature_in_kevin)
            stationName=etree.SubElement(linkObject, "Rxgt_in_dbk")
            stationName.text=str(link.Rxgt_in_dbk)
            stationName=etree.SubElement(linkObject, "Pol_seperation_in_db")
            stationName.text=str(link.Pol_seperation_in_db)
            stationName=etree.SubElement(linkObject, "Otherloss_in_db")
            stationName.text=str(link.Otherloss_in_db)
            stationName=etree.SubElement(linkObject, "GroupID")
            stationName.text=str(eartheStation.groupID)
            flag_link+=1

    et=etree.ElementTree(root)
    et.write(rootPath+CaseData.sysName+'.case',xml_declaration=True,pretty_print=True)

# 转化Emission designation为Float
def valBandwidth(bandwidth,bwlist):
    if 'N0N' in str(bandwidth):
        return False
    if str(bandwidth)[:4] not in bwlist:
        bwlist.append(str(bandwidth)[:4])
    else:
        return False
    par=1

    if 'K' in str(bandwidth)[0:4]:par=par/1000.0
    if 'G' in str(bandwidth)[0:4]:par=par*1000
    charList=['K','M','G']
    value=str(bandwidth)[0:4]
    for char in charList:
        value=value.replace(char,'.')
    return float(value)*par

if __name__ == '__main__':
    # 数据库使用第三方软件转为Sqlite的db格式
    conn=sqlite3.connect(r"H:\BRSpace\srs2825\srs2825.db")
    # 输出根路径
    outPath=r"H:\BRSpace\result\\"
    # 剔除参数不全Group的名单
    error_log=r"H:\BRSpace\result\error_log.csv"

    with open(error_log, 'w') as f:
        csvwriter=csv.writer(f,quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["systemName","GroupID","GroupName"])
        print("initialization logfile")
    f.closed

    cur=conn.cursor()
    # 根据Inmarsat筛选系统
    allSYSItem=cur.execute("SELECT * FROM main.com_el WHERE main.com_el.sat_name "
                           "LIKE '%Inmarsat%' AND main.com_el.prov <> 'RS49'").fetchall()#92500070
    # 遍历系统
    for item in  allSYSItem:

        allSYSKey=item[0]
        earthStationList=[]
        sysName=item[12]
        lat=0
        lon=item[14]
        alt=35786.055
        beamWidth=5.0

        sysCase=CaseItem(earthStationList,sysName,lat,lon,alt,beamWidth)
        # get group ID
        groupItemList=cur.execute("SELECT * FROM main.grp WHERE main.grp.ntc_id ='%d'"
                                 "AND  main.grp.emi_rcp = 'E'"
                                 "AND main.grp.freq_min >= 1518 AND main.grp.freq_max <= 1559"% allSYSKey).fetchall()
        # 遍历Group

        latIndex=0
        # 判断LatIndex是否两次超过60
        latFlat=False
        for groupItem in groupItemList:

            groupGain=groupItem[3]
            groupKey=groupItem[0]#92602901
            e_as_stn_Item=cur.execute("SELECT stn_name,noise_t,bmwdth,gain FROM main.e_as_stn "
                                 "WHERE main.e_as_stn.grp_id ='%d'"%groupKey).fetchone()
            if e_as_stn_Item == None:
                writeErrorInfo(error_log,str(sysCase.sysName),str(groupKey),"")
                continue
            emptyFlag=False
             # if any noise_t,bmwdth,gain is none skip this group and log it
            for item in e_as_stn_Item[1:]:
                if item == None:
                    emptyFlag=True
                    writeErrorInfo(error_log,str(sysCase.sysName),str(groupKey),str(e_as_stn_Item[0]))
            if emptyFlag:continue

            polarType=cur.execute("SELECT polar_type FROM main.grp "
                                 "WHERE main.grp.grp_id ='%d'"%groupKey).fetchone()[0]
            siteName=e_as_stn_Item[0] #if e_as_stn_Item[0]!=None else ""
            maxgain_group=e_as_stn_Item[3] #if e_as_stn_Item[3]!=None else None
            if latIndex>60:
                if latFlat:
                    latIndex=0.5
                else:
                    latIndex=1
                    latFlat=True
            siteLat=latIndex

            siteLon=sysCase.lon
            siteAlt=0
            siteBeamWidth="%.1f"%(e_as_stn_Item[2])
            # if e_as_stn_Item[2] ==None:
            #     otherBeamwidth=cur.execute("SELECT bmwdth FROM main.e_as_stn "
            #                                "WHERE stn_name = '%s' AND bmwdth is not NULL"%siteName).fetchone()
            #     if otherBeamwidth!= None:siteBeamWidth=otherBeamwidth[0]
            #     else:
            #         siteBeamWidth=None
            #         print(sysCase.sysName+','+siteName)
            #         flag+=1
            # else:
            #     siteBeamWidth="%.1f"%(e_as_stn_Item[2])

            linkList=[]
            groupCase=earthStationItem(siteName,siteLat,siteLon,siteAlt,siteBeamWidth,polarType,linkList,groupKey)


            linkKeyList=cur.execute("SELECT * FROM main.emiss WHERE main.emiss.grp_id ='%d'"%groupKey).fetchall()
            bwlist=[]
            # 遍历Group的emission
            for linkItem in linkKeyList:

                linkName=str(groupCase.siteName)+str(groupKey)
                networkName=str(sysCase.sysName)
                linkID=linkItem[0]
                pepGain=linkItem[3] if linkItem[5]==None else linkItem[5]


                maxGain=cur.execute("SELECT gain FROM main.s_beam "
                                    "WHERE main.s_beam.beam_name ='%s'"
                                    "AND main.s_beam.ntc_id='%s'"
                                    "AND main.s_beam.emi_rcp='E'"%(groupGain,allSYSKey)).fetchone()[0]

                Txeirp_in_dbw="%.2f"%(maxGain+pepGain)

                data_value=valBandwidth(linkItem[2],bwlist)
                if data_value==False:continue
                Bandwidth_in_mhz=data_value
                OverlapBw_in_mhz=data_value
                RxstationName=groupCase.siteName
                Rxfreq_in_mhz=cur.execute("SELECT freq_mhz FROM main.freq WHERE main.freq.grp_id ='%d'"%linkItem[0]).fetchone()[0]
                Rxgain_in_db=e_as_stn_Item[3]
                Rxtemperature_in_kevin=e_as_stn_Item[1]
                Rxgt_in_dbk=0
                Pol_seperation_in_db=groupCase.polarType
                if groupCase.polarType=='H' or 'L':Pol_seperation_in_db=3
                if groupCase.polarType=='CR' or None:Pol_seperation_in_db=13


                Otherloss_in_db=0.0
                LinkCase=linkStationItem(linkName,networkName,Txeirp_in_dbw,Bandwidth_in_mhz,OverlapBw_in_mhz
                 ,RxstationName,Rxfreq_in_mhz,Rxgain_in_db,Rxtemperature_in_kevin,Rxgt_in_dbk
                 ,Pol_seperation_in_db,Otherloss_in_db,linkID)



                groupCase.linkList.append(LinkCase)
            sysCase.earthStationList.append(groupCase)
            latIndex=latIndex+2

        writeXML(sysCase,outPath)

    print("Finish!")



