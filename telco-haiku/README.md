# Telecom Haiku Call Center Dataset

A comprehensive synthetic call center dataset containing 2000 highly varied and realistic phone conversations for a fictional telecom company called "Telecom Haiku".

## Dataset Overview

- **Total Documents**: 2000 call records
- **Format**: JSON documents with structured conversation turns
- **Directory Structure**:
  - `calls/` - Directory containing all 2000 call documents (call_000001.json through call_002000.json)
  - `index.csv` - Master index file with metadata for all calls
  - `generate_dataset.py` - Python script to generate additional documents
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
| issue_category | string | Category of the issue/inquiry (support subcategories, billing type, etc.) |
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
    "duration": 42.3,
    "sentiment": "positive",
    "issue_category": "connectivity",
    "issue_resolved": true,
    "resolution_type": "the issue was resolved"
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
      "text": "Hi, thanks for calling. This is Sarah from technical support."
    },
    {
      "speaker": "caller",
      "start_time": 10.2,
      "end_time": 13.8,
      "text": "Yeah, uh, my internet keeps dropping, like"
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
- **issue_resolved** (boolean/string): Whether issue was resolved (varies by call type)
- **sale_completed** (boolean): Whether sale was completed (for sales calls)
- **product_category** (string): Product discussed (for sales calls)
- **resolution_type** (string): Description of how the issue was resolved
- **billing_issue** (string): Type of billing issue (dispute, payment, promotion)
- **technical_issue** (string): Type of technical issue (setup, troubleshooting, device_issue)
- **churn_reason** (string): Reason for potential churn (competitor, service_complaint, leaving)
- **inquiry_type** (string): Type of sales inquiry (upgrade, new_service, device, information)

#### Conversation Array Format

The `conversation` field is a JSON array where each object represents one speaking turn:

- **speaker** (string): Who is speaking - "ivr", "agent", or "caller"
- **start_time** (float): Start time in seconds from beginning of call
- **end_time** (float): End time in seconds from beginning of call
- **text** (string): The spoken content

Each turn contains realistic speech patterns including:
- **Filler words**: "um", "uh", "like", "you know", "well", "so", "actually", "basically"
- **Interruptions**: "sorry...", "hold on...", "wait...", with partial phrases
- **Stutters and repetition**: "can... can you", "let me... let me check"
- **Natural pauses**: Variable gaps between speaker turns (0.5-3.0 seconds)
- **Realistic responses**: Questions, affirmations, concerns, and clarifications

### Issue Categories and Subcategories

The dataset includes diverse call scenarios across multiple dimensions:

**Support Issues** (connectivity, speed, device, service, billing_issue, account_access):
- Connectivity problems (dropping connections, unstable service)
- Speed issues (slow loading, buffering, poor speeds)
- Device problems (modem issues, router resets)
- Service quality (dead zones, patchy coverage)
- Billing discrepancies reported during support calls
- Account access problems (login, password issues)

**Sales Inquiries** (upgrade, new_service, device, information):
- Service upgrades and plan changes
- Adding new services (TV, bundles, additional lines)
- Device purchases and payment plans
- General information requests

**Billing Issues** (dispute, payment, promotion):
- Charge disputes and overcharges
- Payment and balance inquiries
- Promotional offers and discounts

**Technical Issues** (setup, troubleshooting, device_issue):
- Initial setup and configuration
- Troubleshooting non-functional equipment
- Device-specific problems

**Retention/Churn Issues** (competitor, service_complaint, leaving):
- Competitor offers received by customer
- Service quality complaints
- Formal cancellation requests

**Account Management**:
- General account questions
- Profile updates
- Service modifications

## Data Generation Approach

The enhanced generator creates highly varied conversations through:

### Dynamic Issue Selection
Each call type has multiple issue subcategories with 4-5 variants per category, resulting in hundreds of possible issue combinations rather than a fixed set.

### Natural Speech Patterns
- Random insertion of filler words (40% of turns)
- Interruption and stutter effects (30% of turns)
- Variable speaking rates (±15% variation)
- Realistic pauses between speaker turns (0.5-3.0 seconds)

### Context-Aware Generation
- Agent greetings vary by call type and agent personality
- Customer responses reflect their emotional state and issue type
- Problem-solving exchanges adapt to the specific issue
- Resolution types match the call type and conversation flow

### Conversation Flow
All conversations follow realistic patterns:
1. **IVR greeting** (1-3 seconds) - Automated system with 5 different variants
2. **Agent introduction** (4-9 seconds) - Call-type specific greeting
3. **Customer explanation** (5-15 seconds) - Issue or request description
4. **Agent investigation** (varies) - For support/billing/account calls
5. **Problem-solving** (multiple exchanges) - Back-and-forth discussion
6. **Additional issues** (50% of calls) - Customer brings up another matter
7. **Closing** (3-6 seconds) - Professional conclusion

### Outcome Variation
Outcomes vary based on call type:
- **Support calls**: issue_resolved (True, False, partial, escalated)
- **Sales calls**: sale_completed (True, False) with product categories
- **Billing calls**: issue_resolved (True, False)
- **Technical calls**: issue_resolved (True, False, escalated)

## Adding New Documents

To generate additional call documents, use the provided Python script.

### Method 1: Regenerate Entire Dataset

To create a dataset with a different size, edit `generate_dataset.py`:

```python
NUM_DOCUMENTS = 3000  # Change this to desired size
```

Then run:

```bash
python3 generate_dataset.py
```

This will regenerate all documents from scratch using the same random seed for reproducibility.

### Method 2: Extend Dataset with New Documents

To add documents to the existing dataset without regenerating all documents, create a Python script:

```python
import json
import csv
import random
from pathlib import Path
from generate_dataset import generate_dynamic_conversation, save_call_as_json
import datetime

# Get the highest call ID
with open('index.csv', 'r') as f:
    last_id = int(f.readlines()[-1].split(',')[1])

# Generate new documents
for i in range(last_id + 1, last_id + 101):  # Add 100 more documents
    call_type = random.choice(["support", "sales", "billing", "technical", "account", "retention", "general"])
    conversation, metadata = generate_dynamic_conversation(call_type)
    filename = save_call_as_json(i, conversation, metadata)

    # Append to index
    call_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 90))
    call_time = f"{random.randint(8, 17):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"

    index_row = {
        "filename": filename,
        "call_id": i,
        "call_type": call_type,
        # ... populate other fields
    }

    with open('index.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[...])
        writer.writerow(index_row)
```

### Method 3: Manual Document Creation

You can manually create call documents:

1. Create a new file: `calls/call_XXXXXX.json`
2. Follow the JSON structure shown above
3. Ensure the conversation array has proper timing information
4. Add a corresponding row to `index.csv`

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

# Get support call statistics
support_calls = index_df[index_df["call_type"] == "support"]
print(f"Support call resolution rate: {support_calls['issue_resolved'].mean():.2%}")

# Find all sales calls that resulted in purchases
sales = index_df[index_df["call_type"] == "sales"]
completed = sales[sales["sale_completed"] == True]
print(f"Sales success rate: {len(completed) / len(sales):.2%}")
```

### Working with Conversations

```python
import json
import statistics

# Load a call
with open("calls/call_000001.json") as f:
    call = json.load(f)

# Calculate average turn duration
turns = call["conversation"]
durations = [turn["end_time"] - turn["start_time"] for turn in turns]
print(f"Average turn duration: {statistics.mean(durations):.1f} seconds")

# Count turns by speaker
speaker_counts = {}
for turn in turns:
    speaker = turn["speaker"]
    speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1

print(f"Speaker distribution: {speaker_counts}")

# Extract agent dialogue
agent_lines = [turn["text"] for turn in turns if turn["speaker"] == "agent"]
print("\nAgent speaking turns:")
for i, line in enumerate(agent_lines, 1):
    print(f"  {i}. {line}")
```

## Dataset Statistics

- **Total Calls**: 2000
- **Call Types**: 7 distinct types (support, sales, billing, technical, account, retention, general)
- **Agent Pool**: 14 unique agent names
- **Average Call Duration**: ~50 seconds (range: 30-90 seconds)
- **Conversation Turns per Call**: 10-20 turns
- **Date Range**: Past 90 days from generation date
- **Languages**: English
- **Sentiment Distribution**: Mixed positive, neutral, negative, mixed

### Call Type Distribution
Each call type appears with roughly equal frequency (~285 calls per type), ensuring balanced representation.

### Speech Pattern Distribution
- 40% of turns include filler words
- 30% of turns include interruptions or stutters
- 50% of calls include additional follow-up issues
- Speaking rate varies ±15% from standard 150 words/minute

## Generation Parameters

The dataset is generated using:
- **Random seed**: 42 (for reproducibility)
- **Speaking rate baseline**: 150 words per minute (≈ 2.5 words/second)
- **Speaking rate variation**: ±15% per turn
- **IVR speaking rate**: 160 words per minute (slightly faster)
- **Turn gap variation**: 0.3-3.0 seconds between speaker turns

## Output Structure

```
telco-haiku/
├── calls/
│   ├── call_000001.json
│   ├── call_000002.json
│   ├── ...
│   └── call_002000.json
├── index.csv
├── generate_dataset.py
└── README.md
```

## Notes

- All data is synthetic and fictional - no real personal information
- Customer IDs and Agent IDs are randomly generated placeholders
- Phone numbers are randomized (e.g., 555-XXXX)
- Call dates are simulated within 90-day window
- Call times are random throughout business hours (8 AM - 5 PM)
- Conversation text includes realistic patterns like interruptions, partial phrases, and filler words
- Timing information is estimated based on typical speaking rates
- Each call is unique due to dynamic generation (not templated)

## Customization Guide

To customize the dataset, modify `generate_dataset.py`:

### Add More Issue Types
Edit the `SUPPORT_ISSUES`, `SALES_QUERIES`, `BILLING_ISSUES`, `TECHNICAL_ISSUES`, or `RETENTION_ISSUES` dictionaries:

```python
SUPPORT_ISSUES = {
    "new_category": [
        "issue variant 1",
        "issue variant 2",
        # Add more variants
    ],
    # ... other categories
}
```

### Add More Filler Words
Edit the `FILLERS` list:

```python
FILLERS = ["um", "uh", "like", "you know", "well", "so", "actually", "basically", "kinda", "sorta",
           "I mean", "you see", "right", "okay"]
```

### Adjust Speaking Rates
Modify the `speaking_rate` parameter in `calculate_speech_duration()`:

```python
def calculate_speech_duration(text: str, speaking_rate: float = 140) -> float:
    # Lower rates = longer durations
    # Higher rates = shorter durations
    ...
```

### Change Conversation Depth
Modify the problem-solving exchange range:

```python
for exchange in range(random.randint(2, 5)):  # More exchanges = longer calls
    ...
```

## License

This synthetic dataset is provided as-is for testing and development purposes.

## Questions or Issues?

To customize or extend this dataset, modify `generate_dataset.py` according to the customization guide above. The generation is fully parameterized for flexibility.
