from src.client import GeminiClient

client = GeminiClient()
response = client.send_message("Hallo, wer bist du?")
print(response.text)
