
# this is the user struct

dictDataType = {
    'TYPE_BJANC' : 0,
    'TYPE_LAPS_HIGH':1,
    'TYPE_LAPS_WIND' : 2,
    'TYPE_LAPS_SURFACE' : 3,
    'TYPE_LAPS_CLOUD' : 4,
    'TYPE_LAPS_Q' : 5,
    'TYPE_RADARBASE' : 6,
    'TYPE_RUC' : 7,
    'TYPE_SATELLITERETRIVAL' : 8,
    'TYPE_SCOUT_SCKY' : 9,
    'TYPE_BJANC_VDRAS' : 10,
    'TYPE_BJANC_VIPS' : 11,
    'TYPE_BJANC_MERGEDDBZ' : 12,
    'TYPE_BJRUC' : 13,
    'TYPE_SWAN_RADAR3DPT' : 14,
    'TYPE_SWAN_TITAN' : 15,
    'TYPE_SWAN_COTRECWIND' : 16  ,
    'TYPE_SWAN_RADARPUP' : 17,
    'TYPE_SWAN_CLOUD' : 18,
    'TYPE_SWAN_QPE' : 19,
    'TYPE_SWAN_QPF' : 20,
    'TYPE_SWAN_VWP' : 21,
    'TYPE_SWAN_STM' : 22,
    'TYPE_SWAN_LIGHTING' : 23,
    'TYPE_MICAPS4_DATA' : 24,
    'TYPE_MICAPS14_DATA' : 25    ,
    'TYPE_UNKNOWN' : 26
   }


    
def getdatatypedic():
    return dictDataType

class ScoutInfo:

    def __init__(self):
    
        "the scout dir info"
        self.scoutdir = ""
        self.scoutDataType = 14
        self.datetime = None
        self.listInitFile = []
        self.strSelfOutput = ""

if __name__ == "__main__":
    scoutinfo = ScoutInfo()
    
    print("hello",scoutinfo.scoutDataType)