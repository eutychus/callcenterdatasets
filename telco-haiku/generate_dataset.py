#!/usr/bin/env python3
"""
Enhanced synthetic call center dataset generator for Telecom Haiku
Creates highly varied and realistic call center conversations
"""

import json
import csv
import random
import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import math

# Configuration
NUM_DOCUMENTS = 2000
OUTPUT_DIR = Path(__file__).parent / "calls"
INDEX_FILE = Path(__file__).parent / "index.csv"

# Seed for reproducibility
random.seed(42)

# ============================================================================
# COMPREHENSIVE DATA DEFINITIONS FOR VARIETY
# ============================================================================

CALL_TYPES = ["support", "sales", "billing", "technical", "account", "retention", "general"]

AGENT_NAMES = ["Sarah", "Mike", "Jennifer", "David", "Lisa", "Robert", "Emily", "James",
               "Amanda", "Chris", "Susan", "Mark", "Patricia", "Daniel"]

# Filler words and natural speech patterns
FILLERS = ["um", "uh", "like", "you know", "well", "so", "actually", "basically", "kinda", "sorta"]

# Interruptions and natural conversational elements
INTERRUPTIONS = ["sorry", "hold on", "wait", "just a second", "let me check", "hang on", "one moment"]

# Rich set of support issues with variants
SUPPORT_ISSUES = {
    "connectivity": [
        "my internet keeps dropping",
        "I'm having connectivity issues",
        "my connection is unstable",
        "I lose connection every few minutes",
        "can't stay connected for more than a minute"
    ],
    "speed": [
        "my speeds are really slow today",
        "I'm only getting like half my normal speed",
        "pages are taking forever to load",
        "my download speed is terrible",
        "streaming is buffering constantly"
    ],
    "device": [
        "my modem is acting weird",
        "the router keeps resetting",
        "I can't get my device to connect",
        "there's a red light on my modem",
        "my router stopped working"
    ],
    "service": [
        "I'm not getting service in certain rooms",
        "my wifi coverage is patchy",
        "service keeps cutting out",
        "there's a dead zone in my house",
        "signal keeps dropping"
    ],
    "billing_issue": [
        "I was charged twice",
        "there's an unexpected charge",
        "my bill is way higher than normal",
        "I don't think I should be charged this",
        "can you explain this charge"
    ],
    "account_access": [
        "I can't log into my account",
        "I forgot my password",
        "my account is locked",
        "I can't reset my password",
        "it says my account has an issue"
    ]
}

# Sales inquiries with variety
SALES_QUERIES = {
    "upgrade": [
        "I'm interested in upgrading my plan",
        "do you have any better plans available",
        "what are my upgrade options",
        "I need more data",
        "is there a faster plan I can get"
    ],
    "new_service": [
        "I want to add TV service",
        "can I bundle my services",
        "what packages do you offer",
        "I'm thinking about adding a line",
        "do you have any promotions"
    ],
    "device": [
        "I need a new phone",
        "can I get a device with my plan",
        "what phones are available",
        "do you offer device payment plans",
        "I'm interested in a new router"
    ],
    "information": [
        "I want to know about your plans",
        "what's different about your service",
        "how much does it cost",
        "what speeds can I get",
        "are there any special offers"
    ]
}

# Billing scenarios
BILLING_ISSUES = {
    "dispute": [
        "I need to dispute a charge",
        "this charge shouldn't be here",
        "I was overcharged",
        "can you remove this charge",
        "why am I being charged for this"
    ],
    "payment": [
        "I need to make a payment",
        "what's my current balance",
        "when is my payment due",
        "can I set up autopay",
        "what payment methods do you accept"
    ],
    "promotion": [
        "do you have any promotions",
        "can I get a discount",
        "I saw an offer online",
        "are there loyalty discounts",
        "can you lower my bill"
    ]
}

