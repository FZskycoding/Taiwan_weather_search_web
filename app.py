from flask import Flask, render_template, request
import requests
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#input:地點 output:天氣資訊
def get_weather_data(location):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": os.getenv('API_KEY'),
        "format": "JSON",
        "locationName": location
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data


def simplify_data(data):
    location_data = data['records']['location'][0] #取出位置部分資訊
    weather_elements = location_data['weatherElement']#取出天氣部分資訊

    simplified_data = {
        'location': location_data['locationName'],
    }

    for element in weather_elements:
        element_name = element['elementName']
        for time in element['time']:
            start_time = time['startTime']
            if start_time not in simplified_data:
                simplified_data[start_time] = {}

            parameter = time['parameter']
            parameter_str = parameter['parameterName']
            if 'parameterUnit' in parameter:
                parameter_str += f" {parameter['parameterUnit']}"

            end_time = time['endTime']
            if end_time not in simplified_data[start_time]:
                simplified_data[start_time][end_time] = {}

            simplified_data[start_time][end_time][element_name] = parameter_str

    return simplified_data

# 回傳目前的天氣資訊的部分
def get_current_weather(simplified_data):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for start_time in simplified_data:
        if start_time == 'location':
            continue
        for end_time in simplified_data[start_time]:
            if start_time <= now <= end_time:
                return simplified_data[start_time][end_time]
            else:
                return simplified_data[start_time][end_time]
    return None

#檢查輸入的內容有沒有符合台灣縣市名稱 input:輸入訊息 output:縣市名稱
def check_location_in_message(message):
    locations = [
        "臺北市", "臺中市", "臺南市", "高雄市", "新北市", "桃園市", "新竹市", "苗栗縣",
        "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣",
        "臺東縣", "澎湖縣"
    ]

    corrected_message = re.sub("台", "臺", message)
    local = corrected_message.split("_")

    for location in locations:
        if re.search(local[0], location):
            return location
    return locations[0] #如果沒有符合的內容，顯示"臺北市"


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    city_input = ''
    if request.method == 'POST':
        city_input = request.form.get('city')
        location = check_location_in_message(city_input)
        weather_data = get_weather_data(location)
        simplified_data = simplify_data(weather_data)
        current_weather = get_current_weather(simplified_data)
        print(current_weather)

        if current_weather:
            weather_info = {
                'location': location,
                'Wx': current_weather.get('Wx', 'N/A'), #如果 Wx 不存在，回傳預設值 'N/A'
                'PoP': current_weather.get('PoP', 'N/A'),
                'CI': current_weather.get('CI', 'N/A'),
                'MinT': current_weather.get('MinT', 'N/A'),
                'MaxT': current_weather.get('MaxT', 'N/A')
            }

    return render_template('index.html', weather=weather_info, city=city_input)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
