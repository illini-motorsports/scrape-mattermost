from bettermm import BetterMMDriver
from writermm import write_to_file
import yaml
import os.path
from tqdm import tqdm


driver = BetterMMDriver()

channels = driver.get_channels(200)

for c in tqdm(channels):
    # if os.path.exists(f"{c.name}.txt"):
    #     continue

    posts = driver.get_channel_posts_by_id(c.id, 10000, silent=True)

    driver.resolve_poster_info(posts)

    write_to_file(f"output/{c.name}.txt", posts)