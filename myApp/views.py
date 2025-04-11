import json
import requests  # 正确导入 requests 库
from io import BytesIO

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from utils.captcha import check_code
from utils.getChartData import *

# Create your views here.
def index(request):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)
    maxWeiboLike,maxWeiboComLike,maxTiebaLike,maxTiebaCom,xLineData,y1LineData,y2LineData,pie1Data,pie2Data=getIndexData()
    weiboLikeNumList=list(getweiboLikeNum())
    tiebaLikeNumList=list(gettiebaLikeNum())
    return render(request,'index.html',{
        'userInfo':userInfo,
        'maxWeiboLike':maxWeiboLike,
        'maxWeiboComLike':maxWeiboComLike,
        'maxTiebaLike':maxTiebaLike,
        'maxTiebaCom':maxTiebaCom,
        'xLineData':xLineData,
        'y1LineData':y1LineData,
        'y2LineData':y2LineData,
        'pie1Data':pie1Data,
        'pie2Data':pie2Data,
        'weiboLikeNumList':weiboLikeNumList,
        'tiebaLikeNumList':tiebaLikeNumList
    })

def selfInfo(request):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)
    if request.method=='POST':
        print(request.POST)
        res=changePwd(userInfo,request.POST)
        if res!=None:
            messages.error(request,res)
            return HttpResponseRedirect('/myApp/selfInfo')
        else:
            return redirect('login')
    return render(request,'selfInfo.html',{
        'userInfo':userInfo,
    })

def tiebaData(request):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)
    tiebaData=list(gettiebadata())
    return render(request,'tiebaData.html',{
        'userInfo':userInfo,
        'tiebaData':tiebaData
    })

def weiboData(request):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)
    weiboData=list(getweibodata())
    return render(request,'weiboData.html',{
        'userInfo':userInfo,
        'weiboData':weiboData
    })

def tiebaComment(request,a_id):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)
    print(a_id)
    # getTiebaDetail(a_id)
    tiebaComment=getTiebaDetail(a_id)
    return render(request,'tiebaComment.html',{
        'userInfo':userInfo,
        'tiebaData':tiebaData,
        'tiebaComment':tiebaComment,
        'a_id':a_id
    })


def weiboCommemt(request,b_id):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)
    # print(b_id)
    # getTiebaDetail(a_id)
    try:
        weiboComment=getWeiboDetail(b_id)
        return render(request,'weiboComment.html',{
            'userInfo':userInfo,
            'weiboData':weiboData,
            'weiboComment': weiboComment,
            'b_id':b_id
        })
    except:
        return render(request,'weiboComment.html',{
            'userInfo':userInfo,
            'weiboData':weiboData,
            'b_id':b_id
        })

def hotData(request):
    uname=request.session.get('username')
    userInfo=User.objects.get(username=uname)

    hotTiebaList=list(gettiebaHotword())
    hotTiebaList=[x[0] for x in hotTiebaList]
    hotWeiboList=list(getweiboHotword())
    hotWeiboList=[x[0] for x in hotWeiboList]
    print(hotTiebaList)

    defaultTieba=hotTiebaList[0]
    defaultWeibo=hotWeiboList[0]
    tiebaWord = '%' + defaultTieba + '%'
    tiebaComData = querylocaldb('select * from tiebaComment where comContent Like %s', [tiebaWord], 'select')
    lineX, lineY = hotTiebaSelect(defaultTieba)
    weiboWord = '%' + defaultWeibo + '%'
    weiboComData = querylocaldb('select * from weiboComment where content Like %s', [weiboWord], 'select')
    lineX2, lineY2 = hotWeiboSelect(defaultWeibo)
    if request.method=='POST':
        defaultTieba=request.POST.get('defaultTieba')
        defaultWeibo=request.POST.get('defaultWeibo')
        print(defaultTieba)
        if defaultTieba==None:
            defaultTieba=hotTiebaList[0]
        if defaultWeibo==None:
            defaultWeibo=hotWeiboList[0]

        tiebaWord='%' +defaultTieba+ '%'
        tiebaComData=querylocaldb('select * from tiebaComment where comContent Like %s',[tiebaWord],'select')
        lineX,lineY=hotTiebaSelect(defaultTieba)

        weiboWord='%' +defaultWeibo+ '%'
        weiboComData=querylocaldb('select * from weiboComment where content Like %s',[weiboWord],'select')
        lineX2,lineY2=hotWeiboSelect(defaultWeibo)
        return render(request, 'hotData.html', {
            'userInfo': userInfo,
            'hotTiebaList': hotTiebaList,
            'tiebaComData': tiebaComData,
            'defaultTieba':defaultTieba,
            'lineX': lineX,
            'lineY': lineY,
            'hotWeiboList': hotWeiboList,
            'weiboComData': weiboComData,
            'defaultWeibo':defaultWeibo,
            'lineX2': lineX2,
            'lineY2': lineY2
        })
    return render(request,'hotData.html',{
        'userInfo':userInfo,
        'hotTiebaList':hotTiebaList,
        'hotWeiboList':hotWeiboList,
        'tiebaComData': tiebaComData,
        'defaultTieba': defaultTieba,
        'lineX': lineX,
        'lineY': lineY,
        'weiboComData': weiboComData,
        'defaultWeibo': defaultWeibo,
        'lineX2': lineX2,
        'lineY2': lineY2
    })


