"""
VIDEO GENERATION MODULE
Uses LongCat-Video and dramaclaw for autonomous video/reel generation
Integrates with autonomous agent
"""

import os
import subprocess
import json
from typing import Optional
import requests

# ================== CONFIGURATION ==================

MEDIA_DIR = "/app/media"
REPOS_DIR = "/app/repos"  # Where repos are cloned on Railway

os.makedirs(MEDIA_DIR, exist_ok=True)

class VideoGenerator:
    """Generate AI videos using LongCat-Video and dramaclaw"""

    @staticmethod
    def generate_with_longcat(prompt: str, niche: str) -> Optional[str]:
        """Generate video using LongCat-Video (text-to-video)"""
        try:
            print(f"  Generating with LongCat-Video: {prompt[:40]}...")

            # LongCat-Video command structure
            longcat_path = os.path.join(REPOS_DIR, "LongCat-Video")

            if not os.path.exists(longcat_path):
                print(f"    ⚠️ LongCat-Video not found at {longcat_path}")
                return None

            # Run LongCat-Video text-to-video generation
            cmd = [
                "torchrun",
                "run_demo_text_to_video.py",
                f"--checkpoint_dir={os.path.join(longcat_path, 'weights', 'LongCat-Video')}",
                f"--prompt={prompt}",
                f"--output_path={MEDIA_DIR}",
                "--enable_compile"
            ]

            result = subprocess.run(cmd, cwd=longcat_path, capture_output=True, timeout=300)

            if result.returncode == 0:
                # Find generated video
                video_files = [f for f in os.listdir(MEDIA_DIR) if f.endswith('.mp4')]
                if video_files:
                    video_path = os.path.join(MEDIA_DIR, video_files[-1])
                    print(f"    ✓ Generated: {video_files[-1]}")
                    return video_path

        except Exception as e:
            print(f"    ✗ LongCat error: {str(e)[:50]}")

        return None

    @staticmethod
    def generate_with_dramaclaw(prompt: str, niche: str) -> Optional[str]:
        """Generate narrative/drama video using dramaclaw"""
        try:
            print(f"  Generating with dramaclaw: {prompt[:40]}...")

            dramaclaw_path = os.path.join(REPOS_DIR, "dramaclaw")

            if not os.path.exists(dramaclaw_path):
                print(f"    ⚠️ dramaclaw not found at {dramaclaw_path}")
                return None

            # dramaclaw generation command
            cmd = [
                "python",
                "generate.py",
                f"--prompt={prompt}",
                f"--output={MEDIA_DIR}",
                "--style=professional"
            ]

            result = subprocess.run(cmd, cwd=dramaclaw_path, capture_output=True, timeout=300)

            if result.returncode == 0:
                video_files = [f for f in os.listdir(MEDIA_DIR) if f.endswith('.mp4')]
                if video_files:
                    video_path = os.path.join(MEDIA_DIR, video_files[-1])
                    print(f"    ✓ Generated: {video_files[-1]}")
                    return video_path

        except Exception as e:
            print(f"    ✗ dramaclaw error: {str(e)[:50]}")

        return None

    @staticmethod
    def generate_with_replicate(prompt: str, niche: str) -> Optional[str]:
        """Fallback: Generate video using Replicate (free tier)"""
        try:
            print(f"  Generating with Replicate (fallback)...")

            import replicate

            output = replicate.run(
                "dleemiller/longcat-video",
                input={
                    "prompt": prompt,
                    "duration": 5,
                    "fps": 30
                }
            )

            if output:
                video_url = output
                filename = f"replicate_{niche}_{int(__import__('time').time())}.mp4"
                filepath = os.path.join(MEDIA_DIR, filename)

                video_data = requests.get(video_url, timeout=60).content
                with open(filepath, 'wb') as f:
                    f.write(video_data)

                print(f"    ✓ Generated: {filename}")
                return filepath

        except Exception as e:
            print(f"    ✗ Replicate error: {str(e)[:50]}")

        return None

    @staticmethod
    def generate_reel(prompt: str, niche: str) -> Optional[str]:
        """Generate reel video with preference order"""
        print(f"\n🎬 Generating reel for {niche}...")

        # Try in order: dramaclaw (for narrative) → LongCat-Video → Replicate
        video = VideoGenerator.generate_with_dramaclaw(prompt, niche)

        if not video:
            video = VideoGenerator.generate_with_longcat(prompt, niche)

        if not video:
            video = VideoGenerator.generate_with_replicate(prompt, niche)

        return video

    @staticmethod
    def add_captions_with_ffmpeg(video_path: str, caption: str) -> Optional[str]:
        """Add captions to video using FFmpeg"""
        try:
            print(f"  Adding captions with FFmpeg...")

            output_path = video_path.replace(".mp4", "_captioned.mp4")

            # Create subtitle file
            srt_file = video_path.replace(".mp4", ".srt")
            with open(srt_file, 'w') as f:
                f.write("1\n00:00:00,000 --> 00:00:05,000\n")
                f.write(caption[:100] + "\n\n")

            # FFmpeg command to add subtitles
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf", f"subtitles={srt_file}",
                "-c:a", "aac",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=120)

            if result.returncode == 0:
                print(f"    ✓ Captions added")
                return output_path

        except Exception as e:
            print(f"    ✗ FFmpeg error: {str(e)[:50]}")

        return video_path

    @staticmethod
    def generate_reel_with_captions(prompt: str, caption: str, niche: str) -> Optional[str]:
        """Generate reel and add captions"""
        print(f"\n🎬 Generating reel with captions for {niche}...")

        # Generate video
        video = VideoGenerator.generate_reel(prompt, niche)

        if video:
            # Add captions
            video_with_captions = VideoGenerator.add_captions_with_ffmpeg(video, caption)
            return video_with_captions

        return None

# ================== USAGE ==================

def main():
    """Test video generation"""
    print("VIDEO GENERATOR TEST")
    print("="*80)

    prompt = "Professional AI technology workplace with holographic displays and team collaborating"
    caption = "🚀 AI is transforming how we work. #AI #Automation #FutureOfWork"

    video = VideoGenerator.generate_reel_with_captions(prompt, caption, "future_tech_ai")

    if video:
        print(f"\n✅ Generated reel: {video}")
    else:
        print("\n⚠️ Could not generate reel")

if __name__ == "__main__":
    main()
