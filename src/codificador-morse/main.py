import sounddevice as sd
import numpy as np

# The dict to translate the code
MORSE_CODE_DICT: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ", ": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
    " ": "/",
}


def encode_message(message: str) -> str | None:
    """
    Encode a raw message to morse code.

    Args:
        message (str): Message to encode.

    Returns:
        str: The message encoded.
        None: If the message has a invalid character.
    """
    raw_msg: str = message.strip().upper()

    try:
        encoded_msg = "".join(map(lambda char: MORSE_CODE_DICT[char] + " ", raw_msg))
        return encoded_msg
    except:
        print(f"O texto '{raw_msg}' é inválido. Use apenas caracteres ASCII.")
        return None


def play_tone(frequency: float | int, duration: float, sample_rate=44100):
    """
    Generates and plays a simple tone.

    Args:
        frequency (int | float): Tone frequency (Hz).
        duration (float): Duration to play tone (ms).
        sample_rate (int): Number of samples to play.
    """
    # Generate time points
    time = np.linspace(0.0, duration, int(sample_rate * duration), endpoint=False)

    # Generate a sine wave
    data = np.sin(2.0 * np.pi * frequency * time)

    # Play the data (data is automatically treated as float32)
    sd.play(data, samplerate=sample_rate)

    # Wait until playback is finished
    sd.wait()


def play_encoded_message(msg: str, dot_duration: float = 0.06) -> None:
    """
    Play a entire encoded text.

    Args:
        msg (str): A message to encode into a morse code and play.
        dot_duration (float): Timestamp to represent the duration of "." in morse code.
    """
    for char in msg:
        if char == ".":
            # 1 dot duration to represent a "."
            play_tone(440, dot_duration)
        elif char == "-":
            # 3 times the dot duration to represent a "-"
            play_tone(440, dot_duration * 3)
        else:
            # to represent a blank space
            sd.sleep(int(dot_duration * 1000))


while True:
    raw_msg: str = input("Digite seu texto para codificar: ").strip().upper()

    if raw_msg == "":
        break

    msg = encode_message(raw_msg)

    if msg is not None:
        print(f"A mensagem codificada é: {msg}")
        print("Tocando a mensagem codificada...")
        play_encoded_message(msg)

    print("-" * 50)
