

class MMTeam:

    def __init__(self, team_info: dict):
        self.id = team_info["id"]
        self.create_at = team_info["create_at"]
        self.name = team_info["name"]
        self.description = team_info["description"]
        self.type = team_info["type"]


    def __repr__(self):
        return f"MMTeam({self.name})"