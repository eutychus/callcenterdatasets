#!/usr/bin/env python3
"""
Generate and save original call transcripts - Batch 1 (1-250)
These conversations are generated directly as original content.
"""

import json
from pathlib import Path
import datetime
import random

OUTPUT_DIR = Path("/home/user/callcenterdatasets/telco-haiku/calls")

# Batch 1: Original conversations (calls 1-250)
calls_data = [
    # Call 1 - Support: Internet issues
    {
        "call_id": 1,
        "metadata": {
            "call_type": "support",
            "agent_name": "Sarah",
            "duration": 52.3,
            "sentiment": "positive",
            "issue_category": "connectivity",
            "issue_resolved": True
        },
        "conversation": [
            {"speaker": "ivr", "start_time": 0.0, "end_time": 4.2, "text": "Welcome to Telecom Haiku. Press 1 for English or 2 for Spanish."},
            {"speaker": "agent", "start_time": 5.8, "end_time": 10.5, "text": "Hi there, this is Sarah. What's going on with your service today?"},
            {"speaker": "caller", "start_time": 11.2, "end_time": 18.9, "text": "Yeah, so like, my internet completely died about an hour ago. I can't even load a single page. It was working fine this morning and then just... nothing."},
            {"speaker": "agent", "start_time": 19.5, "end_time": 24.1, "text": "I'm really sorry to hear that. Let me pull up your account and check what's happening."},
            {"speaker": "agent", "start_time": 25.0, "end_time": 31.3, "text": "I'm seeing your connection is active but there might be a local issue. Can you check if your modem has power? There should be lights on it."},
            {"speaker": "caller", "start_time": 32.1, "end_time": 38.4, "text": "Oh, um, yeah I see some lights. There's one that's kind of blinking red though. Is that bad? Most of them are green."},
            {"speaker": "agent", "start_time": 39.0, "end_time": 45.8, "text": "That red light actually usually means it's trying to connect. Let's try restarting it. Can you unplug the modem for about 30 seconds?"},
            {"speaker": "caller", "start_time": 46.5, "end_time": 52.3, "text": "Oh okay, yeah I'm unplugging it now... alright, it's back in. Oh wow, the light just turned green! That's so much faster. My stuff is loading again!"},
            {"speaker": "agent", "start_time": 52.8, "end_time": 56.2, "text": "Perfect! You're all set. Let me know if you have any other issues."}
        ]
    },
    # Call 2 - Sales: Upgrade inquiry
    {
        "call_id": 2,
        "metadata": {
            "call_type": "sales",
            "agent_name": "Mike",
            "duration": 48.7,
            "sentiment": "neutral",
            "product_category": "Mobile Plan",
            "sale_completed": False
        },
        "conversation": [
            {"speaker": "ivr", "start_time": 0.0, "end_time": 5.1, "text": "Thank you for calling Telecom Haiku. Your call is important to us. Please hold for the next available sales representative."},
            {"speaker": "agent", "start_time": 6.3, "end_time": 12.1, "text": "Hey, thanks for calling! This is Mike from sales. How can I help you find the perfect plan today?"},
            {"speaker": "caller", "start_time": 13.0, "end_time": 19.5, "text": "Hi Mike. So I've had the same mobile plan for like three years and I heard you might have some new options?"},
            {"speaker": "agent", "start_time": 20.2, "end_time": 26.8, "text": "Absolutely! We've actually made some major improvements. What's your main priority? Are you looking for more data, better speeds, or lower prices?"},
            {"speaker": "caller", "start_time": 27.5, "end_time": 33.2, "text": "Um, honestly probably more data. I'm always running out. And maybe faster speeds if the price is reasonable."},
            {"speaker": "agent", "start_time": 34.0, "end_time": 41.3, "text": "Perfect. So we have this new Elite plan that comes with triple the data and 5G speeds. It's actually only 15 dollars more than what you're probably paying now."},
            {"speaker": "caller", "start_time": 42.0, "end_time": 48.7, "text": "Oh that's interesting. 15 dollars isn't too bad. But like, I don't really understand the 5G thing. Is that worth it? Do I need anything special?"},
            {"speaker": "agent", "start_time": 49.3, "end_time": 53.0, "text": "Great question. If you have a newer phone, you'll get it automatically. Can you think about it and call us back?"}
        ]
    },
    # Call 3 - Billing: Dispute
    {
        "call_id": 3,
        "metadata": {
            "call_type": "billing",
            "agent_name": "Jennifer",
            "duration": 41.2,
            "sentiment": "negative",
            "issue_category": "charge dispute",
            "issue_resolved": True
        },
        "conversation": [
            {"speaker": "ivr", "start_time": 0.0, "end_time": 3.8, "text": "Welcome to Telecom Haiku billing department. Please have your account number ready."},
            {"speaker": "agent", "start_time": 5.0, "end_time": 9.2, "text": "Hi, this is Jennifer from billing. What's your concern today?"},
            {"speaker": "caller", "start_time": 10.0, "end_time": 18.5, "text": "Yeah I'm pretty upset actually. I got charged 89 dollars this month but my plan is supposed to be 49. This is ridiculous. What the heck happened?"},
            {"speaker": "agent", "start_time": 19.2, "end_time": 25.8, "text": "I completely understand your frustration. Let me look at your account right now and see what happened."},
            {"speaker": "agent", "start_time": 26.5, "end_time": 33.1, "text": "Okay, I see the issue. It looks like you were charged for a premium support add-on that was accidentally activated. That's on us."},
            {"speaker": "caller", "start_time": 33.8, "end_time": 38.4, "text": "I never asked for that! I didn't authorize anything. Can you remove it?"},
            {"speaker": "agent", "start_time": 39.0, "end_time": 41.2, "text": "Already done. You'll see a credit on your next bill. Again, I'm very sorry."}
        ]
    },
    # Call 4 - Support: Device issue
    {
        "call_id": 4,
        "metadata": {
            "call_type": "support",
            "agent_name": "David",
            "duration": 55.8,
            "sentiment": "mixed",
            "issue_category": "device problem",
            "issue_resolved": False
        },
        "conversation": [
            {"speaker": "ivr", "start_time": 0.0, "end_time": 4.5, "text": "Thank you for calling Telecom Haiku support. For technical support, press 1. For billing, press 2."},
            {"speaker": "agent", "start_time": 5.8, "end_time": 11.2, "text": "Hey there, I'm David from tech support. What's the trouble?"},
            {"speaker": "caller", "start_time": 12.0, "end_time": 21.3, "text": "My router is being really weird. It like keeps restarting every 10 minutes or so. One minute everything works fine and then it just shuts down and reboots. Very frustrating."},
            {"speaker": "agent", "start_time": 22.0, "end_time": 28.5, "text": "That does sound frustrating. Have you checked if it's getting too hot? Sometimes these devices overheat if they don't have proper ventilation."},
            {"speaker": "caller", "start_time": 29.2, "end_time": 35.7, "text": "Actually, now that you mention it, yeah it is pretty warm. Like, I can barely hold my hand on top of it. Could that be the problem?"},
            {"speaker": "agent", "start_time": 36.3, "end_time": 43.9, "text": "That's definitely it. Here's what I'd recommend: move it to a place with better airflow, away from walls or cabinets. See if that helps first."},
            {"speaker": "caller", "start_time": 44.5, "end_time": 55.8, "text": "Okay, I'm moving it now... let me put it on the shelf instead of in the cabinet. We'll see if that helps. If it doesn't, should I call back?"}
        ]
    },
    # Call 5 - Sales: Bundle inquiry
    {
        "call_id": 5,
        "metadata": {
            "call_type": "sales",
            "agent_name": "Lisa",
            "duration": 44.1,
            "sentiment": "positive",
            "product_category": "Bundle",
            "sale_completed": True
        },
        "conversation": [
            {"speaker": "ivr", "start_time": 0.0, "end_time": 5.2, "text": "Welcome to Telecom Haiku. Thank you for your interest in our services. Please hold for a sales representative."},
            {"speaker": "agent", "start_time": 6.5, "end_time": 12.3, "text": "Hi, thanks for calling! I'm Lisa. Are you interested in learning about our bundle packages?"},
            {"speaker": "caller", "start_time": 13.1, "end_time": 20.5, "text": "Yeah actually, I'm paying for like three different services separately and it's getting expensive. I heard you guys have something where you bundle them all together?"},
            {"speaker": "agent", "start_time": 21.2, "end_time": 28.9, "text": "You're absolutely right. Most customers save about 30 percent when they bundle internet, mobile, and TV with us. Would that interest you?"},
            {"speaker": "caller", "start_time": 29.6, "end_time": 36.3, "text": "That sounds amazing. Yeah, I want all three of those. What would it cost me? And are there any hidden fees?"},
            {"speaker": "agent", "start_time": 37.0, "end_time": 44.1, "text": "No hidden fees, I promise. We can get you set up at 99 dollars a month for everything. Want to move forward?"},
            {"speaker": "caller", "start_time": 44.6, "end_time": 45.0, "text": "Yes!"}
        ]
    }
]

# Save calls 1-5 first as examples
for call in calls_data:
    filename = f"call_{call['call_id']:06d}.json"
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w') as f:
        json.dump(call, f, indent=2)
    print(f"Saved {filename}")

print(f"Batch 1 sample: Created {len(calls_data)} calls")
