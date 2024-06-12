import whisper

def initialize_whisper_model():
    return whisper.load_model("base")
