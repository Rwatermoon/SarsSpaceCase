
class CaseItem:

    def __init__(self,earthStationList,sysName,lat,lon,alt,beamWidth):
        self.earthStationList=earthStationList
        self.sysName=sysName
        self.lat=lat
        self.lon=lon
        self.alt=alt
        self.beamWidth=beamWidth



    # <Object clsid = "GEO">
    #     <Name>Inmarsat4</Name>
    #     <Latitude>0.0</Latitude>  /=0
    #     <Longitude>143.5</Longitude> /=轨道位置(station栏的nominal orbital longitude)
    #     <Altitude>35786.055</Altitude>  /=35786.055
		# <Beamwidth_in_deg>5</Beamwidth_in_deg>  /暂无
		# <GainFile>GainReduction5.0.pattern</GainFile>
    # </Object>
class earthStationItem:
    def __init__(self,siteName,siteLat,siteLon,siteAlt,siteBeamWidth,polarType,linkList,groupID):
        self.siteName=siteName
        self.siteLat=siteLat
        self.siteLon=siteLon
        self.siteAlt=siteAlt
        self.siteBeamWidth=siteBeamWidth
        self.polarType=polarType
        self.linkList=linkList
        self.groupID=groupID
    # <Object clsid = "EarthStation">  /inmarsat GEO 地面站
    #     <Name>class3</Name>
    #     <Latitude>15</Latitude>
    #     <Longitude>150.0</Longitude>
    #     <Altitude>0.0</Altitude>
		# <Beamwidth_in_deg>72</Beamwidth_in_deg>
		# <GainFile>GainReduction72.0.pattern</GainFile>
    # </Object>
class linkStationItem:
    def __init__(self,linkName,networkName,Txeirp_in_dbw,Bandwidth_in_mhz,OverlapBw_in_mhz
                 ,RxstationName,Rxfreq_in_mhz,Rxgain_in_db,Rxtemperature_in_kevin,Rxgt_in_dbk
                 ,Pol_seperation_in_db,Otherloss_in_db,linkID):
        self.linkName=linkName
        self.networkName=networkName
        self.Txeirp_in_dbw=Txeirp_in_dbw
        self.Bandwidth_in_mhz=Bandwidth_in_mhz
        self.OverlapBw_in_mhz=OverlapBw_in_mhz
        self.RxstationName=RxstationName
        self.Rxfreq_in_mhz=Rxfreq_in_mhz
        self.Rxgain_in_db=Rxgain_in_db
        self.Rxtemperature_in_kevin=Rxtemperature_in_kevin
        self.Rxgt_in_dbk=Rxgt_in_dbk
        self.Pol_seperation_in_db=Pol_seperation_in_db
        self.Otherloss_in_db=Otherloss_in_db
        self.linkID=linkID

    # <Object clsid = "Link">
    #     <Name>"Inmarsat4-class1</Name>  /=network+class x
    #     <Txstation>Inmarsat4</Txstation>  /=network name
    #     <Txeirp_in_dbw>35.0</Txeirp_in_dbw>  /=Beam栏中B3a1+Emission栏中的C8c1
    #     <Bandwidth_in_mhz>0.180</Bandwidth_in_mhz>  /载波带宽，一个带宽对应一个link，Emission栏C7a
		# <OverlapBw_in_mhz>0.180</OverlapBw_in_mhz>  /同上
		# <Rxstation>class1</Rxstation>
		# <Rxfreq_in_mhz>1534.0</Rxfreq_in_mhz>  /Frequency栏,需注意GROUP ID
		# <Rxgain_in_db>16.5</Rxgain_in_db>   /assoc earth station栏C10d3(maximum isotropic gain)
		# <Rxtemperature_in_kevin>317</Rxtemperature_in_kevin>  /assoc earth station栏C10d6(Receiving system noise temperature)
		# <Rxgt_in_dbk>-8.5</Rxgt_in_dbk>   /=Rxgain_in_db-10log（Rxtemperature_in_kevin）
		# <Pol_seperation_in_db>13.0</Pol_seperation_in_db>  /与group栏中C6项对比，若为CR，则取13；若为H/;
		# <Otherloss_in_db>0.0</Otherloss_in_db>
    # </Object>