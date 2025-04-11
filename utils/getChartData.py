from utils.querys import *
from utils.getPublicData import *
from myApp.models import *

def getIndexData():
    weibodata=list(getweibodata())
    tiebadata=list(gettiebadata())
    weiboComment=list(getweiboComment())
    tiebaComment = list(gettiebaComment())
    maxWeiboLike=max([int(item[1]) for item in weibodata])
    maxWeiboComLike=max([int(item[2]) for item in weiboComment])
    maxTiebaLike=max([int(item[6]) for item in tiebadata])
    maxTiebaCom=max([int(item[7]) for item in tiebadata])

    dateNum=list(getdateNum())
    weiboTypeCount=list(getweiboTypeCount())
    tiebaTypeCount=list(gettiebaTypeCount())
    xLineData= [str(x[0]) for x in dateNum][:8]
    y1LineData = [x[1] for x in dateNum][:8]
    y2LineData = [x[2] for x in dateNum][:8]
    print(xLineData, y1LineData, y2LineData)
    pie1Data=[]
    pie2Data=[]
    for i in weiboTypeCount:
        pie1Data.append({
            'name':i[0],
            'value':i[1]
        })

    for i in tiebaTypeCount:
        pie2Data.append({
            'name':i[0],
            'value':i[1]
        })
    print(pie1Data, pie2Data)
    return maxWeiboLike,maxWeiboComLike,maxTiebaLike,maxTiebaCom,xLineData,y1LineData,y2LineData,pie1Data,pie2Data


def changePwd(userInfo,passwordInfo):
    oldPwd=passwordInfo['oldPwd']
    newPwd = passwordInfo['newPwd']
    ckdPwd = passwordInfo['ckdPwd']
    user=User.objects.get(username=userInfo.username)
    if oldPwd != user.password:return '原密码错误'
    if newPwd != ckdPwd:return '二次确认密码失败'
    if oldPwd == newPwd:return '新密码不能与旧密码相同'
    if newPwd =="" or ckdPwd =="":return '密码不能为空'
    if len(newPwd)<6:return '密码长度至少为6位'
    user.password=newPwd
    user.save()

def getTiebaDetail(tid):
    tiebaComment=querylocaldb('select * from tiebaComment where tid = %s',[tid],'select')
    # print(tiebaComment[0])
    return tiebaComment
def getWeiboDetail(articleId):
    weiboComment=querylocaldb('select * from weiboComment where articleId = %s',[articleId],'select')
    # print(weiboComment[0])
    return weiboComment

def hotTiebaSelect(tiebaWord):
    tiebaCommentList=list(gettiebaComment())
    tiebaLineData={}
    for i in tiebaCommentList:
        realTime=i[5][:10]
        try:
            if tiebaWord in i[3]:
                if tiebaLineData.get(realTime,-1)==-1: #搜索数据库，判断热词是否在内容中，如果在就+1
                    tiebaLineData[realTime]=1
                else:
                    tiebaLineData[realTime]+=1
        except:
            continue
    lineX=[]
    lineY=[]
    for key,value in tiebaLineData.items():
        lineX.append(key)
        lineY.append(value)
    print(lineX,lineY)
    return lineX,lineY

def hotWeiboSelect(weiboWord):
    weiboCommentList=list(getweiboComment())
    weiboLineData={}
    for i in weiboCommentList:
        realTime=i[1]
        try:
            if weiboWord in i[4]:
                if weiboLineData.get(realTime,-1)==-1: #搜索数据库，判断热词是否在内容中，如果在就+1
                    weiboLineData[realTime]=1
                else:
                    weiboLineData[realTime]+=1
        except:
            continue
    lineX2=[]
    lineY2=[]
    for key,value in weiboLineData.items():
        lineX2.append(key)
        lineY2.append(value)
    print(lineX2, lineY2)
    return lineX2,lineY2

def getPostChartData():
    wLikeCategoryList=list(getwLikeCategory())#微博点赞
    tLikeCategoryList=list(gettLikeCategory())#贴吧点赞
    ComCategoryList=list(getComCategory()) #评论
    order=['0-1000','1000-2000','5000-10000','10000-20000','20000以上']
    order1=['0-50','50-100','100-200','200-500','500-1000','1000以上']
    order2=['0-10','10-50','50-100','100-500','500-1000','1000以上']
    data_dict={item[0]:item[1:] for item in wLikeCategoryList}
    data_dict1={item[0]:item[1:] for item in tLikeCategoryList}
    data_dict2={item[0]:item[1:] for item in ComCategoryList}

    sorted_data=[(key,data_dict[key]) for key in order if key in data_dict]
    sorted_data1=[(key, data_dict1[key]) for key in order1 if key in data_dict1]
    sorted_data2=[(key, data_dict2[key]) for key in order2 if key in data_dict2]
    print(sorted_data,sorted_data1,sorted_data2)

    x1Data=[x[0] for x in sorted_data]
    y1Data = [x[1][0] for x in sorted_data]
    print(x1Data,y1Data)
    x2Data = [x[0] for x in sorted_data1]
    y2Data = [x[1][0] for x in sorted_data1]
    print(x1Data, y1Data)
    x3Data = [x[0] for x in sorted_data2]
    y3Data1 = [x[1][0] for x in sorted_data2]
    y3Data2 = [x[1][1] for x in sorted_data2]
    print(x3Data,y3Data1,y3Data2)
    print(wLikeCategoryList[0],tLikeCategoryList,ComCategoryList)
    return x1Data,y1Data,x2Data,y2Data,x3Data,y3Data1,y3Data2

