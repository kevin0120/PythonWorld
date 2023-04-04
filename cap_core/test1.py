import tsfresh as tsf
import pandas as pd

print("hello world")
x = [1, 2, 3, 4, 4]
if __name__ == '__main__':
    # abs_energy(x)
    ts = pd.Series(x)  # 数据x假设已经获取
    ae = tsf.feature_extraction.feature_calculators.abs_energy(ts)

    # absolute_sum_of_changes(x)
    ae1 = tsf.feature_extraction.feature_calculators.absolute_sum_of_changes(ts)

    print("hello world")
