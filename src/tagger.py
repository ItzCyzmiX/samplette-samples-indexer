import librosa
import numpy as np

def extract_features(y, sr, tempo):

    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))

    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    rms = np.mean(librosa.feature.rms(y=y))

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_var = np.var(mfcc)

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    harmonic_strength = np.mean(chroma)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_density = np.mean(onset_env)

    return {
        "tempo": tempo,
        "centroid": centroid,
        "bandwidth": bandwidth,
        "rolloff": rolloff,
        "zcr": zcr,
        "rms": rms,
        "mfcc_var": mfcc_var,
        "harmonic": harmonic_strength,
        "onset": onset_density
    }

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def norm(x, lo, hi):
    return clamp((x - lo) / (hi - lo))

def score_tags(f):
    scores = {}

    scores["upbeat"] = norm(f["tempo"], 90, 160)
    scores["chill"] = 1 - scores["upbeat"]

    scores["groovy"] = clamp(norm(f["onset"], 0.2, 1.2) * norm(f["tempo"], 90, 130))
    scores["funky"] = clamp(scores["groovy"] * norm(f["harmonic"], 0.2, 0.8))

    scores["jazzy"] = clamp(norm(f["centroid"], 1800, 3500) * norm(f["harmonic"], 0.3, 1.0))

    scores["breakbeat"] = clamp(norm(f["zcr"], 0.05, 0.2) * norm(f["onset"], 0.5, 1.5))
    scores["percussive"] = norm(f["onset"], 0.3, 1.5)

    scores["ambient"] = clamp((1 - norm(f["onset"], 0.3, 1.0)) * (1 - norm(f["tempo"], 80, 140)))
    scores["melodic"] = norm(f["harmonic"], 0.3, 1.0)

    scores["lofi"] = clamp((1 - norm(f["centroid"], 1500, 4000)) * norm(f["zcr"], 0.03, 0.12))
    scores["vintage"] = clamp(scores["lofi"] * (1 - norm(f["bandwidth"], 1000, 4000)))

    scores["electronic"] = norm(f["rolloff"], 3000, 7000)
    scores["experimental"] = norm(f["mfcc_var"], 50, 300)

    scores["vocal"] = norm(f["mfcc_var"], 80, 250)
    scores["instrumental"] = 1 - scores["vocal"]

    scores["catchy"] = clamp(scores["groovy"] * scores["melodic"])

    scores["retro"] = clamp(scores["vintage"] * 0.8 + scores["funky"] * 0.2)
    scores["classic"] = clamp(scores["melodic"] * (1 - scores["electronic"]))

    scores["soulful"] = clamp(scores["melodic"] * scores["chill"])
    scores["rare"] = clamp(scores["experimental"] * 0.8)

    return scores

def tag_sample(y, sr, tempo):
    features = extract_features(y, sr, tempo)
    scores = score_tags(features)

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return top[:3]