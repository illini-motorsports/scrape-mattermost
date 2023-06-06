from mattermostdriver import Driver
import yaml
from collections import defaultdict
import pprint

pp = pprint.PrettyPrinter(indent=4)

auth_file = open('token.yml', 'r')
auth = yaml.load(auth_file, yaml.CLoader)

d = Driver({
    "url": "mattermost.motorsports.illinois.edu",
    "token": auth["Access-Token"],
    "port": 443
})

d.login()

# teams = [(t["name"], t["id"]) for t in d.teams.get_teams()]
# team_ids = {t[0]: t[1] for t in teams}

# channels = defaultdict(list)

# for team_name, team_id in teams:
#     for channel in d.channels.search_channels(team_id):
#         channels["team_name"].append(channel)

print(len(d.client.get(f"/channels/isg6cwttn3rbink85ys91ajuee/posts")["posts"].keys()))