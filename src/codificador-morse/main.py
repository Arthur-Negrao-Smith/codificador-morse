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
    " ": " ",
}


def encode_char(char: str, slots_between_dots: int = 1) -> str:
    """
    Encode a ASCII char to morse code.

    Args:
        char (str): A char to encode.
        slots_between_dots (int): Dot spaces between each morse symbol: "-" or ".".

    Returns:
        str: Return the char encoded.
    """
    # translate from ASCII char to morse code
    raw_encoded: str = MORSE_CODE_DICT[char]
    finished_encoded: str = ""

    for i, current_char_morse in enumerate(raw_encoded):
        finished_encoded += current_char_morse
        # The word do not has a blank space in finish
        if i != len(raw_encoded) - 1:
            finished_encoded += " " * slots_between_dots

    return finished_encoded


def encode_message(
    message: str,
    time_stemp_between_words: int = 7,
    time_stemp_between_chars: int = 3,
) -> str | None:
    """
    Encode a raw message to morse code.

    Args:
        message (str): Message to encode.
        time_stemp_between_words (int): Dot spaces between each word,
        time_stemp_between_chars (int): Dot spaces between each ASCII character.

    Returns:
        str: The message enconded.
        None: If the message has a invalid character.
    """
    raw_msg: str = message.strip().upper()

    try:
        words_list: list[str] = raw_msg.split(" ")
        encoded_words_list: list[str] = []
        for word in words_list:
            encoded_words_list.append(
                (" " * time_stemp_between_chars).join(map(encode_char, word))
            )

        encoded_msg: str = (
            (" " * time_stemp_between_words).join(encoded_words_list).strip()
        )
        return encoded_msg
    except:
        print(f"O texto '{raw_msg}' é inválido. Use apenas caracteres ASCII.")
        return None


def play_tone(frequency: float | int, duration: float, sample_rate=44100):
    """
    Generates and plays a simple tone.

    Args:
        frequency (int | float): Tone frequency (Hz).
        duration (float): Durantion to play tone (ms).
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


def play_encoded_message(
    msg: str, dot_duration: float = 0.06, frequency: int = 440
) -> None:
    """
    Play a entire encoded text.

    Args:
        msg (str): A message to encond into a morse code and play.
        dot_duration (float): Time stemp to represent a duration a "." in morse code.
    """
    for char in msg:
        if char == ".":
            # 1 dot duration to represent a "."
            play_tone(frequency, dot_duration)
        elif char == "-":
            # 3 times the dot duration to represent a "-"
            play_tone(frequency, dot_duration * 3)
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
