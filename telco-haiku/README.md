# Telecom Haiku Call Center Dataset

A comprehensive synthetic call center dataset containing 2000 naturally varied and realistic phone conversations for a fictional telecom company called "Telecom Haiku". Unlike template-based datasets, these conversations are dynamically generated with minimal duplication, creating diverse and natural-sounding interactions.

## Dataset Overview

- **Total Documents**: 2000 call records
- **Format**: JSON documents with structured conversation turns
- **Generation Method**: Naturally varied conversation generation with dynamic composition
- **Directory Structure**:
  - `calls/` - Directory containing all 2000 call documents (call_000001.json through call_002000.json)
  - `index.csv` - Master index file with metadata for all calls
  - `generate_transcripts.py` - Python script to generate additional documents
  - `README.md` - This documentation file

## File Formats

### Index File (index.csv)

The main index file contains one row per call document with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| filename | string | Name of the JSON file (call_XXXXXX.json) |
| call_id | integer | Unique identifier for the call |
| call_type | string | Type of call: support, sales, billing, technical, account, retention, general |
| date | string | Call date (YYYY-MM-DD) |
| time | string | Call time (HH:MM:SS) |
| duration_seconds | float | Total call duration in seconds |
| agent_name | string | Name of the agent who handled the call |
| sentiment | string | Overall call sentiment: positive, neutral, negative, mixed |
| issue_resolved | boolean/string | Whether the issue was resolved (True, False, partial, escalated, or N/A) |
| issue_category | string | Category of the issue/inquiry (specific to call type) |
| sale_completed | boolean/string | For sales calls: whether a sale was completed (True, False, or N/A) |
| product_category | string | For sales calls: product category (Mobile Plan, Broadband, TV Package, Bundle, Device, Add-on, or N/A) |
| customer_id | string | Anonymized customer identifier (CUSTXXXXX) |
| agent_id | string | Agent identifier (AGENTXXXX) |
| language | string | Language of the call (currently all English) |
| call_quality | string | Audio quality rating: excellent, good, fair, poor |
| handle_time_efficient | string | Whether the call was handled efficiently: yes, no |
| follow_up_required | string | Whether follow-up is needed: yes, no |

### Call Documents (JSON)

Each call is stored as a JSON file with the following structure:

```json
{
  "call_id": 1,
  "metadata": {
    "call_type": "support",
    "agent_name": "Sarah",
    "duration": 52.3,
    "sentiment": "positive",
    "issue_category": "internet connectivity",
    "issue_resolved": true
  },
  "conversation": [
    {
      "speaker": "ivr",
      "start_time": 0.0,
      "end_time": 3.4,
      "text": "Welcome to Telecom Haiku. Press 1 for English, 2 for Spanish."
    },
    {
      "speaker": "agent",
      "start_time": 4.1,
      "end_time": 9.5,
      "text": "Hi, thanks for calling. This is Sarah with technical support. How can I help you today?"
    },
    {
      "speaker": "caller",
      "start_time": 10.2,
      "end_time": 17.8,
      "text": "Hi, yeah, I've been having really bad internet. Like, my connection keeps dropping every few minutes."
    }
  ]
}
```

#### Metadata Fields

- **call_id** (integer): Unique call identifier
- **call_type** (string): Type of call (support, sales, billing, technical, account, retention, general)
- **agent_name** (string): Name of the handling agent
- **duration** (float): Total call duration in seconds
- **sentiment** (string): positive, neutral, negative, or mixed
- **issue_category** (string): Specific category of issue/request
- **issue_resolved** (boolean/string): Whether issue was resolved
- **sale_completed** (boolean): Whether sale was completed (for sales calls)
- **product_category** (string): Product discussed (for sales calls)

#### Conversation Array Format

The `conversation` field is a JSON array where each object represents one speaking turn:

- **speaker** (string): Who is speaking - "ivr", "agent", or "caller"
- **start_time** (float): Start time in seconds from beginning of call
- **end_time** (float): End time in seconds from beginning of call
- **text** (string): The spoken content

