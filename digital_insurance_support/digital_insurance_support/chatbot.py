"""FAQ chatbot using TF-IDF + cosine similarity."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQS = [
    ("How do I file a claim?",
     "To file a claim: 1) Inform us within 7 days of the incident, 2) Submit the claim form with "
     "required documents (ID, policy copy, bills/FIR), 3) Our team reviews it and updates you by email."),
    ("How can I renew my policy?",
     "Go to the Policy Status tab, check your expiry date, and pay the renewal premium online before "
     "expiry. A grace period of 30 days is available for most policies."),
    ("What documents are required for a claim?",
     "Policy copy, government ID, claim form, original bills or invoices, and for motor claims an FIR "
     "and photos of the damage."),
    ("How long does claim settlement take?",
     "Most claims are settled within 7 to 15 working days after all documents are received."),
    ("How do I pay my premium?",
     "You can pay premium online by UPI, net banking, debit or credit card, or set up auto-debit."),
    ("How can I check my policy status?",
     "Open the Policy Status tab and enter your policy number to see cover amount, expiry date and status."),
    ("How do I update my contact details or address?",
     "Raise a support ticket with category 'Policy Update' and our team will update your details within 2 days."),
    ("Can I cancel my policy?",
     "Yes. Raise a ticket with category 'Cancellation'. Refunds are calculated as per policy terms "
     "and the free-look period (15 days)."),
    ("What is a free-look period?",
     "It is a 15-day window after buying a policy in which you can cancel it if you disagree with the terms."),
    ("What does my health insurance cover?",
     "Health plans cover hospitalisation, day-care procedures, pre and post hospitalisation expenses and "
     "ambulance charges. Exact coverage depends on your plan."),
    ("What is the customer care number?",
     "Call our toll-free number 1800-000-1234 (Mon-Sat, 9 AM to 6 PM) or email support@digitalinsure.example."),
    ("How do I track my complaint or ticket?",
     "Use the Track Ticket tab and enter your ticket ID."),
]

FALLBACK = ("Sorry, I couldn't find an answer to that. Please raise a support ticket "
            "and our team will get back to you.")
THRESHOLD = 0.25


class FAQBot:
    def __init__(self):
        self.questions = [q for q, _ in FAQS]
        self.answers = [a for _, a in FAQS]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.questions)

    def reply(self, text):
        text = text.lower().strip()
        if text in {"hi", "hello", "hey", "hii"}:
            return "Hello! 👋 I'm your insurance assistant. Ask me about claims, renewal, premium or policy."
        if text in {"thanks", "thank you"}:
            return "You're welcome! Is there anything else I can help with?"
        scores = cosine_similarity(self.vectorizer.transform([text]), self.matrix)[0]
        best = scores.argmax()
        return self.answers[best] if scores[best] >= THRESHOLD else FALLBACK
