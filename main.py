from flask import Flask, request, jsonify
import random
import datetime

app = Flask(__name__)

# In-memory storage (Replace with a database in production)
mood_history = {}

# Mental health resources
resources = [
    "You're not alone. Reach out to a trusted friend or therapist.",
    "988 is the Suicide & Crisis Lifeline if you need immediate support.",
    "Take a deep breath. You deserve rest and care. Here’s a resource: https://www.nami.org/Support-Education"
]

# Uplifting quotes
quotes = [
    "You are enough just as you are.",
    "Your existence is resistance. Keep going.",
    "Rest is revolutionary. Take care of yourself."
]

# Jokes for the comedy bot
jokes = [
    "Why don’t skeletons fight each other? They don’t have the guts!",
    "I told my therapist about my fear of over-engineering things. She said, ‘That’s an interesting problem… let’s build a solution for that.’",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

@app.route('/mood_checkin', methods=['POST'])
def mood_checkin():
    user_id = request.json.get("user_id")
    mood = request.json.get("mood")
    
    if user_id not in mood_history:
        mood_history[user_id] = []
    
    mood_history[user_id].append({"date": str(datetime.date.today()), "mood": mood})
    
    # Keep only last 7 days
    mood_history[user_id] = mood_history[user_id][-7:]
    
    # Check for negative streak
    last_3_days = [entry["mood"] for entry in mood_history[user_id][-3:]]
    if last_3_days.count("negative") >= 3:
        return jsonify({"message": "You've been feeling down for a few days. Here’s some support:", "resource": random.choice(resources)})
    
    return jsonify({"message": "Mood check-in saved!"})

@app.route('/quote', methods=['GET'])
def get_quote():
    return jsonify({"quote": random.choice(quotes)})

@app.route('/joke', methods=['GET'])
def get_joke():
    return jsonify({"joke": random.choice(jokes)})

if __name__ == '__main__':
    app.run(debug=True)
