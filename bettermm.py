import requests
import shutil
from filemm import MMFile
from postmm import MMPost
from usermm import MMUser
from teamm import MMTeam
from channelmm import MMChannel
from exceptionmm import ResponseError, AuthError, UserNotFoundError
from conf import mm_auth, mm_conf


mm_url = mm_conf["url"]


class BetterMMDriver:

    def __init__(self) -> None:
        """
        access_token: personal access token used to authenticate with mattermost server
        """
        self._token = mm_auth["access-token"]

        resp = requests.get(f"{mm_url}/api/v4/teams", headers={"Authorization": f"Bearer {self._token}"})

        if resp.status_code != 200:
            raise AuthError(f"Mattermost authorization failed!:\n{resp.json()}")        

    
    def get_users_by_ids(self, ids: list[str]):

        assert type(ids) == list

        if len(ids) < 1:
            return []
        else:
            assert type(ids[0]) == str

        resp = requests.post(f"{mm_url}/api/v4/users/ids", headers={"Content-Type": "application/json", "Authorization": f"Bearer {self._token}"}, json=ids)

        ret = {}

        for user in resp.json():
            ret[user["id"]] = {
                "first": user["first_name"],
                "last": user["last_name"]
            }  

        return ret
    

    def get_teams(self) -> list[MMTeam]:

        resp = requests.get(f"{mm_url}/api/v4/teams", headers={"Authorization": f"Bearer {self._token}"})

        return [MMTeam(i) for i in resp.json()]
    

    def get_channels(self, num: int) -> list[MMChannel]:

        resp = requests.get(f"{mm_url}/api/v4/channels", params={"per_page": num}, headers={"Authorization": f"Bearer {self._token}"})

        return [MMChannel(i) for i in resp.json()]


    def get_channel_posts_by_id(self, id: str, num_posts: int = 60, before: str = None, silent = False) -> tuple[str, str]:
        """
        id:
            The id of the channel to get the posts for
        
        return:
            tuple of the form (poster id #, message, file_id #'s)
        """

        if num_posts > 200:
            if not silent:
                print(f"Too Many Posts Requested: {num_posts}, defaulting to 200")
            num_posts_corr = 200
        else:
            num_posts_corr = num_posts

        if not before:
            params = {"per_page": num_posts_corr}
        else:
            params = {"before": before}
    
        resp = requests.get(f"{mm_url}/api/v4/channels/{id}/posts", params=params, headers={"Authorization": f"Bearer {self._token}"})

        if resp.status_code != 200:
            print(resp.json())
            raise ResponseError(f"Status Code {resp.status_code} not expected: {resp.json()['message']}\n\tChannel ID: {id}")

        messages = resp.json()

        order = messages["order"]

        num_retreived = len(order)
        if num_retreived == 0: return []

        top_post_id = order[-1]

        posts = []

        for p_id in order:
            post = messages["posts"][p_id]

            posts.append(MMPost(post))

        if num_retreived < num_posts:
            return posts + self.get_channel_posts_by_id(id, num_posts-num_retreived, top_post_id, silent=silent)
        else:
            return posts
    

    def get_file_by_id(self, file: MMFile, file_name: str) -> bytes:

        resp = requests.get(f"{mm_url}/api/v4/files/{file.id}", headers={"Authorization": f"Bearer {self._token}"}, stream=True)

        with open(file_name, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)  


    def resolve_poster_info(self, posts: list[MMPost]) -> None:

        user_ids = [p.user_id for p in posts]
        
        # print(len(user_ids))

        resp_users = requests.post(f"{mm_url}/api/v4/users/ids", headers={"Content-Type": "application/json", "Authorization": f"Bearer {self._token}"}, json=user_ids)

        user_id_map = {u["id"]: MMUser(u) for u in resp_users.json()}

        for post in posts:
            if post.user_id not in user_id_map:
                raise UserNotFoundError(f"User info for {post.user_id} not retrieved")
            else:
                post.user = user_id_map[post.user_id]