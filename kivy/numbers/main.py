from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.kivyagg import FigureCanvasKivyAgg
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# data fetching and processing
# Set the authorized user information
authorized_user_info = {
    "client_id":"877684305447-vcqgmavesu21bid9hnclj60b4k81kv56.apps.googleusercontent.com",
    "project_id":"numbers-372819",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":"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",
    "redirect_uris":["http://localhost"],
    "refresh_token":"1//04wlNsj33AMaDCgYIARAAGAQSNgF-L9Ir2NFkQVWr1_rd3Q5PsBl1qM7_KHuRbdBV0En7cDPwXMUHtBrymVKdkRxsZxvxR-vLjQ"
}

# Set the sheet ID and range for the data you want to fetch
SHEET_ID = '13ufTqDDPhACkQruhbHwnCsueHxEIedOHufmhaXZs2eU'
RANGE_NAME = 'Acquisitions!A1:Z'

# Authenticate with the Google Sheets API
# creds = mock.Mock(spec=credentials.Credentials)
creds = Credentials.from_authorized_user_info(info=authorized_user_info)
# print(creds.__dict__)
service = build('sheets', 'v4', credentials=creds)

# Set up a loop to fetch the data at intervals
# while True:
# Call the Sheets API to fetch the data
result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

# Convert the data into a Pandas DataFrame
df = pd.DataFrame(values[1:], columns=values[0])

# show full rows
pd.set_option('max_colwidth', None)

# Get the indexes of the rows to drop - the ones starting with k and the ones starting with 15000
idx = df[df['Till Number'].str.startswith('K')].index
card_accounts = df[df['Till Number'].str.startswith('4002')].index
other_card_account = df[df['Till Number'].str.startswith('150000')].index

# Drop the rows with those indexes
df.drop(idx, inplace=True)
df.drop(card_accounts, inplace=True)
df.drop(other_card_account, inplace=True)


df['First Transaction Date'] = pd.to_datetime(df['First Transaction Date'], infer_datetime_format=True, dayfirst=True)
df['Last Transaction Date'] = pd.to_datetime(df['Last Transaction Date'], infer_datetime_format=True, dayfirst=True)
df['2nd 30 Milestone Date'] = pd.to_datetime(df['2nd 30 Milestone Date'], infer_datetime_format=True, dayfirst=True)
df['1st 30 Milestone Date'] = pd.to_datetime(df['1st 30 Milestone Date'], infer_datetime_format=True, dayfirst=True)
df['3rd 30 Milestone Date'] = pd.to_datetime(df['3rd 30 Milestone Date'], infer_datetime_format=True, dayfirst=True, errors='raise')
df['Till Creation Date'] = pd.to_datetime(df['Till Creation Date'], infer_datetime_format=True, dayfirst=True, errors='raise')
df['Till Number'] = df['Till Number'].astype('str',errors='ignore')
df['Till Name'] = df['Till Name'].astype('str',errors='ignore')
df['Onboarder'] = df['Onboarder'].astype('str',errors='ignore')
df['Company Name'] = df['Company Name'].astype('str',errors='ignore')
df['Merchant Category'] = df['Merchant Category'].astype('str',errors='ignore')
df['Channel'] = df['Channel'].astype('str',errors='ignore')
df['County'] = df['County'].astype('str',errors='ignore')
df['Region'] = df['Region'].astype('str',errors='ignore')
df['Original Channel'] = df['Original Channel'].astype('str',errors='ignore')
df['Till Status'] = df['Till Status'].astype('str',errors='ignore')

df['1st 30 Transaction Volume'] = pd.to_numeric(df['1st 30 Transaction Volume'])
df['2nd 30 Transaction Volume'] = pd.to_numeric(df['2nd 30 Transaction Volume'])
df['3rd 30 Transaction Volume'] = pd.to_numeric(df['3rd 30 Transaction Volume'])

df['MonthYear'] = df['Till Creation Date'].dt.strftime('%Y-%m')


monthyears = df['MonthYear'].drop_duplicates().sort_values()

all_tv_data = []
for my in monthyears:

        month_name = 'month'+str(my)
        batch = df[df['MonthYear'] == my]
        new = len(batch)  
        firsttv = batch['1st 30 Transaction Volume'].sum()
        secondtv = batch['2nd 30 Transaction Volume'].sum()
        thirdtv = batch['3rd 30 Transaction Volume'].sum()

        all_tv_data.append([my,new,firsttv,secondtv,thirdtv])

# visualization for all_tv_data
# active months = last 13 months

dataset = all_tv_data[-13:]
# print(dataset)


# Extract the date values from the list of lists
dates = [item[0] for item in dataset]

# Extract the numerical values from the list of lists
# tills onboarded
tills = [item[1] for item in dataset]
# first30
ftv = [item[2] for item in dataset]
# second30
stv = [item[3] for item in dataset]
# third30
ttv = [item[4] for item in dataset]

# Create a line chart using the `plot` function
plt.bar(dates, tills)

# Add labels to the x and y axes
plt.xlabel('Date')
plt.ylabel('Tills')


class tvs(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))


    def save_it(self):
        pass

class Cops_db(Widget):
    pass


class CopsApp(App):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme.primary_palette = 'Orange'
        Builder.load_file('cops.kv')
        return tvs()


if __name__ == '__main__':
    CopsApp().run()
