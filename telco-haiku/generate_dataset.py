#!/usr/bin/env python3
"""
Generate synthetic call center dataset for Telecom Haiku
Creates 2000 realistic call center conversations with metadata
"""

import json
import csv
import random
import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import io

# Configuration
NUM_DOCUMENTS = 2000
OUTPUT_DIR = Path(__file__).parent / "calls"
INDEX_FILE = Path(__file__).parent / "index.csv"

# Seed for reproducibility
random.seed(42)

# Call center data
CALL_TYPES = ["support", "sales", "billing", "technical", "account", "retention", "general"]
AGENT_NAMES = ["Sarah", "Mike", "Jennifer", "David", "Lisa", "Robert", "Emily", "James"]
ISSUES = {
    "support": [
        "internet is down", "wifi not working", "can't connect to service",
        "experiencing slow speeds", "getting disconnected", "need password reset",
        "can't access account", "billing question", "service outage", "line quality"
    ],
    "sales": [
        "interested in new plan", "upgrade options", "special offers",
        "bundle packages", "device purchase", "service expansion"
    ],
    "billing": [
        "late payment", "dispute charge", "cancellation", "payment method",
        "refund request", "promos and discounts", "usage charges"
    ],
    "technical": [
        "modem issues", "router configuration", "device compatibility",
        "software update", "connection setup", "signal strength"
    ],
    "retention": [
        "considering leaving", "competitor offer", "service complaint",
        "switching provider", "dissatisfied with service"
    ]
}

RESOLUTIONS = ["resolved", "escalated", "scheduled followup", "partial resolution", "callback needed"]
PRODUCTS = ["Mobile Plan", "Broadband", "TV Package", "Bundles", "Device", "Add-on Service"]
SENTIMENT = ["positive", "neutral", "negative"]
ISSUE_CATEGORIES = [
    "connectivity", "billing", "device", "account", "service_quality",
    "technical_support", "sales_inquiry", "retention", "complaint", "inquiry"
]

# Realistic speech patterns for IVR
IVR_PHRASES = [
    "Welcome to Telecom Haiku. For English, press 1.",
    "Thank you for calling. Please listen carefully as our menu has changed.",
    "If you're calling about billing, press 1. For support, press 2. For sales, press 3.",
    "Your call is important to us. Please hold while we connect you.",
    "Please enter your account number followed by the pound sign.",
    "I'm sorry, I didn't understand that. Please try again.",
    "Thank you. Connecting you to the next available agent.",
]

# Agent greetings based on call type
AGENT_GREETINGS = {
    "support": [
        "Hi there! This is {agent} from Technical Support. How can I help you today?",
        "Hello, thanks for calling. I'm {agent}. What seems to be the issue?",
        "Good day! {agent} here from our support team. What can I assist with?",
    ],
    "sales": [
        "Hi! This is {agent} with our sales team. Are you interested in any of our plans?",
        "Hello! {agent} speaking. I'd love to tell you about our latest offers.",
        "Hi there! Welcome to Telecom Haiku sales. {agent} here. What brings you in today?",
    ],
    "billing": [
        "Hello, {agent} from billing. How can I assist with your account?",
        "Hi! This is {agent}. I'm here to help with any billing questions.",
        "Good day, {agent} here. What billing matter can I help you with?",
    ],
    "technical": [
        "Hi, {agent} technical support here. Let me help you troubleshoot.",
        "Hello! I'm {agent}. Let's get your device working again.",
        "Hi there, {agent} here. What device are we troubleshooting today?",
    ],
    "retention": [
        "Hello, this is {agent}. I see you've been with us for a while.",
        "Hi! {agent} here. I'd love to make sure we're taking care of you.",
    ],
    "general": [
        "Hello! {agent} here. How may I assist you?",
        "Hi, this is {agent}. What can I do for you today?",
    ],
    "account": [
        "Hi! {agent} with account services. What do you need help with?",
        "Hello, {agent} here. How can I help with your account?",
    ]
}

# Customer phrases (realistic with interruptions)
CUSTOMER_PHRASES = {
    "greeting": [
        "Hi, yes, I'm having an issue with my service",
        "Hello, uh, I've been trying to... my internet isn't working",
        "Hi there. So I've got a problem...",
        "Yeah, hello, um, my service seems to be down",
    ],
    "issue_description": [
        "Yeah, so my internet's been really slow today",
        "Um, I can't... I keep getting disconnected",
        "The thing is, when I try to load pages it just... it hangs",
        "Well, basically my speeds have gone way down. Like, really slow",
        "It started maybe an hour ago and... yeah, nothing's working",
    ],
    "agreement": [
        "Yeah, that sounds good",
        "Okay, sure, I can try that",
        "Alright, let me try that",
        "Uh-huh, okay, I got it",
        "Yeah, sounds good to me",
    ],
    "disagreement": [
        "Um, well... I already tried that",
        "I don't think that's gonna work",
        "Yeah, but I already did that before I called",
        "Hmm, no, that doesn't seem to help",
    ],
    "additional_issues": [
        "Oh, and also... could you look at my bill?",
        "By the way, um, I had another question",
        "While we're at it, can you... can you check something else?",
        "Actually, there's one more thing...",
    ],
    "closing": [
        "Okay, great, thanks so much",
        "Alright, I really appreciate it",
        "Thanks for your help, that was really quick",
        "Okay, uh, thanks. That should work",
        "Yeah, okay, thanks a lot",
    ],
    "frustration": [
        "This is... this is ridiculous",
        "I've been trying to get this fixed for days",
        "This is pretty frustrating",
        "I'm really not happy with the service",
    ]
}

