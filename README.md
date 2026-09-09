# Autonomous Social Media Posting System

24/7 autonomous social media posting system using Railway.app, crewAI, and LongCat-Video.

## Features

- ✅ Autonomous content generation (AI agents)
- ✅ AI-generated images (Stable Diffusion)
- ✅ AI-generated videos (LongCat-Video + dramaclaw)
- ✅ Automatic posting every 2 hours
- ✅ Posts to multiple Facebook pages
- ✅ 100% free tier deployment

## Setup

1. Clone repository
2. Add API tokens to Railway dashboard
3. Deploy to Railway.app
4. System runs automatically 24/7

## Tokens Required

- FB_ACCESS_TOKEN (Facebook)
- FB_ACCESS_TOKEN_2 (Facebook)
- REPLICATE_API_TOKEN (Image generation)
- HF_API_TOKEN (Hugging Face)

## Architecture

- autonomous_agent.py: Content generation
- image_generator_module.py: Image generation
- video_generator_module.py: Video generation
- posting_service.py: Facebook posting
- scheduler.py: Cron job scheduling

## Deployment

Deploy to Railway.app with this repo. Railway will automatically:
1. Build the Python environment
2. Set up PostgreSQL database
3. Run the scheduler and posting service
4. Post to Facebook every 2 hours

## Status

✅ Ready for production deployment
