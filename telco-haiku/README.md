# Telecom Haiku Call Center Dataset

A comprehensive synthetic call center dataset containing 2000 realistic phone conversations for a fictional telecom company called "Telecom Haiku".

## Dataset Overview

- **Total Documents**: 2000 call records
- **Format**: JSON documents with embedded CSV conversation transcripts
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
| sentiment | string | Overall call sentiment: positive, neutral, negative |
| issue_resolved | boolean/string | Whether the issue was resolved (True, False, or N/A) |
| issue_category | string | Category of the issue/inquiry |
| sale_completed | boolean/string | For sales calls: whether a sale was completed (True, False, or N/A) |
| product_category | string | For sales calls: product category (Mobile Plan, Broadband, TV Package, Bundles, Device, Add-on Service, or N/A) |
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
    "issue": "internet is down",
    "issue_resolved": true,
    "resolution_type": "resolved"
  },
  "conversation_csv": "speaker,start_time,end_time,text\r\nivr,0.0,3.4,\"Welcome to Telecom Haiku...\"\r\nagent,4.1,9.5,\"Hi there! This is Sarah from Technical Support. How can I help you today?\"\r\n..."
}
```

#### Metadata Fields

- **call_id** (integer): Unique call identifier
- **call_type** (string): Type of call (support, sales, billing, technical, account, retention, general)
- **agent_name** (string): Name of the handling agent
- **duration** (float): Total call duration in seconds
- **sentiment** (string): positive, neutral, or negative
- **issue** (string): Description of the main issue/request
- **issue_resolved** (boolean): Whether issue was resolved (for support/technical calls)
- **sale_completed** (boolean): Whether sale was completed (for sales calls)
- **product_category** (string): Product discussed (for sales calls)
- **resolution_type** (string): How the issue was resolved (resolved, escalated, scheduled followup, partial resolution, callback needed)

#### Conversation CSV Format

The `conversation_csv` field contains a CSV with the actual call transcript. Each row represents one speaking turn with:

- **speaker** (string): Who is speaking - "ivr", "agent", or "caller"
- **start_time** (float): Start time in seconds from beginning of call
- **end_time** (float): End time in seconds from beginning of call
- **text** (string): The spoken content

The conversation typically follows this pattern:
1. IVR greeting/menu system
2. Agent greeting (varies by call type)
3. Customer explanation of issue
4. Agent acknowledgment and troubleshooting/discussion
5. Resolution or follow-up
6. Closing statements

### Issue Categories

The dataset includes calls across 10+ issue categories:

- **connectivity** - Internet/network connection issues
- **billing** - Payment, charges, and account billing
- **device** - Device-related problems (modem, router, phone)
- **account** - Account management and access
- **service_quality** - Service performance and quality
- **technical_support** - Technical troubleshooting
- **sales_inquiry** - Product inquiry and sales discussions
- **retention** - Customer retention and churn prevention
- **complaint** - Customer complaints about service
- **inquiry** - General inquiries and information requests

## Adding New Documents

To generate additional call documents, you can use the provided Python script.

### Method 1: Generate Additional Documents

Edit `generate_dataset.py` and change the `NUM_DOCUMENTS` variable, then run:

```bash
python3 generate_dataset.py
```

**Note**: This will regenerate all documents from scratch using the same random seed.

### Method 2: Extend Dataset with New Documents

To add documents to the existing dataset without regenerating all documents, create a Python script:

```python
import json
import csv
import random
import datetime
from pathlib import Path

def generate_single_call(call_id):
    """Generate a single call document - use logic from generate_dataset.py"""
    # Implementation details from generate_dataset.py
    conversation, metadata = generate_conversation(call_type)
    return save_call_as_json(call_id, conversation, metadata)

def append_to_index(filename, metadata):
    """Append new row to index.csv"""
    index_file = Path("index.csv")
    with open(index_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[...])
        writer.writerow({...})

# Generate new documents starting from ID 2001
for i in range(2001, 2101):  # Add 100 more documents
    filename = generate_single_call(i)
    append_to_index(filename, metadata)
