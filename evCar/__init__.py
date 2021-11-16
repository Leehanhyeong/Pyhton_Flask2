from flask import Flask
from flask_cors import CORS
import pandas as pd
from pandas import Series, DataFrame
import xml.etree.ElementTree as ET #xml을 문서형식으로 만들어준다.
from urllib.request import urlopen
from pandas.core.frame import DataFrame

app = Flask(__name__)

#크로스 도메인 오류를 해결하기 위햐
#flask-cors패키지를 설치해야 한다. (한 상태)
CORS(app)

    
spec = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo?serviceKey=VXGxM3FjoOVHGwjcIqHM4pa9aZW7Gbp0AvSTDrBcXpvwbv7QRBo6lrB9sPt9EqoldaidCOHjn%2F1E9XwDQm0%2BOA%3D%3D'

zcode_list = {'11':'서울','26':'부산','27':'대구','28':'인천',
              '29':'광주','30':'대전','31':'울산','36':'세종',
            '41':'경기','42':'강원','43':'충북','44':'충남','45':'전북','46':'전남',
            '47':'경북','48':'경남','50':'제주'}


@app.route("/evChart", methods=['POST'])
def ev_chart():
    rows = []
    for code in zcode_list.keys() :
        res = urlopen(spec+"&zcode="+code).read()

        #결과를 xml문서로 받았으니 xml객체화 시킨다.
        xmlDoc = ET.fromstring(res)
        
        totalCount = xmlDoc.find('header').find('totalCount').text
        city = zcode_list.get(code)
        #리스트에 {"code":"11", "city":"서울", "count":"12730" 형식으로 추가
        rows.append({'code':code, 'city':city, 'count':totalCount})
        
        
        #JSON으로 반환하기 위해 DataFrame만든다.
        df = DataFrame(rows)
        
    return df.to_json(orient='records')







@app.route("/evCar",methods=['POST'])#포스트방식 요청
def ev_car():
    zcode_dict = {}
    for code in zcode_list:
        res = urlopen(spec+"&zcode="+code).read()
        
        #결과는 xml문서로 받았다.(res) 이것을 xml문서로 변환해야 함!
        xmlDoc = ET.fromstring(res)
        
        items = xmlDoc.find("body").find("items")
        totalCount = xmlDoc.find("header").find("totalCount").text
        
        data_dict = {}
        
        rows = []
        for item in items:
            statNm = item.find("statNm").text
            chgerType = item.find("chgerType").text
            addr = item.find("addr").text
            rows.append({'s_name':statNm, 'type':chgerType, 'addr':addr})
            
            

        #df = DataFrame(rows)
        data_dict["totalCount"] = totalCount
        data_dict["data"] = rows
        zcode_dict[code] = data_dict
    '''
    zcode_dict = [
     {"11":["totalCount":"12730",
             "data":[{"statNm":"종묘...", "chgerType":"03", "addr":"서울..."},
                     {"statNm":"국립...", "chgerType":"03", "addr":"서울..."},
                     {"statNm":"시청...", "chgerType":"03", "addr":"서울..."},
                    ]
            ]
     },{"26":["totalCount":"12730",
               "data":[{"statNm":"종묘...", "chgerType":"03", "addr":"부산..."},
                       {"statNm":"국립...", "chgerType":"03", "addr":"부산..."},
                       {"statNm":"시청...", "chgerType":"03", "addr":"부산..."},
                      ]
            ]
     }] 
    '''    
    #for key in zcode_dict.keys():
    #    print("{}:{}".format(key,zcode_dict.get(key)["totalCount"]))
    
    
    #JSON으로 반환하기 위해 DataFrame만든다.
    df = DataFrame(zcode_dict)

    return df.to_json(orient='columns')
    
    
    
    