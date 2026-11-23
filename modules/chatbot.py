# =========================================================
# BILINGUAL HEALTH AWARENESS CHATBOT
# English + Tamil
# =========================================================

import re
import unicodedata


# =========================================================
# 1. RESPONSE KNOWLEDGE BASE
# =========================================================

RESPONSES = {

    "greeting": {
        "en": (
            "Hello! 👋 Welcome to the Diabetes Health Assistant.\n\n"
            "I can answer general questions about diabetes, BMI, "
            "healthy food, exercise, symptoms, and screening.\n\n"
            "What would you like to know?"
        ),
        "ta": (
            "வணக்கம்! 👋 நீரிழிவு சுகாதார உதவியாளருக்கு "
            "உங்களை வரவேற்கிறேன்.\n\n"
            "நீரிழிவு, BMI, ஆரோக்கியமான உணவு, உடற்பயிற்சி, "
            "அறிகுறிகள் மற்றும் பரிசோதனைகள் பற்றி "
            "பொதுவான தகவல்களை வழங்க முடியும்.\n\n"
            "உங்களுக்கு என்ன தெரிந்துகொள்ள வேண்டும்?"
        ),
    },

    "diabetes": {
        "en": (
            "Diabetes is a condition in which blood glucose levels "
            "remain higher than normal because the body does not "
            "produce enough insulin or cannot use insulin effectively.\n\n"
            "Common types include type 1, type 2, and gestational "
            "diabetes. Blood tests and advice from a healthcare "
            "professional are needed for diagnosis."
        ),
        "ta": (
            "நீரிழிவு என்பது உடலில் இன்சுலின் போதுமான அளவில் "
            "உற்பத்தியாகாததால் அல்லது இன்சுலினை உடல் சரியாகப் "
            "பயன்படுத்த முடியாததால் இரத்தத்தில் சர்க்கரை அளவு "
            "அதிகமாக இருக்கும் ஒரு நிலையாகும்.\n\n"
            "வகை 1, வகை 2 மற்றும் கர்ப்பகால நீரிழிவு ஆகியவை "
            "முக்கிய வகைகள். நீரிழிவைக் கண்டறிய இரத்தப் "
            "பரிசோதனையும் மருத்துவரின் ஆலோசனையும் தேவை."
        ),
    },

    "diet": {
        "en": (
            "Healthy eating tips:\n\n"
            "• Include a variety of vegetables.\n"
            "• Choose whole grains and high-fibre foods.\n"
            "• Eat suitable portions of fruit.\n"
            "• Limit sugary drinks and heavily processed foods.\n"
            "• Include protein sources such as beans, lentils, "
            "eggs, or other suitable foods.\n"
            "• Drink water regularly.\n\n"
            "Your dietary needs may differ depending on your health. "
            "A qualified dietitian can provide individual guidance."
        ),
        "ta": (
            "ஆரோக்கியமான உணவுப் பழக்கங்கள்:\n\n"
            "• பலவகையான காய்கறிகளை உணவில் சேர்த்துக்கொள்ளுங்கள்.\n"
            "• முழுத் தானியங்கள் மற்றும் நார்ச்சத்து நிறைந்த "
            "உணவுகளைத் தேர்ந்தெடுக்கவும்.\n"
            "• பழங்களை சரியான அளவில் சாப்பிடுங்கள்.\n"
            "• சர்க்கரை அதிகமுள்ள பானங்கள் மற்றும் அதிகமாக "
            "பதப்படுத்தப்பட்ட உணவுகளைக் குறைக்கவும்.\n"
            "• பருப்பு, பயறு, முட்டை போன்ற பொருத்தமான "
            "புரத உணவுகளைச் சேர்த்துக்கொள்ளுங்கள்.\n"
            "• போதுமான அளவு தண்ணீர் குடியுங்கள்.\n\n"
            "உங்கள் உடல்நிலைக்கு ஏற்ப உணவுத் தேவைகள் மாறலாம். "
            "தனிப்பட்ட உணவு ஆலோசனைக்கு தகுதியான உணவியல் "
            "நிபுணரை அணுகவும்."
        ),
    },

    "exercise": {
        "en": (
            "Regular physical activity can support overall health "
            "and help manage blood glucose.\n\n"
            "Many adults can aim for at least 150 minutes of "
            "moderate-intensity activity per week, if appropriate "
            "for their health and abilities.\n\n"
            "Walking, cycling, swimming, and suitable strength "
            "exercises are possible options. Start gradually if "
            "you are new to exercise."
        ),
        "ta": (
            "தொடர்ச்சியான உடற்பயிற்சி உடல்நலத்தை மேம்படுத்தவும் "
            "இரத்தச் சர்க்கரையை நிர்வகிக்கவும் உதவலாம்.\n\n"
            "உடல்நிலைக்கு ஏற்றதாக இருந்தால், பல பெரியவர்கள் "
            "வாரத்திற்கு குறைந்தது 150 நிமிடங்கள் மிதமான "
            "தீவிரமுள்ள உடற்பயிற்சியை இலக்காகக் கொள்ளலாம்.\n\n"
            "நடைப்பயிற்சி, மிதிவண்டி ஓட்டுதல், நீச்சல் மற்றும் "
            "உடலுக்கு ஏற்ற வலுப்படுத்தும் பயிற்சிகள் சில "
            "விருப்பங்களாகும். புதிதாகத் தொடங்குபவர்கள் "
            "மெதுவாகத் தொடங்க வேண்டும்."
        ),
    },

    "bmi": {
        "en": (
            "BMI means Body Mass Index. It is calculated using "
            "weight in kilograms divided by height in metres squared.\n\n"
            "BMI is a screening measure, not a diagnosis. It does "
            "not directly measure body fat or fully describe "
            "an individual's health."
        ),
        "ta": (
            "BMI என்பது உடல் நிறை குறியீட்டெண் ஆகும். "
            "உடல் எடையை கிலோகிராமில் அளந்து, உயரத்தின் "
            "மீட்டர் அளவின் வர்க்கத்தால் வகுத்து கணக்கிடப்படுகிறது.\n\n"
            "BMI என்பது ஒரு ஆரம்ப மதிப்பீட்டு அளவுகோல் மட்டுமே; "
            "இது மருத்துவ நோயறிதல் அல்ல. இது உடல் கொழுப்பை "
            "நேரடியாக அளவிடுவதில்லை; ஒருவரின் முழு உடல்நலத்தையும் "
            "இதனால் மட்டும் தீர்மானிக்க முடியாது."
        ),
    },

    "symptoms": {
        "en": (
            "Possible symptoms of diabetes include increased "
            "thirst, frequent urination, unusual tiredness, "
            "blurred vision, and unexplained weight loss.\n\n"
            "Some people have few or no obvious symptoms. "
            "A blood test is needed to diagnose diabetes. "
            "Seek medical advice if you are concerned."
        ),
        "ta": (
            "நீரிழிவின் சாத்தியமான அறிகுறிகளில் அதிக தாகம், "
            "அடிக்கடி சிறுநீர் கழித்தல், அதிக சோர்வு, "
            "மங்கலான பார்வை மற்றும் காரணமில்லாத உடல் எடை "
            "குறைதல் ஆகியவை அடங்கும்.\n\n"
            "சிலருக்கு வெளிப்படையான அறிகுறிகள் இல்லாமலும் இருக்கலாம். "
            "நீரிழிவைக் கண்டறிய இரத்தப் பரிசோதனை தேவை. "
            "கவலை இருந்தால் மருத்துவரை அணுகவும்."
        ),
    },

    "screening": {
        "en": (
            "Diabetes screening may involve blood tests such as "
            "fasting plasma glucose or HbA1c, depending on the "
            "person's circumstances and local clinical guidance.\n\n"
            "Ask a healthcare professional which test is suitable "
            "for you."
        ),
        "ta": (
            "நீரிழிவு பரிசோதனையில் உண்ணாநிலை இரத்தச் சர்க்கரை "
            "பரிசோதனை அல்லது HbA1c போன்ற இரத்தப் பரிசோதனைகள் "
            "பயன்படுத்தப்படலாம். எந்தப் பரிசோதனை தேவை என்பது "
            "உங்கள் உடல்நிலை மற்றும் மருத்துவ வழிகாட்டுதல்களைப் "
            "பொறுத்தது.\n\n"
            "உங்களுக்கு ஏற்ற பரிசோதனை எது என்பதை மருத்துவரிடம் "
            "கேட்டறியுங்கள்."
        ),
    },

    "risk": {
        "en": (
            "Factors associated with type 2 diabetes include "
            "family history, age, physical inactivity, and certain "
            "health conditions.\n\n"
            "Balanced eating, suitable physical activity, routine "
            "screening, and professional guidance can support "
            "overall health. No chatbot can determine your true "
            "personal risk from a short message."
        ),
        "ta": (
            "வகை 2 நீரிழிவுடன் தொடர்புடைய காரணிகளில் குடும்ப "
            "வரலாறு, வயது, உடல் இயக்கம் குறைவாக இருப்பது மற்றும் "
            "சில உடல்நல நிலைகள் அடங்கும்.\n\n"
            "சமச்சீரான உணவு, உடல்நிலைக்கு ஏற்ற உடற்பயிற்சி, "
            "தொடர்ச்சியான பரிசோதனை மற்றும் மருத்துவ ஆலோசனை "
            "ஒட்டுமொத்த உடல்நலத்திற்கு உதவும். சில வார்த்தைகள் "
            "மட்டுமே கொண்டு உங்கள் உண்மையான தனிப்பட்ட ஆபத்தை "
            "சாட்பாட் தீர்மானிக்க முடியாது."
        ),
    },

    "model": {
        "en": (
            "Your application's model classifies information "
            "using patterns learned from a public dataset.\n\n"
            "Its output is not a medical diagnosis and is not "
            "a clinically validated probability of developing "
            "diabetes in the future. Please discuss screening "
            "with a healthcare professional."
        ),
        "ta": (
            "உங்கள் செயலியில் உள்ள மாதிரி, பொது தரவுத்தொகுப்பிலிருந்து "
            "கற்றுக்கொண்ட வடிவங்களின் அடிப்படையில் தகவல்களை "
            "வகைப்படுத்துகிறது.\n\n"
            "இதன் முடிவு மருத்துவ நோயறிதல் அல்ல. எதிர்காலத்தில் "
            "நீரிழிவு ஏற்படும் என்பதற்கான மருத்துவ ரீதியாக "
            "உறுதிப்படுத்தப்பட்ட நிகழ்தகவும் அல்ல. பரிசோதனை "
            "குறித்து மருத்துவரிடம் ஆலோசிக்கவும்."
        ),
    },

    "emergency": {
        "en": (
            "If you have severe symptoms such as confusion, "
            "fainting, difficulty breathing, or inability to stay "
            "awake, seek emergency medical care immediately.\n\n"
            "Do not rely on this chatbot for urgent medical decisions."
        ),
        "ta": (
            "குழப்பநிலை, மயக்கம், சுவாசிப்பதில் சிரமம் அல்லது "
            "விழித்திருக்க முடியாத நிலை போன்ற கடுமையான "
            "அறிகுறிகள் இருந்தால் உடனடியாக அவசர மருத்துவ "
            "உதவியைப் பெறுங்கள்.\n\n"
            "அவசர மருத்துவ முடிவுகளுக்கு இந்த சாட்பாட்டை மட்டும் "
            "நம்ப வேண்டாம்."
        ),
    },

    "unknown": {
        "en": (
            "I can help with general questions about diabetes, "
            "healthy eating, exercise, BMI, symptoms, screening, "
            "and your application's model output.\n\n"
            "Try asking: 'What is BMI?' or "
            "'How can I eat more healthily?'"
        ),
        "ta": (
            "நீரிழிவு, ஆரோக்கியமான உணவு, உடற்பயிற்சி, BMI, "
            "அறிகுறிகள், பரிசோதனைகள் மற்றும் செயலியின் "
            "மாதிரி முடிவுகள் குறித்து பொதுவான தகவல்களை "
            "வழங்க முடியும்.\n\n"
            "'BMI என்றால் என்ன?' அல்லது "
            "'ஆரோக்கியமாக எப்படி சாப்பிடலாம்?' என்று கேளுங்கள்."
        ),
    },
}


