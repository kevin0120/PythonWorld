from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance

X = [[1, 9, 9], [1, 9, 9], [1, 9, 9],
     [0, 9, 9], [0, 9, 9], [0, 9, 9]]
y = [1, 1, 1, 0, 0, 0]
clf = LogisticRegression().fit(X, y)
result = permutation_importance(clf, X, y, n_repeats=10,
                                random_state=0)

if __name__ == "__main__":
    # 构造一些数据点
    X = [[1, 9, 9], [1, 9, 9], [1, 9, 9],
         [0, 9, 9], [0, 9, 9], [0, 9, 9]]
    y = [1, 1, 1, 0, 0, 0]
    clf = LogisticRegression().fit(X, y)
    result = permutation_importance(clf, X, y, n_repeats=10,
                                    random_state=0)
    print(result)