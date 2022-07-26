# 朴素贝叶斯算法
# https://www.cnblogs.com/shirishiyue/p/4003498.html
# https://blog.csdn.net/qq_41133986/article/details/108111747
# https://zhuanlan.zhihu.com/p/259732614
# https://blog.csdn.net/Yemiekai/article/details/119081873
import time
from sklearn.datasets import load_wine

if __name__ == "__main__":
    # 加载数据
    X, y = load_wine(return_X_y=True)
    #
    # from sklearn.linear_model import LinearRegression
    # lr = LinearRegression()

    # Estimators（估算器）
    from sklearn.linear_model import LogisticRegression, LinearRegression

    # from sklearn.naive_bayes import GaussianNB
    # 训练样本权重控制
    # https://blog.csdn.net/weixin_50304531/article/details/109717609
    # https://blog.csdn.net/qq_43391414/article/details/113144702
    lr = LogisticRegression(max_iter=10000, class_weight={0: 0.49, 1: 0.49, 2: 0.02})

    # 拆分数据集--训练+练习
    from sklearn.model_selection import train_test_split

    # test_size 联系集所占比例 random_state：是随机数的种子不填或者None每次都会不一样,填了每次都一样
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

    # 根据训练集练习模型
    import numpy as np

    # sample_weight 可以提高某一条数据的的权重
    aa = y_train.copy()
    aa[aa == 0] = 100
    model = lr.fit(X_train, y_train, sample_weight=aa)

    # 参数说明
    # https://blog.csdn.net/u010099080/article/details/52933430
    print("参数w={},b={}".format(model.coef_, model.intercept_))

    # 根据练习集预测
    predictions = model.predict(X_test)

    # 计算分析错误率
    a = y_test.tolist()
    b = predictions.tolist()
    bb = 0
    for i in range(len(a)):
        if b[i] != a[i]:
            bb = bb + 1
    print('错误率{}'.format(bb / len(a)))

    # 模型评估 根据联系集预测
    from sklearn.metrics import classification_report

    print(classification_report(y_test, predictions))

    # 保存模型
    import joblib

    joblib.dump(model, r'./model/model.pkl')

    # 加载模型
    model_lgb = joblib.load(r'./model/model.pkl')

    # 根据训练集预测
    predictions1 = model_lgb.predict(X_train)
    print(classification_report(y_train, predictions1))

    while True:
        time.sleep(0.1)

# ps:增加权重会提高召回率,降低权重会提高准确率
