def understand_command(text: str):
    text = text.lower().strip()

    pantry_keywords = [
        "తెచ్చాను", "ఉంది", "కొన్నాను",
        "bought", "have", "got", "purchased", "added"
    ]

    shopping_keywords = [
        "కొనాలి", "లేదు", "అయిపోయింది",
        "need", "buy", "finished", "over", "get"
    ]

    for word in pantry_keywords:
        if word in text:
            item = text.replace(word, "").strip()
            return {"action": "pantry", "item": item or text}

    for word in shopping_keywords:
        if word in text:
            item = text.replace(word, "").strip()
            return {"action": "shopping", "item": item or text}

    return {"action": "pantry", "item": text}