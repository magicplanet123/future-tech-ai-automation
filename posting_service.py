"""
FINAL POSTING SYSTEM - SIMPLE & RELIABLE
Posts with IMAGES directly to Facebook
No complex carousel logic - just post images + captions
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Load credentials
def load_env():
    env_path = r"C:\Users\sumyi\OneDrive\Desktop\Future Tech AI\.env"
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

NICHES = {
    "future_tech_ai": {
        "page_id": "1176773852176361",
        "token": os.environ.get("FB_ACCESS_TOKEN", ""),
    },
    "uae_will_services": {
        "page_id": "101102988474969",
        "token": os.environ.get("FB_ACCESS_TOKEN_2", ""),
    }
}

PROJECT_DIR = r"C:\Users\sumyi\OneDrive\Desktop\Future Tech AI"
MEDIA_DIR = os.path.join(PROJECT_DIR, "media")
LOG_FILE = os.path.join(PROJECT_DIR, "posting_log_final.txt")

def log_msg(msg, niche="SYSTEM"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] [{niche}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(formatted + "\n")
    except:
        pass

def post_image_with_caption(niche_name, image_path, caption):
    """Post image directly to Facebook page with caption"""
    try:
        config = NICHES.get(niche_name)
        if not config or not config.get("token"):
            log_msg(f"❌ No credentials for {niche_name}", niche_name)
            return False

        page_id = config["page_id"]
        access_token = config["token"]
        url = f"https://graph.facebook.com/v18.0/{page_id}/photos"

        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            params = {
                'access_token': access_token,
                'caption': caption
            }

            response = requests.post(url, files=files, params=params, timeout=30)
            result = response.json()

            if "id" in result:
                log_msg(f"✅ Image posted! File: {os.path.basename(image_path)}", niche_name)
                return True
            else:
                error = result.get("error", {}).get("message", "Unknown")
                log_msg(f"❌ Failed: {error}", niche_name)
                return False

    except Exception as e:
        log_msg(f"❌ Error: {str(e)[:100]}", niche_name)
        return False

def post_text_with_caption(niche_name, caption):
    """Post text to Facebook"""
    try:
        config = NICHES.get(niche_name)
        if not config or not config.get("token"):
            log_msg(f"❌ No credentials for {niche_name}", niche_name)
            return False

        page_id = config["page_id"]
        access_token = config["token"]
        url = f"https://graph.facebook.com/v18.0/{page_id}/feed"

        params = {
            'message': caption,
            'access_token': access_token
        }

        response = requests.post(url, data=params, timeout=30)
        result = response.json()

        if "id" in result:
            log_msg(f"✅ Text posted!", niche_name)
            return True
        else:
            error = result.get("error", {}).get("message", "Unknown")
            log_msg(f"❌ Failed: {error}", niche_name)
            return False

    except Exception as e:
        log_msg(f"❌ Error: {str(e)[:100]}", niche_name)
        return False

def main():
    print("="*80)
    print("POSTING SYSTEM - WITH IMAGES")
    print("="*80)

    total_posted = 0

    for niche in NICHES.keys():
        print(f"\n📱 {niche}")
        print("-"*80)

        # Get all posts
        queue_dir = Path(PROJECT_DIR)
        pattern = "POST_*.json" if niche == "future_tech_ai" else "UAE_WILL_*.json"
        posts = sorted(queue_dir.glob(pattern), reverse=True)  # NEWEST FIRST!

        # Separate carousel and text posts
        carousel_posts = []
        text_posts = []

        for post_file in posts:
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post_data = json.load(f)
                    media_type = post_data.get("metadata", {}).get("media_type", "text")
                    if media_type == "carousel":
                        carousel_posts.append(post_file)
                    else:
                        text_posts.append(post_file)
            except:
                pass

        # POST CAROUSELS FIRST (with images), then text
        posts = carousel_posts[:3] + text_posts[:2]

        # Process up to 5 posts
        for post_file in posts:
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post_data = json.load(f)

                content = post_data.get("content", {})
                metadata = post_data.get("metadata", {})

                caption = content.get("caption_text", "")
                images = content.get("images", [])
                media_type = metadata.get("media_type", "text")

                log_msg(f"Processing: {post_file.name} (type: {media_type})", niche)

                # Post with images if available
                if images and media_type == "carousel":
                    for idx, img_path in enumerate(images):
                        if os.path.exists(img_path):
                            img_caption = f"{caption}\n\n📸 Image {idx+1}/{len(images)}"
                            if post_image_with_caption(niche, img_path, img_caption):
                                total_posted += 1

                # Post text only
                elif media_type == "text":
                    if post_text_with_caption(niche, caption):
                        total_posted += 1

                # Delete after posting
                try:
                    post_file.unlink()
                except:
                    pass

            except Exception as e:
                log_msg(f"Error: {str(e)[:50]}", niche)

        print(f"Posted: {total_posted} from {niche}\n")

    print("="*80)
    print(f"✅ COMPLETE - Total: {total_posted} posts")
    print("="*80)

if __name__ == "__main__":
    main()
