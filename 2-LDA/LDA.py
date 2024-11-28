# coding='utf-8'
import os
import datetime
import warnings
import pandas as pd
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import corpora, similarities, models
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
warnings.filterwarnings("ignore")

# 读取分词好的文本文件
def infile(filepath,wordstop):
    train = []
    with open(filepath, 'r', encoding='utf8') as fp:
        for line in fp:
            new_line = []
            if len(line) > 1:
                line = line.strip().split(' ')
                for w in line:
                    if len(w) > 1 and w not in wordstop:
                        new_line.append(w)
            if len(new_line) > 1:
                train.append(new_line)
    return train

# 处理文本数据
def deal(train):
    id2word = corpora.Dictionary(train)     # 创建词典
    texts = train                          # 创建语料库
    corpus = [id2word.doc2bow(text) for text in texts]   # 词频矩阵

    # 使用 TF-IDF（词频-逆文档频率模型）
    tfidf = models.TfidfModel(corpus)
    corpus = tfidf[corpus]

    # 保存词典和语料库
    os.makedirs('tmp', exist_ok=True)
    id2word.save('tmp/deerwester.dict')
    corpora.MmCorpus.serialize('tmp/deerwester.mm', corpus)

    return id2word, texts, corpus

# 运行标准 LDA 模型
def run(corpus_1, id2word_1, num, texts):
    lda_model = LdaModel(corpus=corpus_1,
                         id2word=id2word_1,
                         num_topics=num,
                         passes=60,
                         alpha=(50 / num),
                         eta=0.01,
                         random_state=42)

    # 困惑度
    perplex = lda_model.log_perplexity(corpus_1)

    # 一致性
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word_1, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()

    return lda_model, coherence_lda, perplex

# 保存 LDA 可视化结果
def save_visual(lda, corpus, id2word, name):
    d = gensimvis.prepare(lda, corpus, id2word)
    pyLDAvis.save_html(d, name + '.html')

if __name__ == '__main__':
    # 文本名
    stopwords =[line.strip() for line in open('stopWords.txt',encoding='utf-8').readlines()]
    train = infile('西游记-分词.txt',stopwords)
    # 处理数据
    id2word, texts, corpus = deal(train)

    # # 训练标准 LDA 模型
    # perplexity = []            #困惑度数组
    # coherence_values = []      #一致性数组
    # model_list = []
    # for num_topics in range(2, 21, 1):
    #     lda, coherence_lda, perplex = run(corpus, id2word,num_topics, texts)
    #     model_list.append(lda)
    #     perplexity.append(perplex)
    #     coherence_values.append(coherence_lda)
    #
    # #绘制Perplexity - Coherence - Topic折线图
    # plt.figure(figsize=(16, 5), dpi=200)
    # x = range(2, 21, 1)
    # ax1 = plt.subplot(1, 2, 1)
    # plt.plot(x, perplexity)
    # plt.xlabel("Num Topics")
    # plt.ylabel("Perplexity score")
    # plt.xticks(range(1, 21, 2))  # 设置刻度
    # plt.title('困惑度',fontproperties="SimHei")
    # plt.grid(True, alpha=0.5)
    # ax2 = plt.subplot(1, 2, 2)
    # plt.plot(x, coherence_values)
    # plt.xlabel("Num Topics")
    # plt.ylabel("Coherence score")
    # plt.xticks(range(1, 21, 2))  # 设置刻度
    # plt.title('一致性',fontproperties="SimHei")
    # plt.grid(True, alpha=0.5)
    # plt.savefig('./困惑度与一致性.png', dpi=300)

    now = datetime.datetime.now()
    current_time = now.time()
    nicetopicnum = input(f"当前时间:{current_time} " + "请输入最佳主题数:")
    print(f"最佳主题数为{nicetopicnum}")

    lda, coherence_lda, perplex = run(corpus, id2word, int(nicetopicnum), texts)
    topic_list = lda.print_topics()

    #保存主题列表
    with open('xyj_topics.txt', 'w', encoding='utf-8') as f:
        for t in topic_list:
            f.write(' '.join(str(s) for s in t) + '\n')

    #保存LDA可视化结果
    save_visual(lda, corpus, id2word, 'xyj')