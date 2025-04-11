#coding:utf8

#导包
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StringType,IntegerType,StructType,StructField,FloatType
from pyspark.sql.functions import count,mean,col,sum,when,max,min,avg,to_timestamp,current_timestamp,unix_timestamp,to_date,expr,coalesce,lit


if __name__ == '__main__':
    # 构建 关于SparkSession的配置
    spark = SparkSession.builder.appName("sparkSQL").master("local[*]"). \
        config('spark.sql.shuffle.partitions', 2). \
        config('spark.sql.warehouse.dir', 'hdfs://node1:8020/user/hive/warehouse'). \
        config('hive.metastore.uris', 'thrift://node1:9083'). \
        enableHiveSupport(). \
        getOrCreate()
    #读取数据表-再进行数据分析
    #贴吧和微博数据
    tiebadata=spark.read.table('tiebadata')
    weibodata=spark.read.table('weibodata')
    #贴吧和微博评论
    tiebaComment=spark.read.table('tiebaComment')
    weiboComment = spark.read.table('weiboComment')
    #贴吧和微博热词
    tiebaHotword = spark.read.table('tiebaHotword')
    weiboHotword=spark.read.table('weiboHotword')

    #需求1：时间统计
    #贴吧时间统计
    tiebadata=tiebadata.withColumn('postTime', to_date(col('postTime'), 'yyyy-MM-dd HH:mm:ss')) #把postTime从文本格式转换为时间格式
    resualt1 = tiebadata.groupby('postTime').agg(count('*').alias('count'))
    resualt1 = resualt1.withColumn('days_diff', expr('datediff(current_date(),postTime)'))  # 时间对比，对时间进行排序，离当前月近排名就越高
    resualt1 = resualt1.orderBy('days_diff')  # 排序

    #微博时间统计
    weibodata = weibodata.withColumn('create_at', to_date(col('create_at'), 'yyyy-MM-dd'))  # 把postTime从文本格式转换为时间格式
    resualt2 = weibodata.groupby('create_at').agg(count('*').alias('count'))
    resualt2 = resualt2.withColumn('days_diff', expr('datediff(current_date(),create_at)'))  # 时间对比，对时间进行排序，离当前月近排名就越高
    resualt2 = resualt2.orderBy('days_diff')  # 排序

    #把贴吧和微博相同时间点的数量进行结合
    resualt1 = resualt1.withColumnRenamed('count', 'post_count')
    resualt2 = resualt2.withColumnRenamed('count', 'created_count')
    combined_resualt = resualt1.join(resualt2, resualt1.postTime == resualt2.create_at).\
        select(
        coalesce(resualt1.postTime, resualt2.create_at).alias('date'),
        coalesce(resualt1.post_count, lit(0)).alias('post_count'),
        coalesce(resualt2.created_count, lit(0)).alias('created_count'),
    )
    combined_resualt=combined_resualt.orderBy(col('date').desc())
    # resualt2.show()
    # resualt1.show()
    # combined_resualt.show()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    combined_resualt.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'dateNum'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    combined_resualt.write.mode('overwrite').format('parquet').saveAsTable('dateNum')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from dateNum').show()

    # ===========================================================================================================================
    #需求2：类型统计
    resualt3=weibodata.groupby('type').count()
    resualt4 = tiebadata.groupby('area').count()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt3.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboTypeCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt3.write.mode('overwrite').format('parquet').saveAsTable('weiboTypeCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboTypeCount').show()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt4.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaTypeCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt4.write.mode('overwrite').format('parquet').saveAsTable('tiebaTypeCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaTypeCount').show()

    # ===========================================================================================================================
    #需求3：帖子点赞排序
    resualt5=weibodata.orderBy(col('likeNum').desc()).limit(10)
    resualt6=tiebadata.orderBy(col('likeNum').desc()).limit(10)
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt5.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboLikeNum'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt5.write.mode('overwrite').format('parquet').saveAsTable('weiboLikeNum')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboLikeNum').show()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt6.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaLikeNum'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt6.write.mode('overwrite').format('parquet').saveAsTable('tiebaLikeNum')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaLikeNum').show()
    # ===========================================================================================================================
    #需求4：点赞区间分类
    weibodata_like_category=weibodata.withColumn(
        'like_category',
        when(col('likeNum').between(0,1000),'0-1000').\
        when(col('likeNum').between(1000, 2000), '1000-2000').\
        when(col('likeNum').between(2000, 5000), '2000-5000').\
        when(col('likeNum').between(5000, 10000), '5000-10000').\
        when(col('likeNum').between(10000, 20000), '10000-20000').\
        otherwise('20000以上')
    )
    #对like_category进行分类
    resualt7=weibodata_like_category.groupby('like_category').count()

    tiebadata_like_category=tiebadata.withColumn(
        'like_category',
        when(col('likeNum').between(0,50),'0-50').\
        when(col('likeNum').between(50, 100), '50-100').\
        when(col('likeNum').between(100, 200), '100-200').\
        when(col('likeNum').between(200, 500), '200-500').\
        when(col('likeNum').between(500, 1000), '500-1000').\
        otherwise('1000以上')
    )
    #对like_category进行分类
    resualt8=tiebadata_like_category.groupby('like_category').count()

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt7.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'wLikeCategory'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt7.write.mode('overwrite').format('parquet').saveAsTable('wLikeCategory')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from wLikeCategory').show()

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt8.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tLikeCategory'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt8.write.mode('overwrite').format('parquet').saveAsTable('tLikeCategory')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tLikeCategory').show()
    # ===========================================================================================================================
    #评论量分类
    weibodata_com_category = weibodata.withColumn(
        'Com_category',
        when(col('commentsLen').between(0, 10), '0-10'). \
            when(col('commentsLen').between(10, 50), '10-50'). \
            when(col('commentsLen').between(50, 100), '50-100'). \
            when(col('commentsLen').between(100, 500), '100-500'). \
            when(col('commentsLen').between(500, 1000), '500-1000'). \
            otherwise('1000以上')
    )
    resualt9 = weibodata_com_category.groupby('Com_category').count()

    tiebadata_com_category = tiebadata.withColumn(
        'Com_category',
        when(col('replyNum').between(0, 10), '0-10'). \
            when(col('replyNum').between(10, 50), '10-50'). \
            when(col('replyNum').between(50, 100), '50-100'). \
            when(col('replyNum').between(100, 500), '100-500'). \
            when(col('replyNum').between(500, 1000), '500-1000'). \
            otherwise('1000以上')
    )
    resualt10 = tiebadata_com_category.groupby('Com_category').count()

    #结合评论数统计
    combined_resualt2=resualt9.join(resualt10,resualt9.Com_category==resualt10.Com_category,'outer').\
        select(
        coalesce(resualt9.Com_category,resualt10.Com_category).alias('category'),
        coalesce(resualt9['count'], lit(0)).alias('weibo_count'),
        coalesce(resualt10['count'], lit(0)).alias('tieba_count'),
    )
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    combined_resualt2.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'ComCategory'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    combined_resualt2.write.mode('overwrite').format('parquet').saveAsTable('ComCategory')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from ComCategory').show()

    # ===========================================================================================================================
    #需求6：评论分析,点赞数
    weibodata_comLike_category = weiboComment.withColumn(
        'comLike_category',
        when(col('like_counts').between(0,10),'0-10').\
        when(col('like_counts').between(10, 50), '10-50').\
        when(col('like_counts').between(50, 100), '50-100').\
        when(col('like_counts').between(100, 500), '100-500').\
        when(col('like_counts').between(500, 1000), '500-1000').\
        otherwise('1000以上')
    )
    resualt11=weibodata_comLike_category.groupby('comLike_category').count()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt11.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'ComLikeCat'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt11.write.mode('overwrite').format('parquet').saveAsTable('ComLikeCat')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from ComLikeCat').show()

    #评论性别分析
    resualt12=weiboComment.groupby('authorGender').count()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt12.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'ComGender'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt12.write.mode('overwrite').format('parquet').saveAsTable('ComGender')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from ComGender').show()

    #地址
    resualt13=weiboComment.groupby('authorAddress').count()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt13.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboAddress'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt13.write.mode('overwrite').format('parquet').saveAsTable('weiboAddress')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboAddress').show()

    resualt14=tiebaComment.groupby('comAddress').count()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt14.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaAddress'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt14.write.mode('overwrite').format('parquet').saveAsTable('tiebaAddress')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaAddress').show()

    #帖子情感得分分析
    weibodata_scores_category = weibodata.withColumn(
        'emo_category',
        when(col('scores').between(0,0.45),'消极').\
        when(col('scores').between(0.45, 0.55), '平淡').\
        when(col('scores').between(0.55, 1), '积极').\
        otherwise('未知')
    )
    tiebadata_scores_category = tiebadata.withColumn(
        'emo_category',
        when(col('scores').between(0,0.45),'消极').\
        when(col('scores').between(0.45, 0.55), '平淡').\
        when(col('scores').between(0.55, 1), '积极').\
        otherwise('未知')
    )
    resualt15=weibodata_scores_category.groupby('emo_category').count()
    resualt16=tiebadata_scores_category.groupby('emo_category').count()

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt15.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboEmoCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt15.write.mode('overwrite').format('parquet').saveAsTable('weiboEmoCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboEmoCount').show()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt16.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaEmoCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt16.write.mode('overwrite').format('parquet').saveAsTable('tiebaEmoCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaEmoCount').show()

    #热词情感
    weibodata_Hotscores_category = weiboHotword.withColumn(
        'emo_category',
        when(col('scores').between(0, 0.45), '消极'). \
            when(col('scores').between(0.45, 0.55), '平淡'). \
            when(col('scores').between(0.55, 1), '积极'). \
            otherwise('未知')
    )
    tiebadata_Hotscores_category = tiebaHotword.withColumn(
        'emo_category',
        when(col('scores').between(0, 0.45), '消极'). \
            when(col('scores').between(0.45, 0.55), '平淡'). \
            when(col('scores').between(0.55, 1), '积极'). \
            otherwise('未知')
    )
    resualt17 = weibodata_Hotscores_category.groupby('emo_category').count()
    resualt18 = tiebadata_Hotscores_category.groupby('emo_category').count()

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt17.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboHotEmoCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt17.write.mode('overwrite').format('parquet').saveAsTable('weiboHotEmoCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboHotEmoCount').show()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt18.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaHotEmoCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt18.write.mode('overwrite').format('parquet').saveAsTable('tiebaHotEmoCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaHotEmoCount').show()

    #热词得分区间
    weiboHotWord_range_category = weiboHotword.withColumn(
        'scoreCategory',
        when(col('scores').between(0, 0.1), '0-0.1').\
        when(col('scores').between(0.1, 0.2), '0.1-0.2').\
        when(col('scores').between(0.2, 0.3), '0.2-0.3').\
        when(col('scores').between(0.3, 0.4), '0.3-0.4').\
        when(col('scores').between(0.4, 0.5), '0.4-0.5').\
        when(col('scores').between(0.5, 0.6), '0.5-0.6').\
        when(col('scores').between(0.6, 0.7), '0.6-0.7').\
        when(col('scores').between(0.7, 0.8), '0.7-0.8').\
        when(col('scores').between(0.8, 0.9), '0.8-0.9'). \
        when(col('scores').between(0.9, 1), '0.9-1').\
        otherwise('超出范围')
    )
    tiebaHotWord_range_category = tiebaHotword.withColumn(
        'scoreCategory',
        when(col('scores').between(0, 0.1), '0-0.1').\
        when(col('scores').between(0.1, 0.2), '0.1-0.2').\
        when(col('scores').between(0.2, 0.3), '0.2-0.3').\
        when(col('scores').between(0.3, 0.4), '0.3-0.4').\
        when(col('scores').between(0.4, 0.5), '0.4-0.5').\
        when(col('scores').between(0.5, 0.6), '0.5-0.6').\
        when(col('scores').between(0.6, 0.7), '0.6-0.7').\
        when(col('scores').between(0.7, 0.8), '0.7-0.8').\
        when(col('scores').between(0.8, 0.9), '0.8-0.9'). \
        when(col('scores').between(0.9, 1), '0.9-1').\
        otherwise('超出范围')
    )
    resualt19=weiboHotWord_range_category.groupby('scoreCategory').count()
    resualt20=weiboHotWord_range_category.groupby('scoreCategory').count()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt19.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboScoreCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt19.write.mode('overwrite').format('parquet').saveAsTable('weiboScoreCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboScoreCount').show()
    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    resualt20.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaScoreCount'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()
    resualt20.write.mode('overwrite').format('parquet').saveAsTable('tiebaScoreCount')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaScoreCount').show()
