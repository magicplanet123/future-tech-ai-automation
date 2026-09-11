import schedule
import time
from datetime import datetime

def generate_content():
    print(f"🤖 Autonomous content generation starting...")
    try:
        from autonomous_agent import AutonomousContentAgent
        agent = AutonomousContentAgent()
        agent.generate_daily_content()
        print(f"✅ Content generation complete")
    except Exception as e:
        print(f"❌ Error during content generation: {e}")

def post_content():
    print(f"📱 Posting cycle starting...")
    try:
        from posting_service import PostingService
        poster = PostingService()
        poster.post_next_batch()
        print(f"✅ Posting complete")
    except Exception as e:
        print(f"❌ Error during posting: {e}")

# 19:00 UTC = 11 PM Dubai (UTC+4)
schedule.every().day.at("19:00").do(generate_content)
schedule.every(2).hours.do(post_content)

print("🚀 AUTONOMOUS SCHEDULER STARTED - TEST MODE")
print("Content generation: 19:00 UTC (11 PM Dubai)")
print("Posting cycle: Every 2 hours")

while True:
    schedule.run_pending()
    time.sleep(60)
