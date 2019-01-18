import requests
import json
#HTTPS enabled
API_URL="api.challonge.com/v1"


class challonge():
    def __init__(self,user, API_KEY):
        #Create url for requests
        self.url = f"https://{user}:{API_KEY}@{API_URL}"

    def get_tournament(self,code, as_json=True, include_participants=True, include_matches=True):
        """
            Returns 
        """
        request_url = f"{self.url}/tournaments/{code}{'.json'*as_json}?include_participants={1 if include_participants else 0}&include_matches={1 if include_matches else 0}"
        r = requests.get(request_url).json()
        return r