# Technical issues
TECHNICAL_ISSUES = {
    "setup": [
        "I just got my modem and don't know how to set it up",
        "how do I connect everything",
        "can you walk me through the setup",
        "I can't figure out how to configure this",
        "what cables do I need"
    ],
    "troubleshooting": [
        "something's not working right",
        "the signal is weak",
        "I keep getting error messages",
        "it's not working like it used to",
        "something changed and now it's slow"
    ],
    "device_issue": [
        "my modem is overheating",
        "there are lights flashing oddly",
        "I hear a strange noise",
        "it's not responding",
        "I need to reset it"
    ]
}

# Retention/churn scenarios
RETENTION_ISSUES = {
    "competitor": [
        "I got an offer from another provider",
        "your competitor is cheaper",
        "I'm looking at switching",
        "another company has better service",
        "I found a better deal elsewhere"
    ],
    "service_complaint": [
        "I'm really not happy with the service",
        "the quality has gone downhill",
        "I've had too many outages",
        "your customer service is frustrating",
        "I don't think it's worth the price"
    ],
    "leaving": [
        "I want to cancel my service",
        "I need to disconnect",
        "can you process my cancellation",
        "I'm done with this company",
        "when can I terminate my contract"
    ]
}

# Resolutions and outcomes
RESOLUTIONS = {
    "support": [
        "the issue was resolved",
        "a service call was scheduled",
        "we identified a network issue and it should be fixed",
        "the device needs to be replaced",
        "we're escalating to our technical team",
        "it was a software issue that's now updated"
    ],
    "sales": [
        "the customer purchased an upgrade",
        "the customer wasn't interested",
        "they want to think about it",
        "we scheduled a follow-up",
        "they purchased a new device",
        "they added a service"
    ],
    "billing": [
        "the charge was reversed",
        "we applied a credit",
        "the dispute will be investigated",
        "we set up a payment plan",
        "autopay was activated"
    ]
}

# Agent responses with variety
AGENT_RESPONSES = {
    "empathy": [
        "I completely understand your frustration",
        "that must be really annoying",
        "I'm sorry you're experiencing this",
        "I can see why that would be frustrating",
        "let me help you resolve this"
    ],
    "investigation": [
        "let me look into your account",
        "can you give me your account number",
        "let me pull up your information",
        "I'm checking our system now",
        "hold on while I investigate"
    ],
    "solution_offer": [
        "I can help you with that",
        "here's what we can do",
        "I have a solution for you",
        "let me walk you through this",
        "here are your options"
    ],
    "technical": [
        "let's try restarting the device",
        "can you check if the lights are green",
        "try unplugging it for 30 seconds",
        "what error message are you seeing",
        "let me see if there's an outage in your area"
    ],
    "closing": [
        "is there anything else I can help with",
        "thanks for choosing us",
        "we appreciate your business",
        "feel free to call back anytime",
        "have a great day"
    ]
}

# Customer responses - diverse and realistic
CUSTOMER_RESPONSES = {
    "affirmative": [
        "yeah, okay",
        "sure, I can try that",
        "alright, let's do it",
        "that sounds good",
        "I can do that"
    ],
    "questioning": [
        "how long will that take",
        "is there a charge",
        "will that really fix it",
        "how soon can you do that",
        "are you sure about that"
    ],
    "frustrated": [
        "I've already tried that",
        "this shouldn't be happening",
        "I'm not happy with this",
        "this is ridiculous",
        "I can't believe I have to deal with this"
    ],
    "agreement": [
        "yeah, I think that makes sense",
        "okay, that works for me",
        "I'm on board with that",
        "that sounds reasonable",
        "I can live with that"
    ],
    "concern": [
        "I'm worried that won't work",
        "I'm not sure about that",
        "that seems complicated",
        "will it take long",
        "what if it doesn't work"
    ]
}

def add_filler(text: str) -> str:
    """Randomly add filler words to make speech more natural"""
    if random.random() > 0.6:
        filler = random.choice(FILLERS)
        if random.random() > 0.5:
            return f"{filler}, {text}"
        else:
            return f"{text}, {filler}"
    return text

def create_interruption(text: str) -> str:
    """Add interruptions and stutters for naturalness"""
    if random.random() > 0.7:
        interruption = random.choice(INTERRUPTIONS)
        return f"{interruption}... {text}"
    elif random.random() > 0.5:
        # Stutter/repeat
        words = text.split()
        if len(words) > 1:
            first_word = words[0]
            return f"{first_word}... {first_word} {' '.join(words[1:])}"
    return text

