import boto3
import random
import time
import uuid
from datetime import datetime
import os

# === Configuration ===
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
TABLE_NAME = "users"
INSERT_INTERVAL_MS = 500  # Insert every 500 milliseconds

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=REGION_NAME)

# === Helper Functions ===
def random_string(length=8):
    """Generate a random string."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(length))

def random_bool():
    """Generate a random boolean."""
    return random.choice([True, False])

def random_date(start_year=1980, end_year=2000):
    """Generate a random birthdate between two years."""
    return f"{random.randint(start_year, end_year)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

def random_user_type():
    """Randomly select a user type."""
    return random.choice(["User", "Advertiser", "Admin"])

def random_pronouns():
    """Generate random pronouns."""
    return [
        {"M": {"pronoun": {"S": "he"}, "order": {"N": "0"}}},
        {"M": {"pronoun": {"S": "him"}, "order": {"N": "1"}}},
        {"M": {"pronoun": {"S": "his"}, "order": {"N": "2"}}}
    ]

def random_notifications():
    """Generate random notifications."""
    return [
        {"S": "Follows"}, {"S": "Comments"}, {"S": "Quotes"}, {"S": "Likes"},
        {"S": "Mentions"}, {"S": "TeaPartyReply"}, {"S": "TeaPartyInvites"},
        {"S": "SpadeGameInvites"}, {"S": "GameReply"}
    ]

def random_content():
    """Generate random content settings."""
    return {"mode": {"S": "Dark"}, "colorway": {"S": random.choice(["LavenderFlower", "SkyBlue", "Midnight"])}}

def random_accessibility():
    """Generate random accessibility settings."""
    return {"stackSwipeDirection": {"S": random.choice(["right", "left"])}}

def random_member_tour():
    """Generate random member tour data."""
    return {
        "explore": {"N": str(random.randint(0, 10))},
        "teaPartyLobby": {"N": str(random.randint(0, 10))},
        "compose": {"N": str(random.randint(0, 10))},
        "teaPartyLive": {"N": str(random.randint(0, 10))},
        "profile": {"N": str(random.randint(0, 10))},
        "appIntro": {"N": str(random.randint(0, 10))},
        "details": {"N": str(random.randint(0, 10))},
        "teaPartyVideo": {"N": str(random.randint(0, 10))},
        "welcome": {"S": "accepted"}
    }

def random_brew():
    """Generate random interests (brew field)."""
    return [{"S": random.choice(["pop_culture", "food", "movies_tv", "sports"])} for _ in range(4)]

def create_random_record():
    """Create a random user record with all fields."""
    record = {
        "id": {"S": str(uuid.uuid4())},
        "accessibility": {"M": random_accessibility()},
        "allowCodes": {"BOOL": random_bool()},
        "appearance": {"M": random_content()},
        "bio": {"S": random_string(20)},
        "birthdate": {"S": random_date()},
        "brew": {"L": random_brew()},
        "contentSetting": {"S": ""},
        "country": {"S": ""},
        "createdAt": {"S": datetime.utcnow().isoformat() + 'Z'},
        "email": {"S": f"{random_string(5)}@example.com"},
        "ethnicity": {"S": random.choice(["black/african descent", "white", "hispanic", "asian"])},
        "followers": {"N": str(random.randint(0, 100))},
        "followersCount": {"N": str(random.randint(0, 100))},
        "following": {"N": str(random.randint(0, 100))},
        "followingCount": {"N": str(random.randint(0, 100))},
        "gender": {"S": ""},
        "handle": {"S": random_string(10)},
        "imageUrl": {"S": f"https://example.com/{uuid.uuid4()}/image.jpg"},
        "lastUpdated": {"S": ""},
        "likesCount": {"N": str(random.randint(0, 100))},
        "location": {"S": random.choice(["The TVA", "The Citadel", "Metropolis"])},
        "memberTour": {"M": random_member_tour()},
        "name": {"S": f"{random_string(6)} {random_string(6)}"},
        "notifications": {"L": random_notifications()},
        "onboardingStep": {"S": "completed"},
        "phone": {"S": f"+639{random.randint(1000000000, 9999999999)}"},
        "phoneOptOut": {"BOOL": random_bool()},
        "pronouns": {"L": random_pronouns()},
        "repScore": {"N": str(random.randint(0, 10))},
        "spillCount": {"N": str(random.randint(0, 500))},
        "tos": {"S": "accepted"},
        "userType": {"S": random_user_type()},
        "website": {"S": f"https://tdy.lol/{random_string(6)}"},
        "zipCode": {"S": f"{random.randint(10000, 99999)}"}
    }
    return record

def insert_record(record):
    """Insert a single record into DynamoDB."""
    dynamodb.put_item(TableName=TABLE_NAME, Item=record)
    print(f"Inserted record with ID: {record['id']['S']}")

# === Main Execution Loop ===
if __name__ == "__main__":
    print(f"Starting DynamoDB record insertion every {INSERT_INTERVAL_MS} milliseconds...")

    while True:
        # Create a random record
        random_record = create_random_record()

        # Insert the record into DynamoDB
        insert_record(random_record)

        # Wait for the specified interval
        time.sleep(INSERT_INTERVAL_MS / 1000.0)