# Agent phrases
AGENT_PHRASES = {
    "acknowledgment": [
        "I understand, let me look into that for you.",
        "Okay, I see what you mean. Let me check on that.",
        "I got it. Let me pull up your account here.",
        "Yeah, let's troubleshoot that together.",
    ],
    "troubleshooting": [
        "Have you tried restarting your modem?",
        "Can you check if the lights on your router are on?",
        "What do you see when you open your browser?",
        "Okay, and how long has this been happening?",
        "Let me check our systems to see if there's an outage in your area.",
    ],
    "solution": [
        "I think I found the issue. Let me reset your connection.",
        "Looks like we need to restart your modem. Can you do that?",
        "I'm going to push a software update to your device.",
        "That should fix it. Let me verify everything looks good.",
    ],
    "follow_up": [
        "Let me send that information to your email.",
        "You should see improvement within the next 15 minutes.",
        "If it happens again, just give us a call back.",
        "Is there anything else I can help you with today?",
    ],
    "apology": [
        "I sincerely apologize for the inconvenience.",
        "Sorry you've been experiencing this issue.",
        "We really appreciate your patience.",
        "I'm sorry we didn't catch this sooner.",
    ],
    "sales_pitch": [
        "While I have you, we actually just launched a new plan that might interest you.",
        "Our customers are really happy with the new bundled package.",
        "If you upgrade now, we can waive your installation fee.",
        "We have a special promotion running through the end of the month.",
    ]
}

def calculate_speech_duration(text: str) -> float:
    """Estimate duration in seconds based on speech rate (150 words per minute)"""
    words = len(text.split())
    # Average 150 words per minute = 2.5 words per second
    base_duration = words / 2.5
    # Add some variation (±10%)
    variation = random.uniform(0.9, 1.1)
    return round(base_duration * variation, 1)

def generate_conversation(call_type: str) -> Tuple[List[Dict], Dict]:
    """Generate a realistic conversation based on call type"""
    conversation = []
    current_time = 0.0
    metadata = {
        "call_type": call_type,
        "agent_name": random.choice(AGENT_NAMES),
        "duration": 0,
        "sentiment": random.choice(SENTIMENT),
    }

    # IVR portion (1-3 seconds)
    ivr_phrase = random.choice(IVR_PHRASES)
    ivr_duration = calculate_speech_duration(ivr_phrase)
    conversation.append({
        "speaker": "ivr",
        "start_time": current_time,
        "end_time": current_time + ivr_duration,
        "text": ivr_phrase
    })
    current_time += ivr_duration + random.uniform(0.5, 1.5)  # Gap before agent speaks

    # Agent greeting
    agent_greeting = random.choice(AGENT_GREETINGS.get(call_type, AGENT_GREETINGS["general"]))
    agent_greeting = agent_greeting.format(agent=metadata["agent_name"])
    greeting_duration = calculate_speech_duration(agent_greeting)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + greeting_duration,
        "text": agent_greeting
    })
    current_time += greeting_duration + random.uniform(0.8, 1.5)

    # Customer response
    customer_greeting = random.choice(CUSTOMER_PHRASES["greeting"])
    greeting_dur = calculate_speech_duration(customer_greeting)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + greeting_dur,
        "text": customer_greeting
    })
    current_time += greeting_dur + random.uniform(0.5, 1.2)

    # Main issue discussion
    if call_type in ISSUES:
        issue_list = ISSUES[call_type]
        issue = random.choice(issue_list)
        metadata["issue"] = issue
    else:
        issue = "general inquiry"
        metadata["issue"] = issue

    # Customer describes issue (with possible interruptions)
    customer_issue = random.choice(CUSTOMER_PHRASES["issue_description"])
    customer_issue_dur = calculate_speech_duration(customer_issue)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + customer_issue_dur,
        "text": customer_issue
    })
    current_time += customer_issue_dur + random.uniform(0.3, 1.0)

    # Agent acknowledgment
    agent_ack = random.choice(AGENT_PHRASES["acknowledgment"])
    ack_dur = calculate_speech_duration(agent_ack)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + ack_dur,
        "text": agent_ack
    })
    current_time += ack_dur + random.uniform(1.0, 2.0)

    # Troubleshooting or resolution exchange
    if call_type == "sales":
        # Sales calls focus on product pitch
        agent_phrase = random.choice(AGENT_PHRASES["sales_pitch"])
        agent_ack2 = random.choice(AGENT_PHRASES["follow_up"])
        metadata["sale_completed"] = random.choice([True, False])
        metadata["product_category"] = random.choice(PRODUCTS)
    elif call_type == "support":
        agent_phrase = random.choice(AGENT_PHRASES["troubleshooting"])
        metadata["issue_resolved"] = random.choice([True, False])
        metadata["resolution_type"] = random.choice(RESOLUTIONS)
    else:
        agent_phrase = random.choice(AGENT_PHRASES["troubleshooting"])
        metadata["issue_resolved"] = random.choice([True, False])

    agent_phrase_dur = calculate_speech_duration(agent_phrase)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + agent_phrase_dur,
        "text": agent_phrase
    })
    current_time += agent_phrase_dur + random.uniform(0.8, 2.0)

    # Customer response
    customer_response = random.choice(CUSTOMER_PHRASES["agreement"])
    resp_dur = calculate_speech_duration(customer_response)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + resp_dur,
        "text": customer_response
    })
    current_time += resp_dur + random.uniform(0.5, 1.0)

    # Possible additional agent phrase or solution
    if random.random() > 0.3:
        additional = random.choice(AGENT_PHRASES["solution"])
        add_dur = calculate_speech_duration(additional)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + add_dur,
            "text": additional
        })
        current_time += add_dur + random.uniform(0.5, 1.5)

    # Follow-up from agent
    followup = random.choice(AGENT_PHRASES["follow_up"])
    followup_dur = calculate_speech_duration(followup)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + followup_dur,
        "text": followup
    })
    current_time += followup_dur + random.uniform(0.5, 1.0)

    # Customer closing
    customer_close = random.choice(CUSTOMER_PHRASES["closing"])
    close_dur = calculate_speech_duration(customer_close)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + close_dur,
        "text": customer_close
    })
    current_time += close_dur

    metadata["duration"] = round(current_time, 1)
    return conversation, metadata