def calculate_speech_duration(text: str, speaking_rate: float = 150) -> float:
    """Calculate duration based on word count and speaking rate"""
    words = len(text.split())
    # Speaking rate in words per minute, convert to seconds
    duration = (words / speaking_rate) * 60
    # Add variation
    variation = random.uniform(0.85, 1.15)
    return round(duration * variation, 1)

def generate_dynamic_conversation(call_type: str) -> Tuple[List[Dict], Dict]:
    """Generate highly varied and natural conversation"""
    conversation = []
    current_time = 0.0
    metadata = {
        "call_type": call_type,
        "agent_name": random.choice(AGENT_NAMES),
        "duration": 0,
        "sentiment": random.choice(["positive", "neutral", "negative", "mixed"]),
    }

    # IVR greeting (varied)
    ivr_options = [
        "Welcome to Telecom Haiku. Press 1 for English, 2 for Spanish.",
        "Thank you for calling Telecom Haiku. Your call is important to us.",
        "Welcome. Please listen carefully as our menu has changed.",
        "Thank you for contacting Telecom Haiku support.",
        "Please hold while we route you to the next available representative.",
    ]

    ivr_phrase = random.choice(ivr_options)
    ivr_duration = calculate_speech_duration(ivr_phrase, 160)
    conversation.append({
        "speaker": "ivr",
        "start_time": current_time,
        "end_time": current_time + ivr_duration,
        "text": ivr_phrase
    })
    current_time += ivr_duration + random.uniform(1.0, 2.5)

    # Agent greeting - contextual and varied
    agent_name = metadata["agent_name"]
    greetings = {
        "support": [
            f"Hi, thanks for calling. This is {agent_name} from technical support.",
            f"Hello! I'm {agent_name}. How can I help you with your service today?",
            f"Hi there! {agent_name} speaking. What seems to be the issue?",
            f"Good, this is {agent_name}. I'm here to help with any technical issues.",
        ],
        "sales": [
            f"Hey, thanks for calling! This is {agent_name}. I'd love to tell you about some great offers.",
            f"Hello! {agent_name} here with our sales team. Are you interested in learning about our plans?",
            f"Hi! Welcome to Telecom Haiku. {agent_name} speaking. What brings you in today?",
        ],
        "billing": [
            f"Hi, this is {agent_name} from billing. How can I assist with your account?",
            f"Hello! {agent_name} speaking. I'm here to help with any billing questions.",
            f"Thanks for calling. {agent_name} here. What can I do for you?",
        ],
        "technical": [
            f"Hi! {agent_name} from technical support. Let's get your device working.",
            f"Hello, {agent_name} here. What device are we troubleshooting today?",
            f"Thanks for calling. {agent_name} with technical support.",
        ],
        "account": [
            f"Hi, {agent_name} with account services here. How can I help?",
            f"Hello! {agent_name} speaking. What can I do with your account today?",
        ],
        "retention": [
            f"Hi, thanks for calling. {agent_name} here. I see you've been with us a while.",
            f"Hello! {agent_name} speaking. I appreciate your business.",
        ],
        "general": [
            f"Hi! {agent_name} here. How can I help you?",
            f"Hello, thanks for calling. {agent_name} speaking.",
        ]
    }

    greeting = random.choice(greetings.get(call_type, greetings["general"]))
    greeting_duration = calculate_speech_duration(greeting)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + greeting_duration,
        "text": greeting
    })
    current_time += greeting_duration + random.uniform(0.8, 1.8)

    # Customer initial response
    customer_responses = [
        "Yeah, hi. I'm having an issue.",
        "Thanks for picking up.",
        "Hi, uh, I'm calling because of a problem.",
        "Hey, thanks. Yeah, I need help with something.",
        "Hi! So I've been having some trouble.",
    ]

    cust_resp = random.choice(customer_responses)
    cust_resp = add_filler(cust_resp)
    resp_duration = calculate_speech_duration(cust_resp)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + resp_duration,
        "text": cust_resp
    })
    current_time += resp_duration + random.uniform(0.5, 1.5)

    # Main issue/request - varies by call type
    if call_type == "support":
        metadata["issue_category"] = random.choice(list(SUPPORT_ISSUES.keys()))
        issue_text = random.choice(SUPPORT_ISSUES[metadata["issue_category"]])
        metadata["issue"] = metadata["issue_category"]
    elif call_type == "sales":
        metadata["product_category"] = random.choice(["Mobile Plan", "Broadband", "TV Package", "Bundle", "Device", "Add-on"])
        query = random.choice(list(SALES_QUERIES.keys()))
        issue_text = random.choice(SALES_QUERIES[query])
        metadata["inquiry_type"] = query
    elif call_type == "billing":
        issue_key = random.choice(list(BILLING_ISSUES.keys()))
        issue_text = random.choice(BILLING_ISSUES[issue_key])
        metadata["billing_issue"] = issue_key
    elif call_type == "technical":
        issue_key = random.choice(list(TECHNICAL_ISSUES.keys()))
        issue_text = random.choice(TECHNICAL_ISSUES[issue_key])
        metadata["technical_issue"] = issue_key
    elif call_type == "retention":
        issue_key = random.choice(list(RETENTION_ISSUES.keys()))
        issue_text = random.choice(RETENTION_ISSUES[issue_key])
        metadata["churn_reason"] = issue_key
    else:
        issue_text = "I had a question about my service."
        metadata["issue"] = "general"

    # Add natural variation to issue description
    issue_text = add_filler(issue_text)
    issue_text = create_interruption(issue_text)

    issue_duration = calculate_speech_duration(issue_text)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + issue_duration,
        "text": issue_text
    })
    current_time += issue_duration + random.uniform(1.0, 2.5)

    # Agent acknowledges and investigates
    ack = random.choice(AGENT_RESPONSES["empathy"])
    ack = add_filler(ack)
    ack_duration = calculate_speech_duration(ack)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + ack_duration,
        "text": ack
    })
    current_time += ack_duration + random.uniform(0.5, 1.5)

    # Investigation phase
    if call_type in ["support", "billing", "account"]:
        investigation = random.choice(AGENT_RESPONSES["investigation"])
        investigation = create_interruption(investigation)
        inv_duration = calculate_speech_duration(investigation)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + inv_duration,
            "text": investigation
        })
        current_time += inv_duration + random.uniform(1.5, 3.0)

        # Customer provides account info
        account_responses = [
            "Sure, it's on the bill.",
            "Yeah, let me find that.",
            "It's 555-1234.",
            "It's starting with a C... CUST12345.",
            "Okay, hold on."
        ]
        account_resp = random.choice(account_responses)
        account_resp = add_filler(account_resp)
        account_dur = calculate_speech_duration(account_resp)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + account_dur,
            "text": account_resp
        })
        current_time += account_dur + random.uniform(1.0, 2.0)

    # Problem-solving phase with interaction
    for exchange in range(random.randint(1, 3)):
        # Agent offers help
        agent_help = random.choice(AGENT_RESPONSES["solution_offer"])
        if call_type == "technical":
            agent_help = random.choice(AGENT_RESPONSES["technical"])

        agent_help = add_filler(agent_help)
        help_duration = calculate_speech_duration(agent_help)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + help_duration,
            "text": agent_help
        })
        current_time += help_duration + random.uniform(0.8, 2.0)

        # Customer responds
        cust_choice = random.choice(CUSTOMER_RESPONSES["affirmative"] +
                                   CUSTOMER_RESPONSES["questioning"] +
                                   CUSTOMER_RESPONSES["concern"])
        cust_choice = add_filler(cust_choice)
        cust_dur = calculate_speech_duration(cust_choice)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + cust_dur,
            "text": cust_choice
        })
        current_time += cust_dur + random.uniform(0.5, 1.5)

    # Additional exchanges or complications
    if random.random() > 0.5:
        complication = random.choice([
            "Actually, there's one more thing...",
            "Oh, and while we're at it...",
            "By the way, I also have a question...",
            "There's actually another issue...",
        ])
        complication = add_filler(complication)
        comp_dur = calculate_speech_duration(complication)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + comp_dur,
            "text": complication
        })
        current_time += comp_dur + random.uniform(0.5, 1.2)

        agent_follow = random.choice(AGENT_RESPONSES["solution_offer"])
        agent_follow = add_filler(agent_follow)
        follow_dur = calculate_speech_duration(agent_follow)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + follow_dur,
            "text": agent_follow
        })
        current_time += follow_dur + random.uniform(0.5, 1.0)

    # Closing sequence
    closing_prompts = [
        "Is there anything else I can help with today?",
        "Are we all set?",
        "Does that work for you?",
        "Any other questions I can answer?",
    ]

    closing = random.choice(closing_prompts)
    closing_dur = calculate_speech_duration(closing)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + closing_dur,
        "text": closing
    })
    current_time += closing_dur + random.uniform(0.5, 1.0)

    # Customer closing
    customer_closings = [
        "No, that's all. Thanks!",
        "I think that covers it. Thanks for your help.",
        "Nope, that should do it. I appreciate it.",
        "That's everything. Thanks so much!",
        "Yeah, that's good. Thanks!",
    ]

    cust_closing = random.choice(customer_closings)
    cust_closing = add_filler(cust_closing)
    cust_close_dur = calculate_speech_duration(cust_closing)
    conversation.append({
        "speaker": "caller",
        "start_time": current_time,
        "end_time": current_time + cust_close_dur,
        "text": cust_closing
    })
    current_time += cust_close_dur + random.uniform(0.3, 1.0)

    # Final agent farewell
    farewells = [
        "Thanks for choosing Telecom Haiku!",
        "Have a great day!",
        "We appreciate your business.",
        "Thanks for calling, and take care.",
        "Enjoy your service!",
    ]

    farewell = random.choice(farewells)
    farewell_dur = calculate_speech_duration(farewell)
    conversation.append({
        "speaker": "agent",
        "start_time": current_time,
        "end_time": current_time + farewell_dur,
        "text": farewell
    })
    current_time += farewell_dur

    # Set outcomes based on call type
    if call_type == "support":
        metadata["issue_resolved"] = random.choice([True, False, "partial"])
        metadata["resolution_type"] = random.choice(RESOLUTIONS["support"])
    elif call_type == "sales":
        metadata["sale_completed"] = random.choice([True, False])
        metadata["resolution_type"] = random.choice(RESOLUTIONS["sales"])
    elif call_type == "billing":
        metadata["issue_resolved"] = random.choice([True, False])
        metadata["resolution_type"] = random.choice(RESOLUTIONS["billing"])
    else:
        metadata["issue_resolved"] = random.choice([True, False, "escalated"])

    metadata["duration"] = round(current_time, 1)
    return conversation, metadata

def save_call_as_json(call_id: int, conversation: List[Dict], metadata: Dict) -> str:
    """Save call as JSON file with conversation as JSON array"""
    filename = f"call_{call_id:06d}.json"
    filepath = OUTPUT_DIR / filename

    document = {
        "call_id": call_id,
        "metadata": metadata,
        "conversation": conversation  # JSON array instead of embedded CSV
    }

    with open(filepath, 'w') as f:
        json.dump(document, f, indent=2)

    return filename

def generate_all_documents(num_docs: int):
    """Generate all synthetic call documents"""
    index_data = []

    print(f"Generating {num_docs} synthetic call center documents...")

    for i in range(1, num_docs + 1):
        call_type = random.choice(CALL_TYPES)
        conversation, metadata = generate_dynamic_conversation(call_type)
        filename = save_call_as_json(i, conversation, metadata)

        # Create index row
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
            "issue_category": metadata.get("issue_category", metadata.get("billing_issue", metadata.get("technical_issue", metadata.get("churn_reason", "general")))),
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

        if i % 200 == 0:
            print(f"  Generated {i}/{num_docs} documents...")

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
