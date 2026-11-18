# Digital Insurance Customer Support

A simple customer-support system for an insurance company.

## Features
- FAQ chatbot (TF-IDF + cosine similarity) for claims, renewal, premium, etc.
- Raise and track support tickets (SQLite)
- Policy status lookup (sample policies: POL1001-POL1004)
- Admin panel to view tickets and update status (password: admin123)

## Run
```
pip install -r requirements.txt
streamlit run app.py
```

## Files
- app.py - Streamlit UI
- chatbot.py - FAQ chatbot
- database.py - SQLite database (support.db is created automatically)
