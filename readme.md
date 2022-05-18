
##### Python项目如何生成requirements.txt文件
```bash
使用 pip freeze 生成 会把整个Python环境下的所有包都列出生成
pip freeze > D:\pycharm\requirements.txt

使用 pipreqs 生成  只生成我们当前Python项目中所用到的依赖包及其版本号
pipreqs ./ --encoding=utf-8 --force
```