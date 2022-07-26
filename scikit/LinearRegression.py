# https://zhuanlan.zhihu.com/p/147297924
# https://blog.csdn.net/magicchu/article/details/51767409
import time
from sklearn.datasets import load_wine

if __name__ == "__main__":
    # 加载数据
    X, y = load_wine(return_X_y=True)

    # Estimators（估算器）
    from sklearn.linear_model import LogisticRegression, LinearRegression

    # from sklearn.naive_bayes import GaussianNB
    # 训练样本权重控制
    # https://blog.csdn.net/weixin_50304531/article/details/109717609
    # https://blog.csdn.net/qq_43391414/article/details/113144702
    lr = LinearRegression()

    # 拆分数据集--训练+练习
    from sklearn.model_selection import train_test_split

    # test_size 联系集所占比例 random_state：是随机数的种子不填或者None每次都会不一样,填了每次都一样
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

    # 根据训练集练习模型
    model = lr.fit(X_train, y_train)

    print("参数w={},b={}".format(model.coef_, model.intercept_))

    # 参数w = [-1.33715075e-01  3.15758889e-02 - 1.95120901e-01  4.24148960e-02
    #        - 1.67900484e-04  1.46565864e-01 - 3.40698477e-01 - 3.65954420e-01
    #        - 2.92059689e-03  6.64986251e-02 - 3.41715812e-01 - 2.75239546e-01
    #        - 6.43397509e-04], b = 3.938915627031553
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


    # 保存模型
    import joblib

    joblib.dump(model, r'./model/model.pkl')

    # 加载模型
    model_lgb = joblib.load(r'./model/model.pkl')

    # 根据训练集预测
    predictions1 = model_lgb.predict(X_train)


    while True:
        time.sleep(0.1)

# ps:增加权重会提高召回率,降低权重会提高准确率
