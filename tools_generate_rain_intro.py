import math
import random
import struct
import wave
from pathlib import Path

SR = 48000
DURATION = 120.0
N = int(SR * DURATION)
OUT = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame/assets/audio")
OUT.mkdir(parents=True, exist_ok=True)

# Low-density pentatonic motifs for a restrained, misty opening.
SCALE = [146.83, 164.81, 196.00, 220.00, 261.63, 293.66, 329.63]
XIAO_MOTIF = [(0.0, 4, 2.4), (4.8, 3, 1.9), (9.3, 1, 2.6), (15.4, 2, 1.8), (21.0, 0, 2.8)]
QIN_MOTIF = [(1.0, 0, 0.55), (2.9, 2, 0.42), (5.5, 4, 0.62), (8.7, 1, 0.48), (12.4, 3, 0.72), (17.0, 0, 0.54), (20.0, 2, 0.50)]

# Deterministic white-noise state for a smooth rain bed.
rng = random.Random(240807)
noise = 0.0


def env(t, start, length, attack=0.2, release=0.6):
    x = t - start
    if x < 0 or x > length:
        return 0.0
    a = min(1.0, x / max(attack, 1e-6))
    r = min(1.0, (length - x) / max(release, 1e-6))
    return min(a, r)


def xiao(t):
    # Three sparse motif passes; breathy sine + harmonics, no vibrato-heavy lead.
    total = 0.0
    for base in (0.0, 30.0, 62.0, 92.0):
        for off, idx, length in XIAO_MOTIF:
            start = base + off
            e = env(t, start, length, 0.24, 0.85)
            if e:
                f = SCALE[idx]
                u = t - start
                breath = 0.08 * math.sin(2 * math.pi * 6.0 * u)
                total += e * (0.72 * math.sin(2 * math.pi * f * u) + 0.18 * math.sin(2 * math.pi * 2*f*u) + breath * math.sin(2 * math.pi * f * u))
    return total * 0.095


def qin(t):
    # Plucked attacks with short resonant tails.
    total = 0.0
    for base in (0.0, 30.0, 62.0, 92.0):
        for off, idx, length in QIN_MOTIF:
            start = base + off
            u = t - start
            if 0 <= u <= length + 2.2:
                f = SCALE[idx] * (0.5 if idx < 2 else 1.0)
                attack = math.exp(-u * 8.5)
                tail = math.exp(-u * 1.15)
                total += (0.55 * attack + 0.18 * tail) * (math.sin(2*math.pi*f*u) + 0.25*math.sin(2*math.pi*2*f*u) + 0.10*math.sin(2*math.pi*3*f*u))
    return total * 0.11


def fade(t, start=0.0, end=DURATION):
    return min(1.0, t / 1.2) * min(1.0, (end - t) / 1.2)


def write_pcm(path, generator, channels=2):
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(3)  # 24-bit PCM
        wf.setframerate(SR)
        buf = bytearray()
        for i in range(N):
            t = i / SR
            l, r = generator(t)
            for value in (l, r):
                value = max(-0.98, min(0.98, value))
                q = int(value * 8388607.0)
                buf.extend(struct.pack("<i", q)[:3])
            if len(buf) >= 262144:
                wf.writeframesraw(buf)
                buf.clear()
        if buf:
            wf.writeframesraw(buf)


def bgm(t):
    f = fade(t)
    # Small center image with slight stereo drift for a natural room impression.
    x = xiao(t)
    q = qin(t)
    room = 0.006 * math.sin(2*math.pi*0.21*t)
    return f * (x + q + room), f * (x * 0.96 + q * 1.04 - room)


def rain(t):
    global noise
    # Smoothed noise plus occasional soft drops; no thunder or harsh transients.
    white = rng.uniform(-1.0, 1.0)
    noise = 0.985 * noise + 0.015 * white
    hiss = white - noise
    drops = 0.0
    phase = (t * 7.3) % 1.0
    if phase < 0.018:
        drops = math.sin(2 * math.pi * (1500 + 500 * phase) * phase) * (1.0 - phase / 0.018) * 0.18
    v = (0.12 * noise + 0.035 * hiss + drops) * min(1.0, t / 0.9) * min(1.0, (DURATION - t) / 0.9)
    return v, v * 0.98


if __name__ == "__main__":
    write_pcm(OUT / "bgm" / "bgm_rain_intro_sample.wav", bgm)
    write_pcm(OUT / "ambient" / "sfx_rain_continuous_sample.wav", rain)
    print("generated", N, "frames at", SR, "Hz")
