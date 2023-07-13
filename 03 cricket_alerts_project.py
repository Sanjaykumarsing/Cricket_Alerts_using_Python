import requests
import json
from datetime import datetime

class ScoreGet:
    def __init__(self):
        """
        Declaring the endpoints, apikey
        """
        self.url_get_all_matches = "https://api.cricapi.com/v1/currentMatches"
        self.url_get_score = "https://api.cricapi.com/v1/cricScore"
        self.api_key = "Enter API key"
        self.unique_id = "9759d12a-14a6-42c2-bbe2-833c6f612ceb"  # unique to every match

    def get_unique_id(self):
        
        """
        Returns Indian cricket teams match id, if the match is Live
        :return:
        """
        uri_params = {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, params=uri_params)
        resp_dict = resp.json()
        uid_found = 0
        for i in resp_dict['data']:
            if (i['teams'] == "Royal Challengers Bangalore", "Gujarat Titans" and i['matchStarted']):
                todays_date = datetime.today().strftime('%Y-%m-%d')
                todays_date = "2023-05-21"
                if todays_date == i['date']:
                    uid_found = 1
                    self.unique_id = i['id']
                    break
        if not uid_found:
            self.unique_id = -1

        send_data = self.get_score(self.unique_id)
        return send_data

    def get_score(self, unique_id):
        data = ""  # stores the cricket match data
        if unique_id == -1:
            data = "No today match/Match not started yet"
        else:
            uri_params = {"apikey": self.api_key, "id": self.unique_id}
            resp = requests.get(self.url_get_score, params=uri_params)
            data_json = resp.json()
            try:
                 data = data_json['data'][20]['matchType'] + "\n" + data_json['data'][20]['status'] + "\n" +  "Here's the score :\n" + data_json['data'][20]['t1'] + ": " + data_json['data'][20]['t1s'] + "\n" + data_json['data'][20]['t2'] +": " + data_json['data'][20]['t2s']
            except KeyError as e:
                data ="Somethong Went Wrong"
        return data


if __name__ == "__main__":
    match_obj = ScoreGet()
    send_message = match_obj.get_unique_id()
    print(send_message)
    
    from twilio.rest import Client
    account_sid = 'Enter account sid'
    auth_token = 'Enter auth token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=send_message, 
        to='whatsapp:Enter number here'
    )

    print('message has been send plz check the your whatsapp message')
