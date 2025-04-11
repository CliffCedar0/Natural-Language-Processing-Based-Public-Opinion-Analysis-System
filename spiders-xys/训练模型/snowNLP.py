from snownlp import SnowNLP

from snownlp import sentiment

#重新训练模型
sentiment.train('./neg.txt', './pos.txt')
#保存新的训练模型
sentiment.save('sentiment.marshal')