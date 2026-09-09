"""
AUTONOMOUS CONTENT GENERATION AGENT
Generates posts, images, and videos completely autonomously
Runs on Railway.app cloud server 24/7
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict

# ================== CONFIGURATION ==================

OUTPUT_DIR = "/app/content_queue"  # Railway file system
DATABASE_DIR = "/app/database"
MEDIA_DIR = "/app/media"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

NICHES = {
    "future_tech_ai": {
        "page_id": "1176773852176361",
        "descriptions": [
            "AI automation professional workspace",
            "Tech innovation and digital transformation",
            "Future workplace with AI systems",
            "Machine learning and neural networks",
            "Business automation technology"
        ],
        "post_templates": [
            "🚀 {title}\n\n{body}\n\n💡 Key insight: {insight}\n\n{hashtags}",
            "🤖 {title}\n\n{body}\n\n→ {action}\n\n{hashtags}",
            "⚡ Quick Tip: {title}\n\n{body}\n\n{call_to_action}\n\n{hashtags}",
        ],
        "titles": [
            "5 AI Tools That Transformed My Business",
            "Automation Saves 50+ Hours Weekly",
            "The Future of Work Starts Now",
            "AI is Reshaping Business Strategy",
            "Smart Automation for Growth"
        ],
        "hashtags": "#AI #Automation #FutureOfWork #TechTrends #Innovation #ProductivityHacks"
    },
    "uae_will_services": {
        "page_id": "101102988474969",
        "descriptions": [
            "Professional legal family protection",
            "Estate planning and wealth management",
            "Family financial security planning",
            "UAE legal services and documentation",
            "Inheritance and asset protection"
        ],
        "post_templates": [
            "📋 {title}\n\n{body}\n\n⚖️ Important: {important}\n\n{hashtags}",
            "🛡️ {title}\n\n{body}\n\n✓ Action: {action}\n\n{hashtags}",
            "📚 {title}\n\nKey Points:\n{body}\n\n👨‍👩‍👧‍👦 {family_note}\n\n{hashtags}",
        ],
        "titles": [
            "Protect Your Family's Future Today",
            "Estate Planning Made Simple",
            "Why Your Will Matters Now",
            "Family Financial Security Starts Here",
            "Plan Your Legacy Today"
        ],
        "hashtags": "#UAE #EstateePlanning #FamilyProtection #LegalAdvice #FinancialSecurity"
    }
}

# ================== CONTENT GENERATION ==================

class AutonomousContentAgent:
    """Generates posts, images, and videos autonomously"""

    def __init__(self):
        self.queue_file = os.path.join(DATABASE_DIR, "content_queue.json")
        self.load_queue()

    def load_queue(self):
        """Load existing queue"""
        if os.path.exists(self.queue_file):
            with open(self.queue_file, 'r') as f:
                self.queue = json.load(f)
        else:
            self.queue = {"future_tech_ai": [], "uae_will_services": []}

    def save_queue(self):
        """Save queue to file"""
        with open(self.queue_file, 'w') as f:
            json.dump(self.queue, f, indent=2)

    def generate_post_text(self, niche: str) -> str:
        """Generate unique post text using crewAI-style logic"""
        niche_data = NICHES.get(niche, {})

        template = random.choice(niche_data.get("post_templates", ["default"]))
        title = random.choice(niche_data.get("titles", ["Check this out"]))
        body = f"Discover how {niche} solutions can transform your approach."
        insight = "Stay ahead by embracing innovation today"
        action = "Start your journey now"
        hashtags = niche_data.get("hashtags", "#business")
        call_to_action = "Learn more and take action"
        important = "This is essential for your success"
        family_note = "Your family's future depends on smart planning"

        caption = template.format(
            title=title,
            body=body,
            insight=insight,
            action=action,
            hashtags=hashtags,
            call_to_action=call_to_action,
            important=important,
            family_note=family_note
        )

        return caption

    def generate_image_prompt(self, niche: str) -> str:
        """Generate image prompt for Stable Diffusion"""
        descriptions = NICHES[niche].get("descriptions", ["professional image"])
        return random.choice(descriptions)

    def generate_video_prompt(self, niche: str) -> str:
        """Generate video prompt for LongCat-Video or dramaclaw"""
        if niche == "future_tech_ai":
            prompts = [
                "Professional AI workplace with technology and innovation",
                "Digital transformation in modern business",
                "AI automation bringing efficiency to teams",
                "Technology experts collaborating on innovation",
                "Future workplace with smart systems"
            ]
        else:
            prompts = [
                "Professional legal consultation about family protection",
                "Estate planning discussion with financial advisor",
                "Family meeting about wealth and security planning",
                "Professional lawyer discussing inheritance laws",
                "Secure family future visualization"
            ]
        return random.choice(prompts)

    def create_carousel_content(self, niche: str) -> Dict:
        """Create carousel post (text + 3 images)"""
        return {
            "type": "carousel",
            "caption": self.generate_post_text(niche),
            "image_prompts": [
                self.generate_image_prompt(niche),
                self.generate_image_prompt(niche),
                self.generate_image_prompt(niche)
            ],
            "niche": niche,
            "created_at": datetime.now().isoformat()
        }

    def create_reel_content(self, niche: str) -> Dict:
        """Create reel post (video + text)"""
        return {
            "type": "reel",
            "caption": self.generate_post_text(niche),
            "video_prompt": self.generate_video_prompt(niche),
            "niche": niche,
            "created_at": datetime.now().isoformat()
        }

    def create_text_content(self, niche: str) -> Dict:
        """Create text-only post"""
        return {
            "type": "text",
            "caption": self.generate_post_text(niche),
            "niche": niche,
            "created_at": datetime.now().isoformat()
        }

    def generate_daily_content(self):
        """Generate 10 posts per day (5 per niche)"""
        print("="*80)
        print("AUTONOMOUS CONTENT GENERATION")
        print("="*80)

        for niche in NICHES.keys():
            print(f"\n📝 Generating content for: {niche}")
            print("-"*80)

            # Mix: 2 carousels, 2 reels, 1 text per niche
            posts = []

            # 2 Carousel posts
            for i in range(2):
                carousel = self.create_carousel_content(niche)
                posts.append(carousel)
                print(f"  ✓ Carousel {i+1}")

            # 2 Reel posts
            for i in range(2):
                reel = self.create_reel_content(niche)
                posts.append(reel)
                print(f"  ✓ Reel {i+1}")

            # 1 Text post
            text = self.create_text_content(niche)
            posts.append(text)
            print(f"  ✓ Text post")

            # Add to queue
            self.queue[niche].extend(posts)

        self.save_queue()

        print("\n" + "="*80)
        print(f"✅ GENERATION COMPLETE")
        print("="*80)
        print(f"Future Tech AI queue: {len(self.queue['future_tech_ai'])} posts")
        print(f"UAE Will Services queue: {len(self.queue['uae_will_services'])} posts")
        print(f"\nTotal ready to post: {len(self.queue['future_tech_ai']) + len(self.queue['uae_will_services'])}")

    def get_next_post(self, niche: str) -> Dict:
        """Get next post from queue (for posting)"""
        if self.queue[niche]:
            post = self.queue[niche].pop(0)
            self.save_queue()
            return post
        return None

# ================== MAIN ==================

def main():
    agent = AutonomousContentAgent()
    agent.generate_daily_content()

if __name__ == "__main__":
    main()