```

### Method 3: Manual Document Creation

You can manually create call documents by following the JSON structure:

1. Create a new file: `calls/call_XXXXXX.json`
2. Follow the JSON structure shown above
3. Ensure the conversation CSV is properly formatted
4. Add a corresponding row to `index.csv`

## Data Generation Details

### Timing Calculation

Speech durations are estimated using the following formula:

```
duration = (word_count / 2.5) * variation_factor
```

Where:
- Word count is based on the text content
- 2.5 words per second is the average speaking rate (150 words per minute)
- Variation factor: 0.9-1.1 (±10%) to add natural variation
- Results are rounded to 1 decimal place

### Call Types and Characteristics

**Support Calls** (~14% of calls):
- Typical duration: 40-60 seconds
- Issues: connectivity, device, general troubleshooting
- Primary outcome: issue_resolved (True/False)

**Sales Calls** (~14% of calls):
- Typical duration: 45-70 seconds
- Focus: product offerings and upgrades
- Primary outcome: sale_completed (True/False)

**Billing Calls** (~14% of calls):
- Typical duration: 35-55 seconds
- Issues: charges, payments, disputes
- Metadata: billing-related resolution_type

**Technical Calls** (~14% of calls):
- Typical duration: 40-65 seconds
- Issues: modem, router, device configuration
- Metadata: technical resolution approach

**Account Calls** (~14% of calls):
- Typical duration: 35-50 seconds
- Issues: access, password, account changes
- Metadata: account management outcomes

**Retention Calls** (~14% of calls):
- Typical duration: 40-60 seconds
- Issues: customer churn, competitor offers
- Metadata: retention success metrics

**General Calls** (~14% of calls):
- Typical duration: 35-55 seconds
- Issues: various miscellaneous inquiries
- Metadata: general outcomes

### Conversation Patterns

All conversations follow realistic patterns with:
- **IVR Introduction**: 1-3 seconds of automated system
- **Agent Greeting**: Contextual greeting based on call type
- **Customer Issue**: Description of the problem/inquiry (with natural interruptions like "um", "uh", "well")
- **Troubleshooting/Discussion**: Agent asks questions and provides solutions
- **Resolution**: Solutions offered or escalation explained
- **Closing**: Professional closing remarks
- **Natural Gaps**: Realistic pauses between speaker turns (0.3-2.0 seconds)

### Additional Classification Labels (17 total)

1. **call_type** - Type of call (7 categories)
2. **sentiment** - positive, neutral, negative
3. **issue_resolved** - True/False (for support/technical)
4. **sale_completed** - True/False (for sales)
5. **issue_category** - Category of issue (10+ categories)
6. **product_category** - Product type (for sales calls)
7. **call_quality** - Audio quality rating
8. **handle_time_efficient** - Efficiency assessment
9. **follow_up_required** - Whether follow-up is needed
10. **agent_name** - Agent identifier
11. **customer_id** - Customer identifier
12. **language** - Language of call
13. **duration_seconds** - Call length
14. **date** - Call date
15. **time** - Call time
16. **resolution_type** - How resolution was achieved
17. **agent_id** - Agent identifier

Plus metadata fields in individual documents like agent_name, duration, and issue description.

## Example Usage

### Loading and Parsing Data

```python
import json
import csv
import io
import pandas as pd

# Load index
index_df = pd.read_csv("index.csv")

# Load a single call
with open("calls/call_000001.json") as f:
    call_doc = json.load(f)

# Parse conversation CSV
csv_data = io.StringIO(call_doc["conversation_csv"])
conversation_df = pd.read_csv(csv_data)

print(call_doc["metadata"])
print(conversation_df)
```

### Analyzing the Dataset

```python
import pandas as pd

index_df = pd.read_csv("index.csv")

# Call type distribution
print(index_df["call_type"].value_counts())

# Average duration by call type
print(index_df.groupby("call_type")["duration_seconds"].mean())

# Sales success rate
sales_calls = index_df[index_df["call_type"] == "sales"]
print(f"Sales completion rate: {sales_calls['sale_completed'].mean():.2%}")

# Support resolution rate
support_calls = index_df[index_df["call_type"] == "support"]
print(f"Support resolution rate: {support_calls['issue_resolved'].mean():.2%}")
```

## Dataset Statistics

- **Total Calls**: 2000
- **Call Types**: 7 distinct types
- **Average Call Duration**: ~45 seconds
- **Agents in Dataset**: 8 unique names
- **Date Range**: Past 90 days from generation date
- **Languages**: English
- **Sentiment Distribution**: Mixed positive, neutral, negative

## Notes

- All data is synthetic and fictional - no real personal information is included
- Customer IDs and Agent IDs are randomly generated placeholders
- Call dates are simulated within a 90-day window
- Call times are random throughout business hours (8 AM - 5 PM)
- Conversation text includes realistic patterns like interruptions, partial phrases, and thinking phrases ("um", "uh", "yeah")
- Timing information is estimated based on typical speaking rates

## License

This synthetic dataset is provided as-is for testing and development purposes.

## Questions or Issues?

To customize this dataset:
1. Modify `generate_dataset.py` for different conversation patterns
2. Adjust `ISSUES`, `AGENT_PHRASES`, or `CUSTOMER_PHRASES` dictionaries
3. Change `NUM_DOCUMENTS` to generate different dataset sizes
4. Modify metadata fields to add additional classification categories
