from utils.querys import querylocaldb
def gettiebadata():
    tiebadata=querylocaldb('select * from tiebadata',[],'select')
    return tiebadata

def gettiebaComment():
    tiebaComment=querylocaldb('select * from tiebaComment',[],'select')
    return tiebaComment

def gettiebaHotword():
    tiebaHotword=querylocaldb('select * from tiebaHotword',[],'select')
    return tiebaHotword

def getweibodata():
    weibodata=querylocaldb('select * from weibodata',[],'select')
    return weibodata

def getweiboComment():
    weiboComment=querylocaldb('select * from weiboComment',[],'select')
    return weiboComment

def getweiboHotword():
    weiboHotword=querylocaldb('select * from weiboHotword',[],'select')
    return weiboHotword

def getdateNum():
    dateNum=querylocaldb('select * from dateNum',[],'select')
    return dateNum

def getweiboTypeCount():
    weiboTypeCount=querylocaldb('select * from weiboTypeCount',[],'select')
    return weiboTypeCount

def gettiebaTypeCount():
    tiebaTypeCount=querylocaldb('select * from tiebaTypeCount',[],'select')
    return tiebaTypeCount

def getweiboLikeNum():
    weiboLikeNum=querylocaldb('select * from weiboLikeNum',[],'select')
    return weiboLikeNum

def gettiebaLikeNum():
    tiebaLikeNum=querylocaldb('select * from tiebaLikeNum',[],'select')
    return tiebaLikeNum

def getwLikeCategory():
    wLikeCategory=querylocaldb('select * from wLikeCategory',[],'select')
    return wLikeCategory

def gettLikeCategory():
    tLikeCategory=querylocaldb('select * from tLikeCategory',[],'select')
    return tLikeCategory

def getComCategory():
    ComCategory=querylocaldb('select * from ComCategory',[],'select')
    return ComCategory

def getComLikeCat():
    ComLikeCat=querylocaldb('select * from ComLikeCat',[],'select')
    return ComLikeCat

def getComGender():
    ComGender=querylocaldb('select * from ComGender',[],'select')
    return ComGender

def getweiboAddress():
    weiboAddress=querylocaldb('select * from weiboAddress',[],'select')
    return weiboAddress

def gettiebaAddress():
    tiebaAddress=querylocaldb('select * from tiebaAddress',[],'select')
    return tiebaAddress

def getweiboEmoCount():
    weiboEmoCount=querylocaldb('select * from weiboEmoCount',[],'select')
    return weiboEmoCount

def gettiebaEmoCount():
    tiebaEmoCount=querylocaldb('select * from tiebaEmoCount',[],'select')
    return tiebaEmoCount

def getweiboHotEmoCount():
    weiboHotEmoCount=querylocaldb('select * from weiboHotEmoCount',[],'select')
    return weiboHotEmoCount

def gettiebaHotEmoCount():
    tiebaHotEmoCount=querylocaldb('select * from tiebaHotEmoCount',[],'select')
    return tiebaHotEmoCount

def getweiboScoreCount():
    weiboScoreCount=querylocaldb('select * from weiboScoreCount',[],'select')
    return weiboScoreCount

def gettiebaScoreCount():
    tiebaScoreCount=querylocaldb('select * from tiebaScoreCount',[],'select')
    return tiebaScoreCount
