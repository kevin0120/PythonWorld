# https://blog.csdn.net/uncle_ll/article/details/80861852

import cv2

im = cv2.imread('D:\Code\C#\PictureHandle\Resource\original.jpg')

sx1, sx2, sy1, sy2 = 100,100,800,800


cv2.rectangle(im,(int(sx1),int(sy1)),(int(sx2),int(sy2)),(0,255,0),3)

if (sy1 > 10):
    cv2.putText(im, "name", (int(sx1),int(sy1-6)), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (0, 255, 0) )
else:
    cv2.putText(im, "name", (int(sx1),int(sy1+15)), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (0, 255, 0) )

cv2.imwrite('new.jpg', im)

cv2.imshow('new.jpg', im)

cv2.waitKey(0)  # 鼠标点击图像 按空格键退出显示

cv2.destroyAllWindows()

print("Hello, World!")