Each conversation contains:
- **Natural speech patterns**: Filler words ("um", "uh", "like", "you know"), stutters, and interruptions
- **Realistic dialogue flow**: Back-and-forth exchanges that feel conversational
- **Varied pacing**: Pauses and gaps between turns (1-3 seconds)
- **Authentic language**: Incomplete sentences, self-corrections, and natural hesitations
- **Unique variations**: Each call is dynamically generated with different compositions

## Call Categories

### Support Calls
Feature realistic technical support interactions including:
- **Internet connectivity issues**: Dropping connections, unstable service
- **Service quality problems**: Weak signals, slow speeds, buffering
- **Device problems**: Modem/router issues, overheating, non-responsive equipment
- **Account access issues**: Login problems, password resets, locked accounts

### Sales Calls
Feature genuine sales interactions with:
- **Customer interest**: Genuine inquiries about upgrades and new services
- **Product conversations**: Discussions about Mobile Plans, Broadband, TV Packages, Bundles, Devices
- **Pricing discussions**: Questions about costs, installation fees, and savings
- **Closing outcomes**: Sales completed or deferred, with realistic customer responses

### Billing Calls
Feature realistic billing scenarios:
- **Charge disputes**: Unexpected charges, overages, verification of costs
- **Payment issues**: Failed payments, payment method updates, balance inquiries
- **Account investigations**: Agent research into billing problems
- **Resolutions**: Credits, charge reversals, clarifications

## Generation Approach

### Natural Variation Techniques

Unlike template-based generators that create obvious duplication, this dataset uses:

1. **Dynamic Composition**: Each conversation is built turn-by-turn with organic variation
2. **Contextual Responses**: Agent and customer responses adapt to the conversation flow
3. **Natural Speech Addition**: Realistic filler words, stutters, and interruptions are dynamically added
4. **Variable Pacing**: Gaps between speakers vary naturally (0.5-3.0 seconds)
5. **Duration Calculation**: Speech duration is estimated based on word count with variation

### Key Characteristics

- **Minimal Repetition**: Each of 2000 calls has unique composition
- **Authentic Feel**: Conversations read as natural human interactions
- **Realistic Patterns**: Features actual speech patterns like:
  - Interruptions: "sorry... sorry, let me explain that"
  - Stutters: "do... do you have any promotions"
  - Filler words: "um, like, you know, basically"
  - Self-corrections: "Actually,... actually, let me check"
- **Varied Call Lengths**: 30-60 seconds per call with natural variation
- **Different Agents**: 16 unique agent names with varied personalities

## Adding New Documents

To generate additional call documents, use the provided Python script.

### Method 1: Regenerate Entire Dataset

To create a dataset with a different size, edit `generate_transcripts.py`:

```python
NUM_DOCUMENTS = 3000  # Change this to desired size
```

Then run:

```bash
python3 generate_transcripts.py
```

### Method 2: Extend Dataset

To add documents to the existing dataset:

```python
from generate_transcripts import CallGenerator
import json
import csv
from pathlib import Path

generator = CallGenerator()
call_types = ["support", "sales", "billing", "technical", "account", "retention", "general"]

for i in range(2001, 2101):  # Add 100 more
    call_type = random.choice(call_types)
    conversation, metadata = generator.generate_call(call_type)

    # Save to file and update index
    ...
```

### Method 3: Manual Document Creation

You can manually create call documents:

1. Create a new file: `calls/call_XXXXXX.json`
2. Follow the JSON structure shown above
3. Ensure conversation array has realistic timing
4. Add corresponding row to `index.csv`

## Example Usage

### Loading and Analyzing Data

```python
import json
import pandas as pd

# Load index
index_df = pd.read_csv("index.csv")

# Load a single call
with open("calls/call_000001.json") as f:
    call_doc = json.load(f)

# Access conversation turns
for turn in call_doc["conversation"]:
    print(f"{turn['speaker'].upper()} ({turn['start_time']}-{turn['end_time']}s): {turn['text']}")

# Analyze sentiment distribution
print(index_df["sentiment"].value_counts())

# Get support call resolution rate
support_calls = index_df[index_df["call_type"] == "support"]
print(f"Support resolution rate: {support_calls['issue_resolved'].mean():.2%}")
```