def getCommentChartData():
    comLikeCatList=list(getComLikeCat())
    comGenderList=list(getComGender())
    order = ['0-10', '10-50', '50-100', '100-500', '500-1000', '1000以上']
    data_dict = {item[0]: item[1:] for item in comLikeCatList}
    sorted_data = [(key, data_dict[key]) for key in order if key in data_dict]
    print(comLikeCatList[0],comGenderList[0])
    print(sorted_data)
    xData=[x[0] for x in sorted_data]
    yData=[x[1][0] for x in sorted_data]
    print(xData,yData)
    roseData=[]
    for i in comGenderList:
        sex=''
        if i[0]=='m':
            sex='男'
        elif i[0]=='f':
            sex='女'
        else:
            sex='未知'
        roseData.append({
            'name':sex,
            'value':i[1]
        })
    print(roseData)
    return xData,yData,roseData

def getAddressData():
    weiboAddressList=list(getweiboAddress())
    tiebaAddressList=list(gettiebaAddress())
    print(weiboAddressList,tiebaAddressList)
    weiboMapData=[]
    tiebaMapData=[]
    for i in weiboAddressList:
        realCity=''
        if len(i[0])>2:
            realCity=i[0][3:]
        elif i[0]=='其他':
            continue
        else:
            realCity=i[0]
            weiboMapData.append({
                'name':realCity,
                'value':i[1]
            })

    for i in tiebaAddressList:
        realCity=''
        if len(i[0])>2:
            realCity=i[0][3:]
        elif i[0]=='其他':
            continue
        else:
            realCity=i[0]
            tiebaMapData.append({
                'name':realCity,
                'value':i[1]
            })
    print(weiboMapData,tiebaMapData)
    return weiboMapData,tiebaMapData

def getEmoChartData():
    weiboEmoCountList=list(getweiboEmoCount())
    tiebaEmoCountList = list(gettiebaEmoCount())

    weiboHotEmoCountList=list(getweiboHotEmoCount())
    tiebaHotEmoCountList = list(gettiebaHotEmoCount())

    weiboScoreCountList=list(getweiboScoreCount())
    tiebaScoreCountList = list(gettiebaScoreCount())

    weiboHotDataList=list(getweiboHotword())
    tiebaHotDataList=list(gettiebaHotword())

    order = ['0-0.1', '0.1-0.2', '0.2-0.3', '0.3-0.4', '0.4-0.5', '0.5-0.6','0.6-0.7','0.7-0.8','0.8-0.9','0.9-1']
    data_dict = {item[0]: item[1:] for item in weiboScoreCountList}
    sorted_data = [(key, data_dict[key]) for key in order if key in data_dict]
    data_dict1 = {item[0]: item[1:] for item in tiebaScoreCountList}
    sorted_data1 = [(key, data_dict1[key]) for key in order if key in data_dict1]
    print(weiboEmoCountList[0],tiebaEmoCountList[0],weiboHotEmoCountList[0],tiebaHotEmoCountList[0],weiboScoreCountList[0],tiebaScoreCountList[0])
    print(sorted_data,sorted_data1)

    xWeiboData1=[x[0] for x in weiboEmoCountList]
    yWeiboData1=[x[1] for x in weiboEmoCountList]
    xTiebaData1 = [x[0] for x in tiebaEmoCountList]
    yTiebaData1 = [x[1] for x in tiebaEmoCountList]

    totleWeiboData=sum(yWeiboData1)
    xWeiboDataRate = [round((value/totleWeiboData)*100,0) for value in yWeiboData1]

    totleTiebaData = sum(yTiebaData1)
    xTiebaDataRate = [round((value / totleTiebaData) * 100, 0) for value in yTiebaData1]

    weiboCircleData=[]
    for i in weiboHotEmoCountList:
        weiboCircleData.append({
            'name':i[0],
            'value':i[1]
        })

    tiebaCircleData = []
    for i in tiebaHotEmoCountList:
        tiebaCircleData.append({
            'name':i[0],
            'value':i[1]
        })

    xWeiboLine2=[x[0] for x in sorted_data]
    yWeiboLine2=[x[1][0] for x in sorted_data]
    xTiebaLine2 = [x[0] for x in sorted_data]
    yTiebaLine2 = [x[1][0] for x in sorted_data]

    xWeiboBar3=[x[0] for x in weiboHotDataList][:10]
    yweiboBar3=[x[1] for x in weiboHotDataList][:10]
    xTiebaBar3 = [x[0] for x in tiebaHotDataList][:10]
    yTiebaBar3 = [x[1] for x in tiebaHotDataList][:10]

    weiboBarData=[]
    for i in weiboHotDataList:
        weiboBarData.append({
            'areaName':i[0],
            'value':i[1]
        })

    tiebaBarData = []
    for i in tiebaHotDataList:
        tiebaBarData.append({
            'areaName': i[0],
            'value': i[1]
        })
    return xWeiboData1,yWeiboData1,xWeiboDataRate,weiboCircleData,xWeiboLine2,yWeiboLine2,xWeiboBar3,yweiboBar3,xTiebaData1,yTiebaData1,xTiebaDataRate,tiebaCircleData,xTiebaLine2,yTiebaLine2,xTiebaBar3,yTiebaBar3
