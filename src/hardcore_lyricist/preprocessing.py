import re
import yaml


def load_yaml_data(file_path: str = "src/hardcore_lyricist/data/raw_data.yaml"):
    with open(file_path, "r") as file:
        try:
            return yaml.load(file, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)


def train_test_split(songs):
    return (
        [
            {
                "title": song["song_name"],
                "lyrics": song["lyrics"],
                "tokens": preprocess_song_lyrics(song["lyrics"]),
            }
            for song in songs
            if song["track"] not in [5, 6]
        ],
        [
            {
                "title": song["song_name"],
                "lyrics": song["lyrics"],
                "tokens": preprocess_song_lyrics(song["lyrics"]),
            }
            for song in songs
            if song["track"] in [5, 6]
        ],
    )


def remove_junk_text(text):
    # Remove specific punctuation marks
    text = re.sub(r"[,;:?!]", "", text)

    # Remove specific words like "fig" and any remaining non-alphanumeric characters
    text = re.sub(r"\bfig\b", "", text, flags=re.IGNORECASE)

    # Add spaces around the newlines if they are not already there
    text = re.sub(r"\\n", r" \\n ", text)

    # Remove the space added between consecutive newlines
    text = re.sub(r"\\n  \\n", r"\\n\\n", text)

    text = re.sub(r"\\n", r"\n", text)

    return text


def preprocess_song_lyrics(lyrics):
    text = lyrics
    text = remove_junk_text(text).strip().lower()
    return text_to_tokens(text)


def text_to_tokens(text):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    return tokenizer(text)