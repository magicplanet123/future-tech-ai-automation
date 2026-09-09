import schedule
import time
import sys
import os
from autonomous_agent import AutonomousContentAgent

def generate_content():
    print("="*80)
    print("🤖 AUTONOMOUS CONTENT GENERATION")
    print("="*80)
    try:
        agent = AutonomousContentAgent()
        agent.generate_daily_content()
        print("✅ Content generation complete")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def start_scheduler():
    # Schedule content generation at 8 AM Dubai time (UTC+4)
    # For Railway, use UTC: 8 AM Dubai = 4 AM UTC
    schedule.every().day.at("04:00").do(generate_content)
    
    print("⏰ Scheduler started")
    print("📅 Content generation scheduled daily at 04:00 UTC (8:00 AM Dubai)")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
