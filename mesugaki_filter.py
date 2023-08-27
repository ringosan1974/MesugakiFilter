import glob
import json
import os
import random
import requests
import subprocess
import sys


from pydub import AudioSegment, playback


def exec_cmd_TTS(cmd, speak_dict):
    if os.name == "nt": # nt == windows
        output = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    else:
        output = subprocess.run(cmd, capture_output=True, text=True)

    if output.returncode != 0:
        print(output.stderr)
        speak_cink(speak_dict)
    else:
        print(output.stdout, end="")


def speak_cink(dct):
    response = synthesis_speak(dct=dct)
    playback.play(
        AudioSegment(response.content, sample_width=2, frame_rate=44100, channels=1)
    )


def get_speak_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        jsn = json.load(f)
    speaklist = []
    for i in jsn["textBoxes"]:
        speaklist.append(
            dict(
                speakerUuid=i["speakerUuid"],
                styleId=i["styleId"],
                text=i["text"],
                prosodyDetail=i["prosodyDetail"],
                speedScale=i["speedScale"],
                pitchScale=i["pitchScale"],
                intonationScale=i["intonationScale"],
                volumeScale=i["volumeScale"],
                prePhonemeLength=i["prePhonemeLength"],
                postPhonemeLength=i["postPhonemeLength"],
                outputSamplingRate=44100
            )
        )
    return speaklist


# localhost:50032 == coeiroink API
url = "http://localhost:50032/v1"


def synthesis_speak(dct):
    response = requests.post(
        f"{url}/synthesis",
        json=dct
    )
    return response


if __name__ == "__main__":
    cmd = sys.argv[1:]
    path = "./*.cink"

    settingfilelist = glob.glob(path)
    speaks = get_speak_from_json(settingfilelist[0])
    randspeak = random.choice(speaks)

    exec_cmd_TTS(cmd, randspeak)

