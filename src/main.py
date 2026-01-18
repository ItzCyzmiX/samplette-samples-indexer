import os
from pytubefix import Playlist
import librosa
import numpy as np
import supabase
from time import sleep
import random

from keyfinder import Tonal_Fragment
from tagger import tag_sample

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

client = supabase.create_client(
    "https://bqeqkydtmghlnnydjcsk.supabase.co",
    os.getenv("SUPABASE_KEY")
)

PROXIES = []

samples_data = []

PROXIES = [
    'socks4://41.169.151.154:4153',
    'socks4://198.8.94.174:39078',
    'socks4://167.71.65.149:1080',
    'socks4://31.43.33.55:4153',
    'socks4://36.95.189.165:5678',
    'socks4://46.38.41.150:58357',
    'socks4://200.192.236.242:1080',
    'socks4://124.248.184.144:1080',
    'socks4://196.0.113.10:31651',
    'socks4://171.248.216.79:1080',
    'socks4://202.40.177.94:5678',
    'socks4://47.238.60.156:8008',
    'socks4://171.248.208.241:1080',
    'socks4://202.131.159.61:5678',
    'socks4://200.108.190.110:9800',
    'socks4://141.94.70.195:46797',
    'socks4://178.130.47.129:1082',
    'socks4://49.207.177.65:5678',
    'socks4://187.63.9.62:63253',
    'socks4://96.36.50.99:39593',
    'socks4://61.9.34.118:58765',
    'socks4://40.134.10.174:18351',
    'socks4://171.248.217.140:1080'
]

def main():
    url = "https://youtube.com/playlist?list=PLW4NDfp3IicGyAw0Ix0Z0yr-FL35Eo_qB&si=C5iAT8adl0V1M90c"

    pl = Playlist(url, proxies={"https": f"socks5://{random.choice(IPS)}"})
    for video in pl.videos[:40]:  

        ys = video.streams.get_audio_only()
        ys.download(filename=f"{video.title}.m4a")
        

        audio_file_path = f"{video.title}.m4a" 
        y, sr = librosa.load(audio_file_path)
        

        bpm, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        tonal_fragment = Tonal_Fragment(y, sr)

        tags, all_scores = tag_sample(y, sr, bpm)

        props = {
            "yt_id": video.video_id,
            "title": video.title,
            "url": video.watch_url,
            "views": video.views,
            "likes": video.likes,
            "bpm": bpm.astype(int)[0].item(),
            "tags": tags,
            "key": tonal_fragment.key,
            "scale": tonal_fragment.scale,
            "duration": int(video.length),
            "author": video.author,
        }

        
        try: 
            with open(audio_file_path, "rb") as f:
                response = (
                    supabase.storage
                    .from_("samples")
                    .upload(
                        file=f,
                        path="public/" + video.video_id + ".m4a",
                        file_options={"cache-control": "3600", "upsert": "false"}
                    )
                )
            samples_data.append(props)
            print(f"Added sample: {video.title} by {video.author}")
        except Exception as e:
            print("Error uploading to Supabase Storage:", e)
        finally:
            os.remove(audio_file_path)

        sleep(2)

    try:
        client.table("samples").insert(samples_data).execute()
    except Exception as e:
        print("Error uploading to Supabase:", e)


if __name__ == "__main__":
    main()