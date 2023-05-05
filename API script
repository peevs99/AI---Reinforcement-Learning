import requests
import json


class API:
    BASE_URL = 'https://www.notexponential.com/aip2pgaming/api'
    HEADERS = {
        'x-api-key': 'f74c3d7259e8ea471636',
        'userId': '1160',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    @classmethod
    def reset(cls, team_id):
        url = f"{cls.BASE_URL}/rl/reset.php?teamId={team_id}&otp=5712768807"
        response = requests.get(url, headers=cls.HEADERS)
        print("reset", response.json())
        return response.json()

    @classmethod
    def get_runs(cls, team_id, count):
        url = f"{cls.BASE_URL}/rl/gw.php?type=runs&teamId={team_id}&count={count}"
        response = requests.get(url, headers=cls.HEADERS)
        print("get_runs", response.json())
        return response.json()

    @classmethod
    def get_location(cls, team_id):
        url = f"{cls.BASE_URL}/rl/gw.php?type=location&teamId={team_id}"
        response = requests.get(url, headers=cls.HEADERS)
        print("get_location", response.json())
        return response.json()

    @classmethod
    def enter_world(cls, world_id, team_id):
        url = f"{cls.BASE_URL}/rl/gw.php"
        payload = {
            'type': 'enter',
            'worldId': world_id,
            'teamId': team_id
        }
        response = requests.post(url, headers=cls.HEADERS, data=payload)
        print("enter_world", response.json())
        return response.json()

    @classmethod
    def make_move(cls, team_id, move, world_id):
        url = f"{cls.BASE_URL}/rl/gw.php"
        payload = {
            'type': 'move',
            'teamId': team_id,
            'move': move,
            'worldId': world_id
        }
        response = requests.post(url, headers=cls.HEADERS, data=payload)
        print("make_move", move, response.json())
        return response.json()

    @classmethod
    def get_score(cls, team_id):
        url = f"{cls.BASE_URL}/rl/score.php?type=score&teamId={team_id}"
        response = requests.get(url, headers=cls.HEADERS)
        # print("get_score", response.json())
        return response.json()