# =========================================================
# 2. LANGUAGE DETECTION
# =========================================================

def detect_language(message):

    # Tamil Unicode characters.
    if re.search(r"[\u0B80-\u0BFF]", message):
        return "ta"

    # Tamil written using English letters.
    tamil_roman_words = [
        "vanakkam",
        "enna",
        "epdi",
        "eppadi",
        "sapadu",
        "saapadu",
        "udal",
        "payirchi",
        "neerizhivu",
        "sarkkarai",
        "eppadi",
        "sollunga",
        "venum",
        "irukku",
    ]

    lowered = message.lower()

    if any(
        word in lowered.split()
        for word in tamil_roman_words
    ):
        return "ta"

    return "en"


# =========================================================
# 3. INTENT DETECTION
# =========================================================

def detect_intent(message):

    text = unicodedata.normalize(
        "NFKC",
        message.lower(),
    )

    # Urgent symptoms should be checked first.
    emergency_terms = [
        "unconscious",
        "can't breathe",
        "cannot breathe",
        "difficulty breathing",
        "fainting",
        "confusion",
        "மயக்கம்",
        "மூச்சுத்திணறல்",
        "சுயநினைவு",
    ]

    if any(term in text for term in emergency_terms):
        return "emergency"

    greetings = [
        "hello",
        "hi",
        "hey",
        "வணக்கம்",
        "ஹலோ",
    ]

    if text.strip() in greetings:
        return "greeting"

    if any(
        word in text
        for word in [
            "diet",
            "food",
            "eat",
            "nutrition",
            "meal",
            "சாப்பாடு",
            "உணவு",
            "சத்துணவு",
            "சாப்பிட",
            "உணவுமுறை",
        ]
    ):
        return "diet"

    if any(
        word in text
        for word in [
            "exercise",
            "walking",
            "workout",
            "physical activity",
            "உடற்பயிற்சி",
            "நடைப்பயிற்சி",
            "நடப்பது",
        ]
    ):
        return "exercise"

    if any(
        word in text
        for word in [
            "bmi",
            "body mass index",
            "உடல் நிறை",
        ]
    ):
        return "bmi"

    if any(
        word in text
        for word in [
            "symptom",
            "signs of diabetes",
            "thirst",
            "urination",
            "அறிகுறி",
            "தாகம்",
            "சிறுநீர்",
        ]
    ):
        return "symptoms"

    if any(
        word in text
        for word in [
            "screening",
            "blood test",
            "hba1c",
            "test for diabetes",
            "பரிசோதனை",
            "இரத்தப் பரிசோதனை",
            "ரத்த பரிசோதனை",
        ]
    ):
        return "screening"

    if any(
        word in text
        for word in [
            "risk",
            "prevent diabetes",
            "avoid diabetes",
            "reduce diabetes",
            "family history",
            "ஆபத்து",
            "தடுக்க",
            "வராமல்",
            "குடும்ப வரலாறு",
        ]
    ):
        return "risk"

    if any(
        word in text
        for word in [
            "model",
            "prediction",
            "predict",
            "score",
            "result",
            "classification",
            "முடிவு",
            "மதிப்பெண்",
            "கணிப்பு",
        ]
    ):
        return "model"

    if any(
        word in text
        for word in [
            "diabetes",
            "diabetic",
            "blood sugar",
            "நீரிழிவு",
            "சர்க்கரை நோய்",
            "இரத்த சர்க்கரை",
        ]
    ):
        return "diabetes"

    return "unknown"


# =========================================================
# 4. CHATBOT RESPONSE
# =========================================================

def chatbot_response(message, history=None, language=None):

    if not message or not message.strip():

        language = language or "en"

        return RESPONSES["unknown"][language]

    selected_language = (
        language
        if language in ["en", "ta"]
        else detect_language(message)
    )

    intent = detect_intent(message)

    return RESPONSES[intent][selected_language]