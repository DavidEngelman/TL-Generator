import pandas as pd
from datetime import datetime
import json


def dateToJson(o):
    if isinstance(o, datetime):
        return o.__str__()


class FileManager:

    @staticmethod
    def parse(fn):
        df = FileManager.preproc(fn)
        data = FileManager.to_json(df)

        return data

    @staticmethod
    def preproc(fn):
        df = pd.read_excel(fn, header=0)

        df.dropna(axis=1, how='all')

        df = df.rename(index=str, columns={"name event ": "name event"})

        for index, row in df.iterrows():
            row["Last Name"] = row["Last Name"].strip()
            if not pd.isnull(row["First name"]):
                row["First name"] = row["First name"].strip()
            if pd.isnull(row["date"]):
                df.drop(index, inplace=True)

        df['LastName FirstName'] = df['Last Name'].fillna('') + " " + df['First name'].fillna('')

        df = df.drop(columns=['Last Name', 'First name'])

        df = df[['LastName FirstName', "name event", 'date']]

        return df

    @staticmethod
    def to_json(df):
        people = df['LastName FirstName'].unique()

        timelines = []
        for p in people:

            timeline = {"name": p, "events": []}

            events = df.loc[df['LastName FirstName'] == p, 'name event']
            dates = df.loc[df['LastName FirstName'] == p, 'date']

            i = 1
            for event, date in zip(events, dates):
                timeline["events"].append(
                    {"id": i,
                     "content": event,
                     "start": date
                     }
                )
                i += 1

            timelines.append(timeline)


        return json.dumps(timelines, default=dateToJson)
