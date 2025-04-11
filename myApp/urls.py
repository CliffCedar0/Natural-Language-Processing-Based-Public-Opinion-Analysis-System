from django.contrib import  admin
from django.urls import path, include
from myApp import views
from django.urls import path
urlpatterns = [
    path('index/', views.index, name='home'),
    path('selfInfo/', views.selfInfo, name='selfInfo'),
    path('tiebaData/', views.tiebaData, name='tiebaData'),
    path('weiboData/', views.weiboData, name='weiboData'),
    path('tiebaComment/<a_id>', views.tiebaComment, name='tiebaComment'),
    path('weiboComment/<b_id>', views.weiboCommemt, name='weiboComment'),
    path('hotData/', views.hotData, name='hotData'),
    path('postChart/', views.postChart, name='postChart'),
    path('CommentChart/', views.CommentChart, name='CommentChart'),
    path('addressChart/', views.addressChart, name='addressChart'),
    path('emoChart/', views.emoChart, name='emoChart'),
    path('weiboCloud/', views.weiboCloud, name='weiboCloud'),
    path('tiebaCloud/', views.tiebaCloud, name='tiebaCloud'),
    path('commentCloud/', views.commentCloud, name='commentCloud'),
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path('register/', views.register, name='register'),
    path('analysis/', views.analysis, name='analysis'),
    path('rag/', views.rag, name='rag'),
    path('LDA/', views.LDA, name='LDA'),
    path('Bertopic/', views.Bertopic, name='Bertopic'),
    path('Textclustering/', views.Textclustering, name='Textclustering'),
    path('image_code/', views.image_code, name='image_code'),

    # 其他路径...
]