def save_call_as_json(call_id: int, conversation: List[Dict], metadata: Dict) -> str:
    """Save call as JSON file with embedded CSV"""
    filename = f"call_{call_id:06d}.json"
    filepath = OUTPUT_DIR / filename

    # Create CSV in memory
    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=["speaker", "start_time", "end_time", "text"])
    csv_writer.writeheader()
    csv_writer.writerows(conversation)
    csv_content = csv_buffer.getvalue()

    # Create JSON document
    document = {
        "call_id": call_id,
        "metadata": metadata,
        "conversation_csv": csv_content
    }

    with open(filepath, 'w') as f:
        json.dump(document, f, indent=2)

    return filename

def generate_all_documents(num_docs: int):
    """Generate all synthetic call documents"""
    index_data = []

    print(f"Generating {num_docs} synthetic call center documents...")

    for i in range(1, num_docs + 1):
        # Choose call type
        call_type = random.choice(CALL_TYPES)

        # Generate conversation
        conversation, metadata = generate_conversation(call_type)

        # Save as JSON
        filename = save_call_as_json(i, conversation, metadata)

        # Prepare index row
        call_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 90))
        call_time = f"{random.randint(8, 17):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"

        index_row = {
            "filename": filename,
            "call_id": i,
            "call_type": call_type,
            "date": call_date.strftime("%Y-%m-%d"),
            "time": call_time,
            "duration_seconds": metadata["duration"],
            "agent_name": metadata["agent_name"],
            "sentiment": metadata["sentiment"],
            "issue_resolved": metadata.get("issue_resolved", "N/A"),
            "issue_category": random.choice(ISSUE_CATEGORIES),
            "sale_completed": metadata.get("sale_completed", "N/A"),
            "product_category": metadata.get("product_category", "N/A"),
            "customer_id": f"CUST{random.randint(10000, 99999)}",
            "agent_id": f"AGENT{random.randint(1000, 9999)}",
            "language": "English",
            "call_quality": random.choice(["excellent", "good", "fair", "poor"]),
            "handle_time_efficient": random.choice(["yes", "no"]),
            "follow_up_required": random.choice(["yes", "no"]),
        }

        index_data.append(index_row)

        # Progress indicator
        if i % 200 == 0:
            print(f"  Generated {i}/{num_docs} documents...")

    # Write index CSV
    print(f"Writing index file to {INDEX_FILE}...")
    fieldnames = list(index_data[0].keys())
    with open(INDEX_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(index_data)

    print(f"\nDataset generation complete!")
    print(f"  Total documents: {num_docs}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Index file: {INDEX_FILE}")

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_all_documents(NUM_DOCUMENTS)
