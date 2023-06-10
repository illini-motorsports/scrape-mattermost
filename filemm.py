from __future__ import annotations
import boto3
import requests
from uuid import uuid4
import os
import shutil
from conf import conf, mm_conf, mm_auth, s3_conf, s3



class MMFile():

    def __init__(self, file_info: dict) -> None:
        self.create_at = file_info["create_at"]
        self.extension = file_info["extension"]
        self.id = file_info["id"]
        self.mime_type = file_info["mime_type"]
        self.mini_preview = file_info["mini_preview"]
        self.name = file_info["name"]
        self.post_id = file_info["post_id"]
        self.size = file_info["size"]
        self.user_id = file_info["user_id"]


    def upload_to_s3(self) -> str:        
        f_id = str(uuid4())
        file_name = f_id + "." + self.extension

        resp = requests.get(f"{mm_conf['url']}/api/v4/files/{self.id}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {mm_auth['access-token']}"}, stream=True)

        with open(file_name, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)

        if not conf["debug"]:
            res = s3.meta.client.upload_file(Filename=file_name, Bucket=s3_conf["bucket-name"], Key=f_id)
        else:
            res = None
        
        assert res == None

        os.remove(file_name)

        return f"https://{s3_conf['bucket-name']}.s3.{s3_conf['region']}.amazonaws.com/{f_id}"