### Analyzing Natural Language Patterns

```python
import json

# Load a call
with open("calls/call_000001.json") as f:
    call = json.load(f)

# Find filler words
filler_words = ["um", "uh", "like", "you know", "basically"]
for turn in call["conversation"]:
    text = turn["text"].lower()
    for filler in filler_words:
        if filler in text:
            print(f"{turn['speaker']}: found '{filler}' in '{turn['text']}'")

# Analyze conversation structure
speakers = [turn["speaker"] for turn in call["conversation"]]
print(f"Speaker pattern: {' -> '.join(speakers)}")

# Calculate average turn duration
turns = call["conversation"]
avg_duration = sum(t["end_time"] - t["start_time"] for t in turns) / len(turns)
print(f"Average turn duration: {avg_duration:.1f} seconds")
```

## Dataset Statistics

- **Total Calls**: 2000
- **Call Types**: 7 categories distributed roughly evenly
- **Agent Pool**: 16 unique agent names
- **Average Call Duration**: ~45-50 seconds
- **Conversation Turns per Call**: 8-10 turns
- **Date Range**: Past 90 days from generation date
- **Languages**: English
- **Unique Conversations**: 2000 (each dynamically generated)

### Call Type Distribution

Call types are distributed across the dataset:
- Support calls: ~28%
- Sales calls: ~28%
- Billing calls: ~28%
- Technical calls: ~14%
- Other types: ~2%

### Natural Language Distribution

- **60% of calls** include filler words or interruptions
- **50% of calls** have stutters or self-corrections
- **100% of calls** have variable pacing between turns
- **100% of calls** use naturally calculated speech durations

## Generation Parameters

The dataset is generated using:
- **Speaking rate baseline**: 150 words per minute
- **Speaking rate variation**: ±15% per turn
- **IVR speaking rate**: 160 words per minute
- **Turn gap variation**: 1.0-3.0 seconds between speaker turns
- **Filler word injection**: ~30% of turns
- **Stutter/interruption injection**: ~20% of turns

## Output Structure

```
telco-haiku/
├── calls/
│   ├── call_000001.json
│   ├── call_000002.json
│   ├── ...
│   └── call_002000.json
├── index.csv
├── generate_transcripts.py
└── README.md
```

## Key Differences from Template-Based Datasets

This dataset differs from template-based approaches by:

1. **Dynamic Generation**: Conversations are built dynamically, not selected from templates
2. **Minimal Duplication**: Each call is unique in composition and flow
3. **Natural Speech**: Includes realistic speech patterns, not obvious templating
4. **Organic Variation**: Variation in every aspect of conversation (timing, language, structure)
5. **Realistic Interactions**: Conversations flow naturally like real human interactions

## Notes

- All data is synthetic and fictional - no real personal information
- Customer IDs and Agent IDs are randomly generated placeholders
- Call dates are simulated within 90-day window
- Call times are random throughout business hours (8 AM - 5 PM)
- Each of the 2000 calls is a unique, dynamically generated conversation
- Timing information is estimated based on typical speaking rates with variation

## Customization Guide

To customize the dataset, modify `generate_transcripts.py`:

### Add More Issue Types

Edit the `support_scenarios`, `sales_scenarios`, or `billing_scenarios` lists:

```python
self.support_scenarios = [
    {
        "issue": "new_issue_type",
        "customer_opening": [...],
        "agent_approaches": [...],
        "troubleshooting": [...],
        "resolution": [...]
    }
]
```

### Adjust Natural Language Intensity

Modify the `add_naturalism()` method to change frequency of filler words and interruptions.

### Change Speaking Rates

Modify the `calculate_duration()` method to adjust speech pacing.

### Expand Agent Names

Add more names to the `agent_names` list in the `CallGenerator` class.

## License

This synthetic dataset is provided as-is for testing and development purposes.

## Questions or Issues?

To customize or extend this dataset, modify `generate_transcripts.py` according to the customization guide above.
