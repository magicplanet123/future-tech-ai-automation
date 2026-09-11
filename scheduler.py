import schedule
import time
from datetime import datetime

def generate_content():
    print(f"🤖 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S US/Eastern')}] Autonomous content generation starting...")
    try:
        from autonomous_agent import AutonomousContentAgent
        agent = AutonomousContentAgent()
        agent.generate_daily_content()
        print(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S US/Eastern')}] Content generation complete")
    except Exception as e:
        print(f"❌ Error during content generation: {e}")

def post_content():
    print(f"📱 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S US/Eastern')}] Posting cycle starting...")
    try:
        from posting_service import PostingService
        poster = PostingService()
        poster.post_next_batch()
        print(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S US/Eastern')}] Posting complete")
    except Exception as e:
        print(f"❌ Error during posting: {e}")

schedule.every().day.at("14:00").do(generate_content)
schedule.every(2).hours.do(post_content)

print("=" * 60)
print("🚀 AUTONOMOUS SCHEDULER STARTED (US Eastern Time)")
print("=" * 60)
print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S US/Eastern')}")
print(f"Content generation: Every day at 14:00 US/Eastern (2 PM)")
print(f"Posting cycle: Every 2 hours")
print("=" * 60)

while True:
    schedule.run_pending()
    time.sleep(60)
