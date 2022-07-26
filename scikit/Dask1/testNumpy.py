if __name__ == "__main__":
    import numpy as np

    print("ndarray************************************")
    a = np.array([1, 2, 3, 4, 5, 6])
    print(a)
    a1 = a[::2]
    print(a1.ndim)
    # 多于一个维度
    a = np.array([[1, 2], [3, 4]], order='C')
    print(a)
    a = np.array([[1, 2], [3, 4]], order='F')
    print(a)

    # 最小维度
    a = np.array([1, 2, 3, 4, 5], ndmin=2)
    print(a)

    # dtype 参数
    a = np.array([1, 2, 3], dtype=complex)
    print(a)
    print("dtype************************************")
    # 将数据类型应用于 ndarray 对象
    dt = np.dtype([('age', np.int8)])
    a = np.array([(10,), (20,), (30,)], dtype=dt)
    print(a)
    print(a['age'])
    student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
    a = np.array([('abc', 21, 50), ('xyz', 18, 75)], dtype=student)
    print(a)
    print(a['name'])
    print("数组属性************************************")

    a = np.arange(24)
    print(a.ndim)  # a 现只有一个维度
    # 现在调整其大小
    b = a.reshape(2, 4, 3)  # b 现在拥有三个维度
    print(b.ndim)
    print(b.shape)
    print(b.size)
    print(b.dtype)
    print(b.itemsize)
    print(b.flags)
    print(b.real)
    print(b.imag)
    print(b.data)

    print("创建数组************************************")
    x = np.empty([3, 2], dtype=int)
    print(x)
    # 创建指定大小的数组，数组元素以0来填充：
    # 默认为浮点数
    x = np.zeros(5)
    print(x)
    # 设置类型为整数
    y = np.zeros((5,), dtype=int)
    print(y)
    # 自定义类型
    z = np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4')])
    print(z)

    # 创建指定形状的数组，数组元素以1来填充
    # 默认为浮点数
    x = np.ones(5)
    print(x)
    # 自定义类型
    x = np.ones([2, 2], dtype=int)
    print(x)

    print("NumPy Mat plot lib************************************")
    from matplotlib import pyplot as plt

    x = np.arange(1, 11)
    y = 2 * x + 5
    plt.title("Matplotlib demo")
    plt.xlabel("x axis caption")
    plt.ylabel("y axis caption")
    plt.plot(x, y)
    plt.show()

    plt.title("Matplotlib demo")
    plt.xlabel("x axis caption")
    plt.ylabel("y axis caption")
    plt.plot(x, y, "ob")
    plt.show()

    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0, 3 * np.pi, 0.1)
    y = np.sin(x)
    plt.title("sine wave form")
    # 使用 matplotlib 来绘制点
    plt.plot(x, y)
    plt.show()

    x = [5, 8, 10]
    y = [12, 16, 6]
    x2 = [6, 9, 11]
    y2 = [6, 15, 7]
    plt.bar(x, y, align='center')
    plt.bar(x2, y2, color='g', align='center')
    plt.title('Bar graph')
    plt.ylabel('Y axis')
    plt.xlabel('X axis')
    plt.show()

    a = np.array([22, 87, 5, 43, 56, 73, 55, 54, 11, 20, 51, 5, 79, 31, 27])
    plt.hist(a, bins=[0, 20, 40, 60, 80, 100])
    plt.title("histogram")
    plt.show()

    aa = np.random.random((1000, 20))
    print(aa*100)
