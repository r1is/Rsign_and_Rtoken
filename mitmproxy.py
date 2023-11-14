
from mitmproxy import http
import random
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import urllib.parse
from gmssl import sm3,func

RT_HOST = "wx.rtfund.com"

def request(flow: http.HTTPFlow) -> None:
    headers = flow.request.headers
    body = flow.request.content
    host = flow.request.host

    if flow.request.method == "POST" and host == RT_HOST:
        headers['Rtoken'] = get_r_token()
        str_body = body.decode("utf-8")
        headers['Rsign'] = get_rt_sign(str_body)

        print("url:",flow.request.url)
        print("Rtoken:",headers['Rtoken'])
        print("Rsign:",headers['Rsign'])
        print("body:",str_body)
        print("=" * 50)

def response(flow: http.HTTPFlow) -> None:
    host = flow.request.host
    if host == RT_HOST:
        print("Response intercepted:")
        print(f"URL: {flow.request.url}")
        print(f"Status Code: {flow.response.status_code}")
        print("Headers:")
        for key, value in flow.response.headers.items():
            print(f"  {key}: {value}")
        print("Content:")
        print(flow.response.content.decode("utf-8", "replace"))
        print("=" * 50)
    
def AES_CBC_PKCS7(text,key = 'B49A86FA425D439d', iv = 'B49A86FA425D439d'):
    """
    text : 需要加密的明文
    key : 密钥
    iv : 向量（偏移量）
    """
    # CBC 模式
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    # pkcs7 填充
    padded_text = pad(text.encode(), AES.block_size, style='pkcs7')
    ciphertext = cipher.encrypt(padded_text)
    return base64.b64encode(ciphertext).decode()

# 随机字符串生成
generate_random = lambda n: "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n))

def get_r_token():
    try:
        e = "rtwxapp" + "|" + str(int(time.time()) * 1000) + "|" + generate_random(10)
        # print(e)
        encryData = AES_CBC_PKCS7(e)
        return urllib.parse.quote(encryData) # encodeURIComponent

    except Exception as e:
        print(e)

def get_rt_sign(n):
    # 进行两次URL解码
    decoded_str = urllib.parse.unquote(urllib.parse.unquote(n))
    #print(decoded_str)
    # 对解码后的字符串按照 & 分割，排序后再连接起来
    sorted_str = "&".join(sorted(decoded_str.split("&"))) + "&key=rtmsite"
    #print(sorted_str)
    # 计算 sm3 摘要
    data_byte = sorted_str.encode('utf-8')
    hash_data = sm3.sm3_hash(func.bytes_to_list(data_byte))
    return hash_data

if __name__ == "__main__":
    print(get_r_token())
    print(get_rt_sign("123"))
