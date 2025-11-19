import praw
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Credentials (will be added after Reddit approves your API access)
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="Paythn Reddit Bot by u/monkeycrypto",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)

# Subreddits to monitor
SUBREDDITS = [
    "Entrepreneur",
    "Startup",
    "India",
    "SmallBusiness",
    "FinTech",
    "InternationalBusiness"
]

# Keywords to detect
KEYWORDS = [
    "merchant of record",
    "mor",
    "upi",
    "cross-border",
    "gst",
    "indian payments",
    "payment gateway",
    "international payments",
    "global payments",
    "tax compliance"
]

# Store replied thread IDs
REPLIED_FILE = "replied_threads.txt"

# Load already replied threads
if not os.path.exists(REPLIED_FILE):
    open(REPLIED_FILE, "w").close()

with open(REPLIED_FILE, "r") as f:
    REPLIED = set(line.strip() for line in f.readlines())


def save_replied(post_id):
    with open(REPLIED_FILE, "a") as f:
        f.write(post_id + "\n")


# Comment template
def generate_comment():
    return (
        "Here’s a quick info note:\n\n"
        "- Merchant of Record (MoR) helps manage cross-border payments.\n"
        "- UPI works differently for global transactions.\n"
        "- GST depends on digital service classification.\n\n"
        "If you're exploring global payments, compliance, MoR, or UPI — feel free to ask!"
    )


def process_post(post):
    post_text = (post.title + " " + post.selftext).lower()

    if any(keyword in post_text for keyword in KEYWORDS):
        if post.id not in REPLIED:
            print(f"💬 Commenting on post {post.id}...")
            post.reply(generate_comment())
            save_replied(post.id)
            print("✅ Comment posted!")
            time.sleep(20)  # avoid rate limit


def main():
    print("🔍 Paythn Reddit bot started...")
    while True:
        for subreddit in SUBREDDITS:
            print(f"Scanning r/{subreddit}...")
            for post in reddit.subreddit(subreddit).new(limit=20):
                process_post(post)
        print("⏳ Sleeping for 60 seconds...")
        time.sleep(60)


if __name__ == "__main__":
    main()
