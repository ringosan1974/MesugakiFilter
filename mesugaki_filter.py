import os
import requests
import subprocess
import sys


from pydub import AudioSegment, playback


def exec_cmd_TTS(cmd, speakerUuid, styleId, text):
    if os.name == "nt":
        output = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    else:
        output = subprocess.run(cmd, capture_output=True, text=True)

    if output.returncode != 0:
        print(output.stderr)
        prosody = estimate_prosody().json()
        response = synthesis_speak(speakerUuid, styleId, text, prosody["detail"])
        playback.play(
            AudioSegment(response.content, sample_width=2, frame_rate=44100, channels=1)
        )
    else:
        print(output.stdout)


def estimate_prosody(text):
    return requests.post(
        "http://localhost:50032/v1/estimate_prosody",
        json={
            "text": text
        }
    )


def synthesis_speak(
        speakerUuid,
        styleId,
        text,
        prosodyDetail,
        speedScale=1.00,
        pitchScale=0.00,
        intonationScale=1.00,
        volumeScale=1.00,
        prePhonemeLength=0.10,
        postPhonemeLength=0.10,
        outputSamplingRate=0
    ):

    return requests.post(
        "http://localhost:50032/v1/synthesis",
        json={
            "speakerUuid": speakerUuid,
            "styleId": styleId,
            "text": text,
            "prosodyDetail":prosodyDetail,
            "speedScale": speedScale,
            "pitchScale": pitchScale,
            "intonationScale": intonationScale,
            "volumeScale": volumeScale,
            "prePhonemeLength": prePhonemeLength,
            "postPhonemeLength": postPhonemeLength,
            "outputSamplingRate": outputSamplingRate
        }
    )


if __name__ == "__main__":
    speakerUuid = "cb11bdbd-78fc-4f16-b528-a400bae1782d",
    styleId = 92
    text = "ざこ"
    cmd = sys.argv[1:]
    exec_cmd_TTS(cmd, speakerUuid, styleId, text)

