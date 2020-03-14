import requests

url = 'https://free-api.heweather.net/s6/weather/forecast?location=平遥&key=e506974e3ab643cc842b4d6d4d095b5b'
res = requests.get(url)
print(res.text)


import json
import requests

url = 'https://free-api.heweather.net/s6/weather/forecast?location=广州&key=e506974e3ab643cc842b4d6d4d095b5b'
res = requests.get(url)
res = json.loads(res.text)	# 转换json数据为字典
result = res['HeWeather6'][0]['basic']
print(result)
# 这是所查询城市的经纬度，时区等等信息。
## {'cid': 'CN101280101', 'location': '广州', 'parent_city': '广州', 'admin_area': '广东', 'cnty': '中国', 'lat': '23.12517738', 'lon': '113.28063965', 'tz': '+8.00'}


import requests

url = 'https://free-api.heweather.net/s6/weather/forecast?location=广州&e506974e3ab643cc842b4d6d4d095b5b'
res = requests.get(url).json()		# 返回的数据为json格式
result = res['HeWeather6'][0]['daily_forecast']
print(result)
