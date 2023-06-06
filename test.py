from mattermostdriver import Driver
import yaml

auth_file = open('token.yml', 'r')
auth = yaml.load(auth_file, yaml.CLoader)

d = Driver({
    "url": "mattermost.motorsports.illinois.edu",
    "token": auth["Access-Token"],
    "port": 443
})

d.login()

team_ids = [t["id"] for t in d.teams.get_teams()]
    