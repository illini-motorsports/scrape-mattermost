

class MMChannel:

    def __init__(self, ch_info: dict):
        self.id = ch_info["id"]
        self.create_at = ch_info["create_at"]
        self.team_id = ch_info["team_id"]
        self.type = ch_info["type"]
        self.display_name = ch_info["display_name"]
        self.name = ch_info["name"]
        self.header = ch_info["header"]
        self.total_msg_count = ch_info["total_msg_count"]
        self.creator_id = ch_info["creator_id"]
        self.team_display_name = ch_info["team_display_name"]
        self.team_name = ch_info["team_name"]
        self.policy_id = ch_info["policy_id"]


    def __repr__(self):
        return f"MMChannel({self.name})"