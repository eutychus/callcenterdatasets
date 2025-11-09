#!/usr/bin/env python3
"""
Natural call transcript generator for Telecom Haiku
Generates diverse, realistic conversations with minimal duplication
"""

import json
import csv
import random
import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib

NUM_DOCUMENTS = 2000
OUTPUT_DIR = Path(__file__).parent / "calls"
INDEX_FILE = Path(__file__).parent / "index.csv"

random.seed(42)

# ============================================================================
# EXTENSIVE NATURAL LANGUAGE VARIATION LIBRARY
# ============================================================================

class CallGenerator:
    """Generate naturally varied call transcripts"""

    def __init__(self):
        self.ivr_intros = [
            "Welcome to Telecom Haiku. Press 1 for English, 2 for Spanish.",
            "Thank you for calling Telecom Haiku. Please listen carefully as our menu has changed.",
            "You've reached Telecom Haiku customer service. For technical support, press 1. For billing, press 2. For sales, press 3.",
            "Welcome. Your call is important to us. Please hold while we connect you to the next available agent.",
            "Thank you for choosing Telecom Haiku. Press 1 to continue in English.",
            "Welcome to Telecom Haiku support. Please have your account number ready.",
            "Telecom Haiku customer service. How may we help you today?",
        ]

        self.agent_names = [
            "Sarah", "Mike", "Jennifer", "David", "Lisa", "Robert", "Emily", "James",
            "Amanda", "Chris", "Susan", "Mark", "Patricia", "Daniel", "Rachel", "Kevin"
        ]

        # Support call scenarios
        self.support_scenarios = [
            {
                "issue": "internet connectivity",
                "customer_opening": [
                    "Hi, yeah, I've been having really bad internet. Like, my connection keeps dropping every few minutes.",
                    "So I've got this problem where I can barely stay connected. It's been happening since yesterday.",
                    "My internet's been incredibly slow. Pages aren't loading, nothing's working properly.",
                    "I'm calling because my service just cut out. I can't even browse right now.",
                ],
                "agent_approaches": [
                    "I understand how frustrating that must be. Let me pull up your account and see what's going on.",
                    "That sounds really annoying. Okay, let me check on your service status and we'll figure this out.",
                    "I'm sorry you're experiencing that. Let me look into your account details.",
                    "That must be really frustrating. Can you tell me a little bit more about when this started?",
                ],
                "troubleshooting": [
                    "Have you tried restarting your modem and router? Sometimes that clears things up.",
                    "Let's do a quick restart. Can you unplug your modem for about 30 seconds?",
                    "First thing - have you rebooted your equipment recently?",
                    "Can you check if the lights on your modem are all green or if any are flashing red?",
                ],
                "resolution": [
                    "I'm pushing a software update to your modem right now. You should see improvement.",
                    "It looks like there's a node issue in your area. Our team is working on it.",
                    "We've identified the problem. Let me schedule a technician visit for you.",
                    "The connection looks stable now. Try a speed test and let me know.",
                ]
            },
            {
                "issue": "service quality",
                "customer_opening": [
                    "I'm calling because my WiFi signal is really weak in most rooms. I barely get bars.",
                    "The speeds you promised me in the contract? I'm getting maybe half of that.",
                    "My service has been degrading. It started out fast, but now it's painfully slow.",
                    "I keep getting disconnected from WiFi randomly throughout the day.",
                ],
                "agent_approaches": [
                    "Let me look into your current speed and service status.",
                    "I can definitely help with that. Let me check what's going on with your account.",
                    "Okay, let's see what the issue might be. I'm pulling up your information now.",
                ],
                "troubleshooting": [
                    "Sometimes interference can affect signal strength. Are you using a 5GHz network?",
                    "Let me check if we can optimize your connection. Have you moved your router recently?",
                    "We might need to adjust your setup. Where's your router located?",
                ],
                "resolution": [
                    "I'm going to send you a better router at no charge.",
                    "Let me upgrade your service tier. You should see much better speeds.",
                    "We're going to credit your account this month for the inconvenience.",
                ]
            },
            {
                "issue": "device problem",
                "customer_opening": [
                    "My modem just stopped working completely. The lights went off and now nothing.",
                    "I've got this modem that's making a weird buzzing sound. I think something's wrong with it.",
                    "The router keeps rebooting itself. It's like every hour it just powers down.",
                    "My equipment is overheating. The modem is really hot to the touch.",
                ],
                "agent_approaches": [
                    "That could be a hardware issue. Let me see if we need to replace it.",
                    "That's not normal. Let's walk through some basic checks first.",
                    "Okay, it sounds like the device might be failing. Let me figure out the best solution.",
                ],
                "troubleshooting": [
                    "Is it plugged in and is the outlet working? Let me confirm the basics first.",
                    "When did you last reboot it? Sometimes a factory reset helps.",
                    "Can you try a different power outlet? Sometimes that solves the problem.",
                ],
                "resolution": [
                    "We'll send you a replacement modem. It should arrive in 2-3 business days.",
                    "I'm shipping you a new unit express. It'll be there tomorrow.",
                    "You're still under warranty. We'll replace it at no cost.",
                ]
            },
            {
                "issue": "account access",
                "customer_opening": [
                    "I can't log into my account online. It says my password is wrong but I know it's correct.",
                    "My account is locked. I tried resetting my password but nothing happened.",
                    "I'm trying to check my bill but I forgot my login credentials.",
                    "Something's wrong with my account. It won't let me do anything online.",
                ],
                "agent_approaches": [
                    "Let me unlock that for you and get you back in.",
                    "I can help you regain access. Let me verify your information.",
                    "No problem, that happens all the time. We can fix that right now.",
                ],
                "troubleshooting": [
                    "Let me send you a password reset link to your email on file.",
                    "I'm going to unlock your account. Try logging in again in a few minutes.",
                    "Can you tell me the email address associated with your account?",
                ],
                "resolution": [
                    "Your account is unlocked now. Try resetting your password.",
                    "You should receive a reset email shortly. Click the link to create a new password.",
                    "You're all set. You should be able to log in now without any issues.",
                ]
            }
        ]

        # Sales scenarios
        self.sales_scenarios = [
            {
                "opening": [
                    "Hi, I was actually thinking about upgrading my plan. What options do you have?",
                    "I'm interested in getting faster speeds. What's available in my area?",
                    "Do you have any promotions running right now? I'm open to changing my service.",
                    "I saw an ad for a bundle package. Can you tell me about that?",
                ],
                "product_types": ["Mobile Plan", "Broadband", "TV Package", "Bundle", "Device", "Add-on"],
                "agent_pitches": [
                    "Actually, we just launched a new plan that's perfect for what you need.",
                    "We have some really good options right now that could save you money.",
                    "Let me show you some plans that are faster and in a similar price range.",
                    "We have a bundle offer that customers love. It might be perfect for you.",
                ],
                "customer_responses": [
                    "That sounds interesting. How much more would it be per month?",
                    "What's the difference between the tiers? I want to make sure I'm getting a good deal.",
                    "Can I try it without being locked in? I want to see if I like it first.",
                    "Is there an installation fee? I'd like to know the total cost.",
                ],
                "closing": [
                    "Okay, I'll sign up. When can you get me switched over?",
                    "That actually sounds like a better deal. Let's do it.",
                    "Yeah, I think I'll try it. Can you start that for me?",
                    "I'm interested but let me think about it and call back.",
                    "I appreciate the offer but I'll stick with what I have.",
                ]
            }
        ]

        # Billing scenarios
        self.billing_scenarios = [
            {
                "issue": "unexpected charge",
                "opening": [
                    "Why was I charged an extra 50 dollars this month? That's not right.",
                    "My bill is way too high. There's a charge I don't recognize.",
                    "I got my bill and there's something on there I didn't authorize.",
                    "Can you explain this charge? I don't remember agreeing to it.",
                ],
                "investigation": [
                    "Let me pull up your bill and see what that charge is for.",
                    "I can see that charge. Let me look into what it's for.",
                    "Okay, I see it too. Let me investigate that for you.",
                ],
                "explanation": [
                    "That was a late fee from last month. Let me see if I can waive it.",
                    "It looks like you were charged for an add-on service. Would you like me to remove it?",
                    "That appears to be a promotional fee that wasn't applied correctly.",
                    "We charged you for premium support. I can reverse that if you want.",
                ],
                "resolution": [
                    "I'm removing that charge and crediting your account.",
                    "Let me apply a credit. You shouldn't have been charged for that.",
                    "I'm going to have that reversed. You'll see the credit on your next bill.",
                ]
            },
            {
                "issue": "payment problem",
                "opening": [
                    "My payment didn't go through and now I'm worried my service will get cut off.",
                    "I tried to pay my bill but the system rejected my card.",
                    "I can't pay online. The website isn't accepting my payment.",
                    "Is my service going to be disconnected? I've been trying to pay.",
                ],
                "investigation": [
                    "Let me check the status of your account.",
                    "Let me see what's going on with your account.",
                ],
                "explanation": [
                    "It looks like there's an issue with the payment system on your end.",
                    "Your card might be expired or there could be a security hold.",
                    "Sometimes your bank blocks us for fraud protection.",
                ],
                "resolution": [
                    "Try updating your payment method online or I can process it over the phone.",
                    "Let me take your payment right now over the phone.",
                    "I'll note this on your account so you won't be disconnected.",
                ]
            }
        ]

        # Retention scenarios
        self.retention_scenarios = [
            {
                "opening": [
                    "Yeah, so I've been getting offers from other companies. They're cheaper.",
                    "I'm thinking about switching. Your competitor is offering way better rates.",
                    "I want to cancel. I found a better deal elsewhere.",
                    "I'm not happy with the service anymore. I'm looking at other options.",
                ],
                "agent_response": [
                    "I understand. Before you go, let me see what we can do to keep your business.",
                    "I hear you. Let me show you what specials we can offer existing customers.",
                    "I'd hate to see you go. Can I make you an offer that changes your mind?",
                ],
                "retention_offer": [
                    "How about if I gave you a discount for the next 6 months?",
                    "We can lower your rate to beat what they're offering you.",
                    "What if I upgraded your service at no extra cost?",
                    "We have a loyalty program I can enroll you in right now.",
                ],
                "customer_response": [
                    "How much of a discount are we talking about?",
                    "That might be worth reconsidering. What exactly are you offering?",
                    "I appreciate it, but I think I should still switch.",
                    "That's interesting. Tell me more about that.",
                ]
            }
        ]

        self.filler_words = ["um", "uh", "like", "you know", "I mean", "basically", "honestly", "right", "so"]
        self.interruptions = ["sorry", "hold on", "wait", "okay", "actually", "oh yeah"]

    def add_naturalism(self, text: str, intensity: float = 0.5) -> str:
        """Add natural speech patterns"""
        if random.random() < intensity * 0.3:
            filler = random.choice(self.filler_words)
            if random.random() > 0.5:
                return f"{filler}, {text.lower()}" if text[0].isupper() else f"{filler}, {text}"
            else:
                return f"{text}, {filler}"
        if random.random() < intensity * 0.2:
            # Add stutter or interruption
            words = text.split()
            if len(words) > 1:
                return f"{words[0]}... {text.lower()}"
        return text

    def calculate_duration(self, text: str) -> float:
        """Calculate speech duration from text"""
        words = len(text.split())
        base_duration = (words / 150) * 60
        variation = random.uniform(0.85, 1.15)
        return round(base_duration * variation, 1)

    def generate_support_call(self) -> Tuple[List[Dict], Dict]:
        """Generate a natural support call"""
        scenario = random.choice(self.support_scenarios)
        conversation = []
        current_time = 0.0

        agent_name = random.choice(self.agent_names)

        # IVR
        ivr_text = random.choice(self.ivr_intros)
        duration = self.calculate_duration(ivr_text)
        conversation.append({
            "speaker": "ivr",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": ivr_text
        })
        current_time += duration + random.uniform(1.0, 2.5)

        # Agent greeting
        agent_greeting = f"Hi, thanks for calling. This is {agent_name} with technical support. How can I help you today?"
        agent_greeting = self.add_naturalism(agent_greeting, 0.3)
        duration = self.calculate_duration(agent_greeting)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": agent_greeting
        })
        current_time += duration + random.uniform(0.8, 1.5)

        # Customer explains issue
        customer_opening = random.choice(scenario["customer_opening"])
        customer_opening = self.add_naturalism(customer_opening, 0.6)
        duration = self.calculate_duration(customer_opening)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": customer_opening
        })
        current_time += duration + random.uniform(0.5, 1.5)

        # Agent acknowledges
        agent_ack = random.choice(scenario["agent_approaches"])
        agent_ack = self.add_naturalism(agent_ack, 0.4)
        duration = self.calculate_duration(agent_ack)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": agent_ack
        })
        current_time += duration + random.uniform(1.0, 2.0)

        # Troubleshooting steps
        for step in range(random.randint(1, 2)):
            troubleshooting = random.choice(scenario["troubleshooting"])
            troubleshooting = self.add_naturalism(troubleshooting, 0.5)
            duration = self.calculate_duration(troubleshooting)
            conversation.append({
                "speaker": "agent",
                "start_time": current_time,
                "end_time": current_time + duration,
                "text": troubleshooting
            })
            current_time += duration + random.uniform(1.0, 2.5)

            # Customer response
            customer_responses = [
                "Okay, let me try that.",
                "Yeah, I'll do that now.",
                "Alright, it's restarting.",
                "Done. Now what?",
                "That didn't help.",
                "Still not working.",
            ]
            customer_resp = random.choice(customer_responses)
            customer_resp = self.add_naturalism(customer_resp, 0.4)
            duration = self.calculate_duration(customer_resp)
            conversation.append({
                "speaker": "caller",
                "start_time": current_time,
                "end_time": current_time + duration,
                "text": customer_resp
            })
            current_time += duration + random.uniform(0.5, 1.2)

        # Resolution
        resolution = random.choice(scenario["resolution"])
        resolution = self.add_naturalism(resolution, 0.3)
        duration = self.calculate_duration(resolution)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": resolution
        })
        current_time += duration + random.uniform(0.5, 1.0)

        # Closing
        agent_closing = random.choice([
            "Is there anything else I can help with?",
            "Does that help?",
            "You should be good to go now.",
            "Feel free to call back if you have issues.",
        ])
        duration = self.calculate_duration(agent_closing)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": agent_closing
        })
        current_time += duration + random.uniform(0.3, 1.0)

        customer_closing = random.choice([
            "Thanks for your help.",
            "Great, appreciate it.",
            "Thanks, that solved it.",
            "Okay, thanks.",
        ])
        customer_closing = self.add_naturalism(customer_closing, 0.4)
        duration = self.calculate_duration(customer_closing)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": customer_closing
        })
        current_time += duration

        metadata = {
            "call_type": "support",
            "agent_name": agent_name,
            "duration": current_time,
            "sentiment": random.choice(["positive", "neutral", "mixed"]),
            "issue_category": scenario["issue"],
            "issue_resolved": random.choice([True, False, "partial"]),
        }

        return conversation, metadata

    def generate_sales_call(self) -> Tuple[List[Dict], Dict]:
        """Generate a natural sales call"""
        scenario = self.sales_scenarios[0]
        conversation = []
        current_time = 0.0
        agent_name = random.choice(self.agent_names)

        # IVR
        ivr_text = "Thank you for calling Telecom Haiku sales team. Please hold while we connect you."
        duration = self.calculate_duration(ivr_text)
        conversation.append({
            "speaker": "ivr",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": ivr_text
        })
        current_time += duration + random.uniform(1.0, 2.5)

        # Agent greeting
        agent_greeting = f"Hi! Thanks for calling. This is {agent_name} with our sales team. What brings you in today?"
        duration = self.calculate_duration(agent_greeting)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": agent_greeting
        })
        current_time += duration + random.uniform(0.8, 1.5)

        # Customer opening
        opening = random.choice(scenario["opening"])
        opening = self.add_naturalism(opening, 0.5)
        duration = self.calculate_duration(opening)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": opening
        })
        current_time += duration + random.uniform(0.5, 1.5)

        # Agent pitch
        pitch = random.choice(scenario["agent_pitches"])
        pitch = self.add_naturalism(pitch, 0.3)
        duration = self.calculate_duration(pitch)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": pitch
        })
        current_time += duration + random.uniform(1.0, 2.0)

        # Customer question
        question = random.choice(scenario["customer_responses"])
        question = self.add_naturalism(question, 0.4)
        duration = self.calculate_duration(question)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": question
        })
        current_time += duration + random.uniform(0.5, 1.2)

        # Agent explains details
        details = random.choice([
            "You'd save about 20 dollars a month with this plan.",
            "The speeds are double what you're getting now.",
            "There's no contract, so you can cancel anytime.",
            "We'll waive the setup fee for new customers.",
        ])
        details = self.add_naturalism(details, 0.3)
        duration = self.calculate_duration(details)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": details
        })
        current_time += duration + random.uniform(0.8, 1.5)

        # Customer decision
        closing = random.choice(scenario["closing"])
        closing = self.add_naturalism(closing, 0.4)
        duration = self.calculate_duration(closing)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": closing
        })
        current_time += duration + random.uniform(0.5, 1.0)

        # Agent closing
        agent_close = random.choice([
            "Perfect! Let me get you signed up.",
            "Awesome, I'll start the process now.",
            "Great decision! I'll get that rolling.",
            "Thanks for considering us. I'll have that active soon.",
        ])
        duration = self.calculate_duration(agent_close)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": agent_close
        })
        current_time += duration

        product = random.choice(scenario["product_types"])
        metadata = {
            "call_type": "sales",
            "agent_name": agent_name,
            "duration": current_time,
            "sentiment": random.choice(["positive", "neutral"]),
            "product_category": product,
            "sale_completed": random.choice([True, False]),
        }

        return conversation, metadata

    def generate_billing_call(self) -> Tuple[List[Dict], Dict]:
        """Generate a natural billing call"""
        scenario = random.choice(self.billing_scenarios)
        conversation = []
        current_time = 0.0
        agent_name = random.choice(self.agent_names)

        # IVR
        ivr_text = "Welcome to Telecom Haiku billing. Your call is important to us."
        duration = self.calculate_duration(ivr_text)
        conversation.append({
            "speaker": "ivr",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": ivr_text
        })
        current_time += duration + random.uniform(1.0, 2.5)

        # Agent
        agent_greeting = f"Hi, this is {agent_name} from billing. What can I help you with?"
        duration = self.calculate_duration(agent_greeting)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": agent_greeting
        })
        current_time += duration + random.uniform(0.8, 1.5)

        # Customer issue
        issue = random.choice(scenario["opening"])
        issue = self.add_naturalism(issue, 0.6)
        duration = self.calculate_duration(issue)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": issue
        })
        current_time += duration + random.uniform(0.5, 1.5)

        # Agent investigates
        investigation = random.choice(scenario["investigation"])
        duration = self.calculate_duration(investigation)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": investigation
        })
        current_time += duration + random.uniform(1.5, 3.0)

        # Agent explains
        explanation = random.choice(scenario["explanation"])
        explanation = self.add_naturalism(explanation, 0.3)
        duration = self.calculate_duration(explanation)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": explanation
        })
        current_time += duration + random.uniform(0.8, 1.5)

        # Agent resolution
        resolution = random.choice(scenario["resolution"])
        duration = self.calculate_duration(resolution)
        conversation.append({
            "speaker": "agent",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": resolution
        })
        current_time += duration + random.uniform(0.5, 1.0)

        # Customer closing
        customer_close = random.choice([
            "Thanks for handling that.",
            "I appreciate you fixing it.",
            "Okay, thanks.",
            "That's all I needed.",
        ])
        duration = self.calculate_duration(customer_close)
        conversation.append({
            "speaker": "caller",
            "start_time": current_time,
            "end_time": current_time + duration,
            "text": customer_close
        })
        current_time += duration

        metadata = {
            "call_type": "billing",
            "agent_name": agent_name,
            "duration": current_time,
            "sentiment": random.choice(["positive", "neutral", "negative"]),
            "issue_category": scenario["issue"],
            "issue_resolved": random.choice([True, False]),
        }

        return conversation, metadata

    def generate_call(self, call_type: str) -> Tuple[List[Dict], Dict]:
        """Generate a call of specified type"""
        if call_type == "support":
            return self.generate_support_call()
        elif call_type == "sales":
            return self.generate_sales_call()
        elif call_type == "billing":
            return self.generate_billing_call()
        else:
            # Random other type
            return random.choice([
                self.generate_support_call(),
                self.generate_sales_call(),
                self.generate_billing_call()
            ])


def generate_all_calls(num_calls: int):
    """Generate all call transcripts"""
    generator = CallGenerator()
    index_data = []
    call_types = ["support", "sales", "billing", "technical", "account", "retention", "general"]

    print(f"Generating {num_calls} unique call transcripts...")

    for i in range(1, num_calls + 1):
        call_type = random.choice(call_types)
        conversation, metadata = generator.generate_call(call_type)

        # Save call
        filename = f"call_{i:06d}.json"
        filepath = OUTPUT_DIR / filename

        document = {
            "call_id": i,
            "metadata": metadata,
            "conversation": conversation
        }

        with open(filepath, 'w') as f:
            json.dump(document, f, indent=2)

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
            "issue_category": metadata.get("issue_category", "general"),
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
            print(f"  Generated {i}/{num_calls} transcripts...")

    # Write index
    print(f"Writing index to {INDEX_FILE}...")
    fieldnames = list(index_data[0].keys())
    with open(INDEX_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(index_data)

    print(f"\nDataset generation complete!")
    print(f"  Total calls: {num_calls}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Index file: {INDEX_FILE}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_all_calls(NUM_DOCUMENTS)
