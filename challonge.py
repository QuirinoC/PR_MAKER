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
    
    def tournament_matches(self, tournament):
        t = self.get_tournament(tournament)
        participants = get_participants(t)
        matches = get_matches(participants, t)
        count = count_matches(matches)
        return count

def get_participants(tournament):
    participants = tournament['tournament']['participants']
    data = {}
    for p in participants:
        p = p['participant']
        data[p['id']] = {
            'name': p['display_name']
        }
    return data

def get_matches(participants, tournament):
    matches = tournament['tournament']['matches']
    data = {}
    for m in matches:
        m = m['match']
        data[m['id']] = {
            'winner': participants[m['winner_id']]['name'],
            'loser': participants[m['loser_id']]['name']
        }
    return data

def count_matches(matches):
    count = {}
    for id, data in matches.items():
        t = tuple([data['winner'], data['loser']])
        count[t] = 1 + count.get(t, 0)
    return count

def merge_count(matches_count):
    count = {}
    for match_count in matches_count:
        for match in match_count:
            count[match] = count.get(match,0) + match_count[match]
    return count


def power_rank(match_count, d=0.85):
    power = {}
    match_record = {
        'wins' : {},
        'loses': {}
    }
    #Extracts every player and sets power to 1
    for m in match_count:
        for player in m:
            power[player] = 0.5
        winner, loser = m
        match_record['wins'][winner] = match_record['wins'].get(winner, []) + [loser] * match_count[m]
        match_record['loses'][loser] = match_record['loses'].get(loser, []) + [winner] * match_count[m]

    for i in range(100000):
        for player in power:
            #Calculate the PR using the beaten players
            if player not in match_record['wins']: continue
            win_sum = 0
            for loser in match_record['wins'][player]:
                win_sum += (power[loser] / (power[player] + 0.0000001)) 
            

            #Calculate the PR using the players that beat current
            if player not in match_record['loses']: continue
            lose_sum = 0
            for winner in match_record['loses'][player]:
                lose_sum += (power[loser] / (power[winner] + 0.0000001)) 
            lose_sum = 0 #<- Remove
            power[player] = (1 - d) + d * (win_sum - lose_sum)
            

        #Normalize data
        #for player in power:
        #    min_val = min(power.values())
        #    max_val = max(power.values())
        #    power[player] = (power[player] - min_val) / (max_val - min_val)
                


    return sorted(power.items(), key=lambda x: x[1])