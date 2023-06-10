from filemm import MMFile
import datetime


class MMPost:

    def __init__(self, post_info: dict) -> None:
        self.channel_id = post_info["channel_id"]
        self.create_at = post_info["create_at"]
        self.delete_at = post_info["delete_at"]
        self.edit_at = post_info["edit_at"]
        self.message = post_info["message"]

        if "file_ids" in post_info:
            self.file_ids = post_info["file_ids"]
        else:
            self.file_ids = []

        self.id = post_info["id"]
        self.user_id = post_info["user_id"]
        self.user = None
        self.files = []

        if len(self.file_ids) > 0:
            for f_info in post_info["metadata"]["files"]:
                self.files.append(MMFile(f_info))


    def __repr__(self) -> str:
        dt = datetime.datetime.fromtimestamp(self.create_at/1000).strftime("%m/%d/%Y, %H:%M:%S")
        file_paths = ""
        if len(self.files) > 0:
            file_paths = "IMAGE(s): "
            for file in self.files:
                file_path = file.upload_to_s3()
                file_paths += file_path + ", "
            file_paths += "\n\n"

        if not self.user:
            return f"{self.user_id} ({dt}): {self.message}\n" + file_paths
        else:
            return f"{self.user.first_name} {self.user.last_name} ({dt}): {self.message}\n" + file_paths