from string import Template
from smhi import forecast_timestamps 
from datetime import datetime, timedelta
from collections import Counter 
from requests import post

TIMEFORMAT = '%Y-%m-%dT%H:%M:%SZ'

TIMESOFDAY = {
    (00, 11): "morning",
    (11, 13): "noon",
    (13, 18): "afternoon",
    (18, 23): "evening",
}

if __name__ == "__main__":
    with open("./prompt.system.txt", "r") as fp_system, open("./prompt.user.txt", "r") as fp_user, open("./longlat.txt") as fp_longlat:
        system_prompt = fp_system.read().strip()
        user_template = Template(fp_user.read().strip())
        long_lat = tuple(map(str.strip, fp_longlat.readlines()))
   
    forecast = {name: [] for name in TIMESOFDAY.values()}

    today = datetime.today()

    # This *should* be ran in the morning, but if it's during the day fetch tomorrows forecast
    if today.hour > 9:
        today += timedelta(days=1)

    for timestamp, code in forecast_timestamps(*long_lat):
        datetime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        if today.day != datetime.day or today.month != datetime.month or today.year != datetime.year:
            continue
        hour = datetime.hour 
        for (start, end), timeofday in TIMESOFDAY.items():
            if start <= hour and hour < end:
                forecast[timeofday].append(code)

    forecast = {timeofday: Counter(map(str.lower, codes)).most_common(1)[0][0] for timeofday, codes in forecast.items()}

    user_prompt = user_template.substitute(
            month=today.strftime('%B'), 
            day=today.day, 
            morning=forecast['morning'], 
            noon=forecast['noon'],
            afternoon=forecast['afternoon'],
            evening=forecast['evening'],
            )

    with open("apikey.txt", "r") as fp_apikey:
        apikey = fp_apikey.read().strip()

    headers = {
        "Authorization": f"Bearer {apikey}"
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    }

    url = "https://api.openai.com/v1/chat/completions"
    response = post(url, json=body, headers=headers)
    if not response.status_code == 200:
        print("Failed to generate prompt")
        print(response.text)
    else:
        print(response.json()['choices'][0]['message']['content'])
    

