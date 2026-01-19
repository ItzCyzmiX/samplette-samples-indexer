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

samples_data = []

def main():
    url = "https://youtube.com/playlist?list=PLW4NDfp3IicGyAw0Ix0Z0yr-FL35Eo_qB&si=C5iAT8adl0V1M90c"

    pl = Playlist(url)
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
