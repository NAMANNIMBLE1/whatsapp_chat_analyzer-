import re
import  pandas as pd

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)


    times_ = []
    dates_ = []
    for i in dates:
        dates_.append(i.split(", ")[0])
        times_.append(i.split(", ")[1])

    time_ = []

    for i in times_:
        time_.append(i.split("\u202f")[0])


    df = pd.DataFrame({
        "user_message": messages,
        "date": dates_,
        "time": time_
    })

    # splitting username and message
    user = []
    msg = []

    for i in df["user_message"]:
        x = re.split(r"([\w\W]+?):\s", i)  # splitting based on format
        if x[1:]:  # if exists
            user.append(x[1])
            msg.append(x[2])
        else:  # if not exists
            user.append('Group notification')
            msg.append(x[0])

    df['user'] = user
    df['msg'] = msg
    df.drop(columns=['user_message'], inplace=True)

    # Converting to datetime format
    df['date'] = pd.to_datetime(df['date'])
    # Extracting  year, month name, and day name
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()

    return  df



