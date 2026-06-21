"""
Multilingual Translator Agent
=============================
Supports 50+ languages for healthcare accessibility.
Demonstrates: Agent skills (multilingual capability)

Ensures patients can communicate in their preferred language while
preserving medical terminology accuracy and cultural sensitivity.

NOTE: In Google ADK, tools are plain Python functions.
NO decorator needed - just pass them to LlmAgent(tools=[...])
"""
from google.adk.agents import LlmAgent
import json


# Tool functions - plain Python functions, NO decorator needed
def detect_language(text: str) -> str:
    """
    Detect the language of patient input.

    Args:
        text: Patient's input text

    Returns:
        JSON with detected language code and confidence
    """
    # In production, use a language detection library like langdetect
    # For demo, simple heuristic based on common words
    text_lower = text.lower()

    language_hints = {
        "es": ["el", "la", "los", "las", "fiebre", "dolor", "cabeza"],
        "fr": ["le", "la", "les", "fievre", "mal", "tete"],
        "ar": ["ال", " fever", "رأس"],
        "hi": ["मैं", "हूँ", "बुखार", "दर्द"],
        "zh": ["我", "是", "发烧", "头痛"],
    }

    for lang_code, hints in language_hints.items():
        if any(hint in text_lower for hint in hints):
            return json.dumps({
                "language_code": lang_code,
                "language_name": SUPPORTED_LANGUAGES.get(lang_code, "Unknown"),
                "confidence": 0.85,
                "method": "keyword_detection"
            })

    # Default to English if uncertain
    return json.dumps({
        "language_code": "en",
        "language_name": "English",
        "confidence": 0.5,
        "method": "default"
    })


def get_language_name(language_code: str) -> str:
    """
    Get the full name of a language from its code.

    Args:
        language_code: ISO 639-1 language code (e.g., 'es', 'fr')

    Returns:
        Full language name
    """
    return SUPPORTED_LANGUAGES.get(language_code, "Unknown")


# Supported languages for healthcare contexts
SUPPORTED_LANGUAGES = {
    "en": "English", "es": "Spanish", "fr": "French", "ar": "Arabic",
    "hi": "Hindi", "zh": "Mandarin", "sw": "Swahili", "pt": "Portuguese",
    "bn": "Bengali", "ru": "Russian", "ja": "Japanese", "de": "German",
    "it": "Italian", "ko": "Korean", "vi": "Vietnamese", "tr": "Turkish",
    "pl": "Polish", "uk": "Ukrainian", "ro": "Romanian", "nl": "Dutch",
    "el": "Greek", "th": "Thai", "cs": "Czech", "id": "Indonesian",
    "sv": "Swedish", "hu": "Hungarian", "fi": "Finnish", "he": "Hebrew",
    "da": "Danish", "no": "Norwegian", "sk": "Slovak", "bg": "Bulgarian",
    "hr": "Croatian", "sr": "Serbian", "sl": "Slovenian", "lt": "Lithuanian",
    "lv": "Latvian", "et": "Estonian", "ms": "Malay", "tl": "Tagalog",
    "fa": "Persian", "ur": "Urdu", "ta": "Tamil", "te": "Telugu",
    "mr": "Marathi", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam",
    "pa": "Punjabi", "si": "Sinhala", "my": "Burmese", "km": "Khmer",
    "lo": "Lao", "ne": "Nepali", "am": "Amharic", "so": "Somali",
    "ha": "Hausa", "yo": "Yoruba", "ig": "Igbo", "zu": "Zulu"
}


class TranslatorAgent:
    """
    Handles real-time translation for patient communication.

    Supports 50+ languages with medical terminology preservation
    and cultural sensitivity awareness.

    Attributes:
        agent: LlmAgent configured for medical translation
        supported_languages: Dictionary of language codes and names
    """

    def __init__(self):
        """Initialize the translator agent."""
        self.agent = LlmAgent(
            name="translator",
            model="gemini-2.5-flash",
            description="Healthcare multilingual translator",
            instruction="""
            You are a medical translator. Translate between languages while 
            preserving medical accuracy and cultural appropriateness.

            RULES:
            1. Preserve medical terminology - use internationally recognized terms
            2. Maintain empathetic and reassuring tone
            3. Flag culturally sensitive health topics (mental health, reproductive health, etc.)
            4. Keep translations concise for SMS compatibility (under 160 chars when possible)
            5. Use simple language for low-literacy populations
            6. Include both technical and lay terms when helpful

            TRANSLATION GUIDELINES:
            - Symptom descriptions: Be precise but use accessible language
            - Care instructions: Use step-by-step format
            - Emergency warnings: Use urgent, clear language
            - Appointment details: Include date, time, location clearly

            CULTURAL SENSITIVITY:
            - Be aware of cultural attitudes toward certain medical topics
            - Respect gender preferences in communication
            - Consider family dynamics in healthcare decisions
            """,
            tools=[detect_language, get_language_name]  # Pass functions directly
        )

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text between languages using the agent.

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text
        """
        if source_lang == target_lang:
            return text

        # Use the LLM agent for translation
        translation_prompt = f"""
        Translate the following medical text from {SUPPORTED_LANGUAGES.get(source_lang, source_lang)} 
        to {SUPPORTED_LANGUAGES.get(target_lang, target_lang)}.

        Preserve medical accuracy and use appropriate terminology.

        Text to translate:
        {text}

        Provide only the translation, no explanations.
        """

        return self.agent.run(input=translation_prompt)


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Translator Agent - Demo")
    print("=" * 60)

    translator = TranslatorAgent()

    print(f"\nSupported languages: {len(translator.SUPPORTED_LANGUAGES)}")
    print(f"Sample: {list(translator.SUPPORTED_LANGUAGES.items())[:5]}")

    # Test language detection
    print("\n1. Language Detection:")
    test_texts = [
        "fiebre y dolor de cabeza",
        "j'ai mal à la tête",
        "I have a headache"
    ]
    for text in test_texts:
        result = json.loads(detect_language(text))
        print(f"   '{text}' -> {result['language_name']} (confidence: {result['confidence']})")

    print("\n" + "=" * 60)
