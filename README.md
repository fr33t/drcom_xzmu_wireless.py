# drcom_xzmu_wireless.py
西藏民族大学校园网 WIFI 登陆脚本

# 前置条件
安装 python3

安装 requests
```zsh
pip install requests
```

# 配置你的信息
##  在 drcom_xzmu_wireless.py 里配置你的凭证
```python
stu_number = "学号"
stu_passwd = "密码"
```

## win版
编辑 drcom_xzmu_wireless_4win.py

安装依赖 requirements.txt

```cmd
pyinstaller -F -w --hidden-import plyer.platforms.win.notification .\drcom_xzmu_wireless_4win.py
```

生成dist/xx.exe

拷贝到
win+R 输入shell:startup
