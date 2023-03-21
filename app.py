import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/dialogflow', methods=['GET', 'POST'])
def dialogflow():

    data = request.get_json()
    if data['pageInfo']['displayName'] == 'GetInfo':
        reply = fetch(data)
        return jsonify(reply)

def fetch(data):
    try:
        parameters = data["intentInfo"]["parameters"]
    
        # Extract the parameter you want to keep
        print(parameters)
        if 'team' not in data['intentInfo']['parameters']:
            reply = {
                'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': [f'Make sure you have write about the team as well']
                        }
                    }
                ]
            }
        }
        team = data['sessionInfo']['parameters']['team']
        print(team)
        url = f'https://v3.football.api-sports.io/teams?league=1&season=2022&name={team}'
        payload={}
        headers = {
       'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        if res['response']:
            print('id is: ',res['response'][0]['team']['id'])
            id = res['response'][0]['team']['id']
            url = f'https://v3.football.api-sports.io/teams/statistics?league=1&season=2022&team={id}'
            payload={}
            headers = {
            'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            res = response.json()
            team_name = res['response']['team']['name']
            total_matches = res['response']['fixtures']['played']['total']
            home = res['response']['fixtures']['played']['home']
            outside_home = res['response']['fixtures']['played']['away']
            wins = res['response']['fixtures']['wins']['total']
            draws = res['response']['fixtures']['draws']['total']
            loose = res['response']['fixtures']['loses']['total']
            print('check1')
            if 'info' in data['intentInfo']['parameters'].keys():
                print('reached 11')

                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{team_name} has played total of {total_matches} matches, {home} at home and {outside_home} away. Among them, they won {wins} matches,drew {draws} and lost {loose}.']
                                }
                            }
                        ]
                    }
                }

            elif 'numgamesplayed' in data['intentInfo']['parameters'].keys():
                print('reached')
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{team_name} have played {total_matches} matches so far']
                                }
                            }
                        ]
                    }
                }

            elif 'leagueposition' in data['intentInfo']['parameters'].keys():
                print('leaguePosition')
                url = f'https://v3.football.api-sports.io/standings?league=1&season=2022&team={id}'
                payload={}
                headers = {
                'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                res = response.json()
                rank = res['response'][0]['league']['standings'][0][0]['rank']  
                played = res['response'][0]['league']['standings'][0][0]['all']['played']   
                win = res['response'][0]['league']['standings'][0][0]['all']['win']
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{team_name} are in {rank} place with {played} matches played and {win} wins']
                                }
                            }
                        ]
                    }
                }

            elif 'lastOpponent' in data['intentInfo']['parameters'].keys():
                print('lastOpponent')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                opponentTeam = result['response'][0]['teams']['away']['name']
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{opponentTeam}']
                                }
                            }
                        ]
                    }
                }
            elif 'manager' in data['intentInfo']['parameters'].keys():
                print('manager')
                url = f"https://v3.football.api-sports.io/coachs&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                managerName = result['response'][0]['name']
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{managerName}']
                                }
                            }
                        ]
                    }
                }
            elif 'nextopponent' in data['intentInfo']['parameters'].keys():
                print('nextOpponent')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                nextGameDate = result['response'][0]['fixture']['date']
                print(nextGameDate)
                y,m,d = nextGameDate.split('T')[0].split('-')
                y=2023
                dateV2 = str(y) + '-' + str(m) + '-' + str(d)
                nextOpponent = result['response'][0]['teams']['away']['name']
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{team_name} will play against {nextOpponent} on {dateV2}']
                                }
                            }
                        ]
                    }
                }
            
            elif 'lastscore' in data['intentInfo']['parameters'].keys():
                print('lastscore')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                lastGameDate = result['response'][0]['fixture']['date'].split('T')[0]
                lastOpponent = result['response'][0]['teams']['away']['name']
                winner = result['response'][0]['teams']['home']['winner']
                home = result['response'][0]['goals']['home']
                away = result['response'][0]['goals']['away']
                status = 'Loose'
                if winner:
                    status = 'won'
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{team_name} played their last game on {lastGameDate} against {lastOpponent} and they {status} the game by {home}-{away}.']
                                }
                            }
                        ]
                    }
                }

            elif 'playingnow' in data['intentInfo']['parameters'].keys():
                print('lastscore')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': 'api-key',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                nextGameDate = result['response'][0]['fixture']['date']
                y,m,d = nextGameDate.split('T')[0].split('-')
                y=2023
                dateV2 = str(y) + '-' + str(m) + '-' + str(d)
                lastOpponent = result['response'][0]['teams']['away']['name']
                winner = result['response'][0]['teams']['home']['winner']
                home = result['response'][0]['goals']['home']
                away = result['response'][0]['goals']['away']
                status = 'Loose'
                if winner:
                    status = 'won'
                reply = {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [f'{team_name} was not scheduled to play today their next game is against {lastOpponent} on {dateV2}']
                                }
                            }
                        ]
                    }
                }

    except Exception as e:
        print(e)

    return reply

if __name__ == '__main__':
    app.run(debug=True)