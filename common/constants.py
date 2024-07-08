import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
# url -> [start download time, end download time]
CLIPS_URLS_DICT = {
    "https://www.youtube.com/watch?v=L0HTZ0XBv_o&ab_channel=Wimbledon": [15, 65],
    "https://www.youtube.com/watch?v=OthPga0vEkE&ab_channel=Wimbledon": [15, 65],
    "https://www.youtube.com/watch?v=XVrOXUAsqmQ&ab_channel=Wimbledon": [15, 65],
}
