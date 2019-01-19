from challonge import *
import os

API_KEY=os.getenv("API_KEY")
user=os.getenv("user")

c = challonge(user,API_KEY)


tournaments = [
    #"Mmxus3",
    "Ultmazaranch2",
    "Ultmazaranch1",
]

matches = [c.tournament_matches(t) for t in tournaments]

count = merge_count(matches)

print(power_rank(count))