def postChart(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    x1Data,y1Data,x2Data,y2Data,x3Data,y3Data1,y3Data2=getPostChartData()
    return render(request, 'postChart.html', {
        'userInfo': userInfo,
        'x1Data': x1Data,
        'y1Data': y1Data,
        'x2Data': x2Data,
        'y2Data': y2Data,
        'x3Data': x3Data,
        'y3Data1': y3Data1,
        'y3Data2': y3Data2
    })

def CommentChart(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    xData,yData,roseData=getCommentChartData()
    return render(request, 'CommentChart.html', {
        'userInfo': userInfo,
        'xData': xData,
        'yData': yData,
        'roseData': roseData
    })

def addressChart(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    weiboMapData,tiebaMapData=getAddressData()
    getAddressData()
    return render(request, 'addressChart.html', {
        'userInfo': userInfo,
        'weiboMapData': weiboMapData,
        'tiebaMapData': tiebaMapData
    })

def emoChart(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    xWeiboData1,yWeiboData1,xWeiboDataRate,weiboCircleData,xWeiboLine2,yWeiboLine2,xWeiboBar3,yweiboBar3,xTiebaData1,yTiebaData1,xTiebaDataRate,tiebaCircleData,xTiebaLine2,yTiebaLine2,xTiebaBar3,yTiebaBar3=getEmoChartData()
    return render(request, 'emoChart.html', {
        'userInfo': userInfo,
        'xWeiboData1':xWeiboData1,
        'yWeiboData1':yWeiboData1,
        'xWeiboDataRate':xWeiboDataRate,
        'weiboCircleData':weiboCircleData,
        'xWeiboLine2':xWeiboLine2,
        'yWeiboLine2':yWeiboLine2,
        'xWeiboBar3':xWeiboBar3,
        'yweiboBar3':yweiboBar3,
        'xTiebaData1':xTiebaData1,
        'yTiebaData1':yTiebaData1,
        'xTiebaDataRate':xTiebaDataRate,
        'tiebaCircleData':tiebaCircleData,
        'xTiebaLine2':xTiebaLine2,
        'yTiebaLine2':yTiebaLine2,
        'xTiebaBar3':xTiebaBar3,
        'yTiebaBar3':yTiebaBar3
    })


def weiboCloud(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'weiboCloud.html', {
        'userInfo': userInfo,
    })

def tiebaCloud(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'tiebaCloud.html', {
        'userInfo': userInfo,
    })

def commentCloud(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'commentCloud.html', {
        'userInfo': userInfo,
    })


def login(request):
    if request.method == "GET":
        return render(request, 'login.html', {})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        verification_code = request.POST.get('verification_code')

        # 检查验证码是否为None
        if verification_code is None:
            messages.error(request, '请输入验证码！')
            return redirect('/myApp/login')

        verification_code = verification_code.upper()  # 转换为大写
        session_code = request.session.get('image_code', '').upper()  # 获取并转换为大写

        if verification_code != session_code:
            messages.error(request, '验证码错误，请重新输入！')
            return redirect('/myApp/login')

        try:
            user = User.objects.get(username=username, password=password)
            request.session['username'] = username
            return redirect('/myApp/index')
        except ObjectDoesNotExist:
            messages.error(request, '请输入正确的用户名或密码！')
            return redirect('/myApp/login')

def getCaptcha(request):
    # 调用poillow函数，生成图片
    img, code_string = check_code()
    print(code_string)
    # 创建内存中的文件
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.clear()
    return redirect('login')



def register(request):
    if request.method == "GET":
        return render(request,'register.html',{})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        ckPassword = request.POST.get('ckPassword')
        print(username,password,ckPassword)
        try:
            User.objects.get(username=username),
            message='该用户名已存在!'
            messages.error(request,message)
            return HttpResponseRedirect('/myApp/register')
        except:
            if not username or not password or not ckPassword:
                message='请输入完整的注册信息!'
                messages.error(request, message)
                return HttpResponseRedirect('/myApp/register')
            elif password != ckPassword:
                message='输入的两次密码不相同!'
                messages.error(request, message)
                return HttpResponseRedirect('/myApp/register')
            else:
                User.objects.create(username=username,password=password)
                messages.success(request, '恭喜您!注册成功!')
                return HttpResponseRedirect('/myApp/login')


def analysis(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)


    # 将用户信息和热搜数据传递给模板
    return render(request, 'analysis.html', {
        'userInfo': userInfo,
    })
def rag(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'rag.html', {
        'userInfo': userInfo,
    })


def LDA(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'LDA.html', {
        'userInfo': userInfo,
    })


def Bertopic(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'Bertopic.html', {
        'userInfo': userInfo,
    })

def Textclustering(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'Textclustering.html', {
        'userInfo': userInfo,
    })


def image_code(request):
    # 调用 check_code 函数获取图像对象和验证码字符串
    img, code_string = check_code()
    # 打印验证码字符串到控制台（仅用于调试）
    print(code_string)
    # 将验证码字符串存储在 session 中
    request.session['image_code'] = code_string
    # 创建一个 BytesIO 对象用于保存图像
    stream = BytesIO()
    # 将图像保存到 BytesIO 对象
    img.save(stream, 'PNG')  # 注意这里使用大写 'PNG'
    # 返回 HttpResponse，内容类型为 'image/png'
    return HttpResponse(stream.getvalue(), content_type='image/png')


