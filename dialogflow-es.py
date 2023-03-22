from flask import Flask, request,jsonify
import json
import requests

app = Flask(__name__)

@app.route('/webhook',methods = ['GET','POST'])
def webhook():

    data = request.get_json(silent=True)
    if data['queryResult']['intent']['displayName'] == 'GetInfo':
        reply = fetch(data)
        return jsonify(reply)

def fetch(data):
    try:
        eamilToBeVerified = data['queryResult']['parameters']
        keys_with_values = [key for key, value in eamilToBeVerified.items() if value]
        print(keys_with_values)
        team = data['queryResult']['parameters']['team'][0]
        print(team)
        url = f'https://v3.football.api-sports.io/teams?league=1&season=2022&name={team}'
        payload={}
        headers = {
       'x-rapidapi-key': '<API-KEY>'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        if res['response']:
            print('id is: ',res['response'][0]['team']['id'])
            id = res['response'][0]['team']['id']
            url = f'https://v3.football.api-sports.io/teams/statistics?league=1&season=2022&team={id}'
            payload={}
            headers = {
            'x-rapidapi-key': '<API-KEY>'
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
            print('reached here')
            if 'info' in keys_with_values:
                print('reached 11')

                reply = {
                    'fulfillmentText': f'{team_name} has played total of {total_matches} matches, {home} at home and {outside_home} away. Among them, they won {wins} matches,drew {draws} and lost {loose}.'
                }

            elif 'lastOpponent' in keys_with_values:
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': '<API-KEY>'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                opponentTeam = result['response'][0]['teams']['away']['name']
                reply = {
                     'fulfillmentText': f'{opponentTeam}' 
                        }

            elif 'numGamesPlayed' in keys_with_values:
                print('reached')
                reply = {
                     'fulfillmentText': f'{team_name} have played {total_matches} matches so far' 
                        }

            elif 'leaguePosition' in keys_with_values:
                print('leaguePosition')
                url = f'https://v3.football.api-sports.io/standings?league=1&season=2022&team={id}'
                payload={}
                headers = {
                'x-rapidapi-key': '<API-KEY>',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                res = response.json()
                rank = res['response'][0]['league']['standings'][0][0]['rank']  
                played = res['response'][0]['league']['standings'][0][0]['all']['played']   
                win = res['response'][0]['league']['standings'][0][0]['all']['win']
                reply = {
                     'fulfillmentText': f'{team_name} are in {rank} place with {played} matches played and {win} wins' 
                        }

            elif 'manager' in keys_with_values:
                print('manager')
                url = f"https://v3.football.api-sports.io/coachs&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': '<API-KEY>',
                'x-rapidapi-host': 'v3.football.api-sports.io'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                managerName = result['response'][0]['name']
                reply = {
                     'fulfillmentText': f'{managerName}' 
                        }
                
            elif 'nextOpponent' in keys_with_values:
                print('nextOpponent')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': '<API-KEY>',
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
                     'fulfillmentText': f'{team_name} will play against {nextOpponent} on {dateV2}' 
                        }
            
            elif 'lastScore' in keys_with_values:
                print('lastscore')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': '<API-KEY>',
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
                     'fulfillmentText': f'{team_name} played their last game on {lastGameDate} against {lastOpponent} and they {status} the game by {home}-{away}.' 
                        }

            elif 'playingNow' in keys_with_values:
                print('lastscore')
                url = f"https://v3.football.api-sports.io/fixtures?league=1&season=2022&team={id}"
                payload={}
                headers = {
                'x-rapidapi-key': '<API-KEY>',
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
                     'fulfillmentText': f'{team_name} was not scheduled to play today their next game is against {lastOpponent} on {dateV2}'
                        }

    except Exception as e:
        print(e)

    return reply

if __name__ == '__main__':
    app.run(debug=True)