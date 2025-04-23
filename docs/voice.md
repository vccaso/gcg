When using OpenAI’s TTS models (tts-1 and tts-1-hd), you can choose from six high-quality voices — each with a distinct style and tone.

🎤 OpenAI TTS Voices (as of GPT-4o / April 2024)

Voice	Style / Description
alloy	🎧 Crisp, warm, well-balanced (default)
echo	🌙 Calm, slightly deeper, soothing
fable	📖 Friendly, upbeat, clear storytelling
onyx	🖤 Deep, smooth, professional
nova	🌟 Bright, expressive, articulate
shimmer	✨ Light, youthful, slightly playful
🧪 Example Usage
python
Copy
Edit
response = openai.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input="Welcome to your personal AI assistant!"
)
response.stream_to_file("output/audio/nova_voice.wav")
✅ Best Practice Tips
Use tts-1 for faster generation, tts-1-hd for higher fidelity

Choose voice to match personality of app:

fable for a friendly onboarding

onyx for serious assistant

shimmer for playful tone

You can even let the user pick a voice in your frontend or workflow input