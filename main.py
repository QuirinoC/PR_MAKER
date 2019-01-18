from challonge import challonge
import os

API_KEY=os.getenv("API_KEY")
user=os.getenv("user")

c = challonge(user,API_KEY)

print(c.get_tournament("Ultmazaranch2"))