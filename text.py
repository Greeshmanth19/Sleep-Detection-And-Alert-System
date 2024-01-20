import pyttsx3


class tts:

    def text_to_speech(self, text):
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set properties (optional)
        # You can experiment with different voices and rates
        engine.setProperty('rate', 150)  # Speed of speech
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Select a voice (0 for the default)

        # Convert text to speech
        engine.say(text)

        # Wait for the speech to finish
        engine.runAndWait()
