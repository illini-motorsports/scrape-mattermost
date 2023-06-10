from __future__ import annotations


class MMUser():

    def __init__(self, user_info: dict) -> None:
        self.create_at = user_info["create_at"]
        self.id = user_info["id"]
        self.username = user_info["username"]
        self.email = user_info["email"]
        self.nickname = user_info["nickname"]
        self.first_name = user_info["first_name"]
        self.last_name = user_info["last_name"]


    @staticmethod
    def create_files(ids: list[str]) -> list[MMUser]:
        pass