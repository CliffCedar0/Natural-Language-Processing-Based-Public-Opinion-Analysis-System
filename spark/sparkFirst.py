#coding:utf8
#导包
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StringType,StructField,StructType,IntegerType,FloatType

if __name__ == '__main__':
    #构建 关于SparkSession的配置
    spark = SparkSession.builder.appName("sparkSQL").master("local[*]").\
        config('spark.sql.shuffle.partitions', 2).\
        config('spark.sql.warehouse.dir', 'hdfs://node1:8020/user/hive/warehouse').\
        config('hive.metastore.uris', 'thrift://node1:9083'). \
        enableHiveSupport(). \
        getOrCreate()

    schema=StructType().add('area',StringType(),nullable=True).\
        add('tid',StringType(),nullable=True).\
        add('author', StringType(), nullable=True).\
        add('authorImg', StringType(), nullable=True).\
        add('title', StringType(), nullable=True).\
        add('content', StringType(), nullable=True).\
        add('likeNum', IntegerType(), nullable=True).\
        add('replyNum', IntegerType(), nullable=True).\
        add('postTime', StringType(), nullable=True).\
        add('scores', FloatType(), nullable=True)

    #存储
    df=spark.read.format('csv').\
        option('sep',',').\
        option('header',True).\
        option('encoding','utf-8').\
        schema(schema=schema).\
        load('./NLP_Tieba.csv')
    # df.show()
    df=df.withColumn('id',monotonically_increasing_id())
    #数据清洗
    df=df.drop_duplicates()  # 去除重复行
    # df=df.dropna()  # 删除包含缺失值的行

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    df.write.mode('overwrite').\
        format('jdbc').\
        option('url','jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8').\
        option('dbtable','tiebadata').\
        option('user','root').\
        option('password','root').\
        option('encoding','utf-8').\
        save()

    df.write.mode('overwrite').format('parquet').saveAsTable('tiebadata')#保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebadata').show()

    #=================================================================================================================
    # tieba评论
    schema2 = StructType().add('tid', StringType(), nullable=True). \
        add('comAuthor', StringType(), nullable=True). \
        add('comAuthorImg', StringType(), nullable=True). \
        add('comContent', StringType(), nullable=True). \
        add('comAddress', StringType(), nullable=True). \
        add('comTime', StringType(), nullable=True)


    # 存储
    df2 = spark.read.format('csv'). \
        option('sep', ','). \
        option('header', True). \
        option('encoding', 'utf-8'). \
        schema(schema=schema2). \
        load('./tiebaDetail.csv')
    # df.show()
    df2 = df2.withColumn('id', monotonically_increasing_id())
    # 数据清洗
    df2 = df2.drop_duplicates()  # 去除重复行
    # df=df.dropna()  # 删除包含缺失值的行

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    df2.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaComment'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()

    df2.write.mode('overwrite').format('parquet').saveAsTable('tiebaComment')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaComment').show()


    # =================================================================================================================
    # tieba热词评论
    schema3 = StructType().add('word', StringType(), nullable=True). \
        add('count', StringType(), nullable=True). \
        add('scores', FloatType(), nullable=True)

    # 存储
    df3 = spark.read.format('csv'). \
        option('sep', ','). \
        option('header', True). \
        option('encoding', 'utf-8'). \
        schema(schema=schema3). \
        load('./NLP_hotWordTieba.csv')
    # df.show()
    df3 = df3.withColumn('id', monotonically_increasing_id())
    # 数据清洗
    df3 = df3.drop_duplicates()  # 去除重复行
    # df=df.dropna()  # 删除包含缺失值的行

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    df3.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'tiebaHotword'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()

    df3.write.mode('overwrite').format('parquet').saveAsTable('tiebaHotword')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from tiebaHotword').show()

    # =================================================================================================================
    # weibo数据
    schema4 = StructType().add('aid', StringType(), nullable=True). \
        add('likeNum', IntegerType(), nullable=True). \
        add('commentsLen', IntegerType(), nullable=True). \
        add('reposts_count', IntegerType(), nullable=True). \
        add('region', StringType(), nullable=True). \
        add('content', StringType(), nullable=True). \
        add('contentLen', IntegerType(), nullable=True). \
        add('create_at', StringType(), nullable=True). \
        add('type', StringType(), nullable=True). \
        add('detailUrl', StringType(), nullable=True). \
        add('authorAvatar', StringType(), nullable=True). \
        add('authorName', StringType(), nullable=True). \
        add('authorDetail', StringType(), nullable=True). \
        add('isVip', IntegerType(), nullable=True). \
        add('scores', FloatType(), nullable=True)
        # 存储
    df4 = spark.read.format('csv'). \
        option('sep', ','). \
        option('header', True). \
        option('encoding', 'utf-8'). \
        schema(schema=schema4). \
        load('./NLP_weibo.csv')
    # df.show()
    df4 = df4.withColumn('id', monotonically_increasing_id())
    # 数据清洗
    df4 = df4.drop_duplicates()  # 去除重复行
    # df=df.dropna()  # 删除包含缺失值的行

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    df4.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weibodata'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()

    df4.write.mode('overwrite').format('parquet').saveAsTable('weibodata')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weibodata').show()


    # =================================================================================================================
    # weibo评论
    schema5 = StructType().add('articleId', StringType(), nullable=True). \
        add('create_at', StringType(), nullable=True). \
        add('like_counts', StringType(), nullable=True). \
        add('region', StringType(), nullable=True). \
        add('content', StringType(), nullable=True). \
        add('authorName', StringType(), nullable=True). \
        add('authorGender', StringType(), nullable=True). \
        add('authorAddress', StringType(), nullable=True). \
        add('authorAvatar', StringType(), nullable=True)

        # 存储
    df5 = spark.read.format('csv'). \
        option('sep', ','). \
        option('header', True). \
        option('encoding', 'utf-8'). \
        schema(schema=schema5). \
        load('./weiboDetail.csv')
    # df.show()
    df5 = df5.withColumn('id', monotonically_increasing_id())
    # 数据清洗
    df5 = df5.drop_duplicates()  # 去除重复行
    # df=df.dropna()  # 删除包含缺失值的行

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    df5.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboComment'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()

    df5.write.mode('overwrite').format('parquet').saveAsTable('weiboComment')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboComment').show()


   # =================================================================================================================
    # weibo评论
    schema6 = StructType().add('word', StringType(), nullable=True). \
        add('count', StringType(), nullable=True). \
        add('scores', FloatType(), nullable=True)

        # 存储
    df6 = spark.read.format('csv'). \
        option('sep', ','). \
        option('header', True). \
        option('encoding', 'utf-8'). \
        schema(schema=schema6). \
        load('./NLP_hotWordWeibo.csv')
    # df.show()
    df6 = df6.withColumn('id', monotonically_increasing_id())
    # 数据清洗
    df6 = df6.drop_duplicates()  # 去除重复行
    # df=df.dropna()  # 删除包含缺失值的行

    # sql数据表存储
    # 连接远程大数据集群中node1的数据库，url、jdbc：3306、userSSL和编码
    df6.write.mode('overwrite'). \
        format('jdbc'). \
        option('url', 'jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8'). \
        option('dbtable', 'weiboHotword'). \
        option('user', 'root'). \
        option('password', 'root'). \
        option('encoding', 'utf-8'). \
        save()

    df6.write.mode('overwrite').format('parquet').saveAsTable('weiboHotword')  # 保存到tiebadata的数据库，数据形式为partuet
    spark.sql('select * from weiboHotword').show()
