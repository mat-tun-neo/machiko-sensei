import whisper
import sys

args = sys.argv
# 利用できる学習済みmodelサイズは tiny, base, small, medium, largeの順に5種類
model = whisper.load_model(args[1])
result = model.transcribe(args[2], verbose=True, language='ja')
print(result["text"])
