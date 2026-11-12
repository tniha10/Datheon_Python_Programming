import json
import re
from pathlib import Path

# The FAQ dataset must sit in the same folder as this script.
FAQ_FILE = Path(__file__).resolve().parent / "sample_faq.json"

# Exit commands from the task: 'bye', 'exit', 'quit'. Word boundaries let
# "ok bye" work too.
EXIT_PATTERN = re.compile(r"\b(bye|exit|quit)\b")

# Minimum share of an FAQ question's keywords that must appear in the user's
# message. Below this, the bot uses the fallback instead of guessing.
MIN_CONFIDENCE = 0.3

# Common words that carry no meaning for matching.
STOPWORDS = {
    "what", "are", "your", "do", "i", "my", "how", "when", "will", "you",
    "the", "a", "an", "is", "to", "of", "can", "me", "we", "it", "for",
    "in", "on", "and", "please", "tell", "about", "have",
}

# Maps different ways of saying the same thing to one keyword,
# e.g. "when are you open" should match "hours of operation".
SYNONYMS = {
    "open": "hour", "opening": "hour", "timing": "hour", "schedule": "hour",
    "submission": "submit", "upload": "submit", "get": "receive",
}

# Conversation states: greeting -> intent identification -> resolution -> exit
GREETING, LISTENING, RESOLVED = "greeting", "listening", "resolved"


def load_data():
    """Load greetings and FAQs from JSON, with error handling for a missing or broken file."""
    try:
        with open(FAQ_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{FAQ_FILE.name}' not found. Place it next to chatbot.py.")
    except json.JSONDecodeError:
        print(f"Error: '{FAQ_FILE.name}' is not valid JSON.")
    return None


def clean(text):
    """Normalize input: lowercase, strip whitespace, remove punctuation."""
    return re.sub(r"[^\w\s]", "", text.lower().strip())


def extract_keywords(text):
    """Regex-extract words, drop stopwords, reduce plurals, apply synonyms."""
    keywords = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in STOPWORDS:
            continue
        # Simple plural handling so 'certificates' matches 'certificate'
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        keywords.add(SYNONYMS.get(word, word))
    return keywords


def find_answer(user_input, faqs):
    """Return the answer of the best-matching FAQ, or None if confidence is low."""
    user_keywords = extract_keywords(user_input)
    best_score, best_answer = 0, None

    for faq in faqs:
        faq_keywords = extract_keywords(faq["question"])
        if not faq_keywords:
            continue
        # Confidence = fraction of the FAQ question's keywords found in the input
        score = len(user_keywords & faq_keywords) / len(faq_keywords)
        if score > best_score:
            best_score, best_answer = score, faq["answer"]

    return best_answer if best_score >= MIN_CONFIDENCE else None


def main():
    data = load_data()
    if data is None:
        return

    greetings = set(data["greetings"])
    faqs = data["faqs"]
    state = GREETING

    print("Bot: Hello! Ask me a question, or type 'bye' to exit.")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        text = clean(user_input)
        if not text:
            continue

        # Exit check comes first so it works in any state
        if EXIT_PATTERN.search(text):
            print("Bot: Goodbye! Have a great day.")
            break

        # Greeting -> move on to intent identification
        if text in greetings:
            print("Bot: Hello! How can I help you today?")
            state = LISTENING
            continue

        # After an answer, the bot asked "anything else?" so handle yes/no replies
        if state == RESOLVED:
            if re.fullmatch(r"no|nope|nothing|no thanks|thats all", text):
                print("Bot: Goodbye! Have a great day.")
                break
            if re.fullmatch(r"yes|yeah|yep|sure", text):
                print("Bot: Sure, go ahead.")
                state = LISTENING
                continue

        # Intent identification -> resolution
        answer = find_answer(user_input, faqs)
        if answer:
            print(f"Bot: {answer}")
            print("Bot: Is there anything else I can help with?")
            state = RESOLVED
        else:
            # Fallback for low-confidence / unrecognized queries
            print("Bot: Sorry, I didn't understand that. You can ask things like:")
            for faq in faqs:
                print(f"  - {faq['question']}")


if __name__ == "__main__":
    main()