# Rsign_and_Rtoken
融通基金微信端、h5，Rsign和Rtoken js逆向，mitmproxy 脚本。 
```bash
URL：https://wx.rtfund.com/gbusweb/msitepro/#/account/login
```
## 依赖
- 测试环境：python 3.11.6
```bash
pip install mitmproxy
pip install gmssl
pip install pycryptodome
```

## 启动mitmproxy
```bash
mitmweb -p 8888 --set scripts=yourPath\mitmproxy.py # 监听8888端口
```

访问：`http://127.0.0.1:8081 ` webUI mitmproxy 可视化，低配网页版burp

### 下载mitmproxy证书

先给浏览器挂上 127.0.0.1:8888 的代理，访问：http://mitm.it/ 下载对应操作系统的证书，安装为【受系统信任的根证书颁发机构】

关闭浏览器代理 127.0.0.1:8888 ,浏览器再挂 burp的代理 127.0.0.1:8080 。
在burp的proxy 中设置上游代理（upstream proxy servers）添加：127.0.0.1:8888

### 截图
![image](https://github.com/r1is/Rsign_and_Rtoken/assets/21257485/2724d0bd-fdd4-463b-8374-726d12bd44d7)
