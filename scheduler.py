from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_pipeline

scheduler = BlockingScheduler(timezone="Asia/Kolkata")

scheduler.add_job(
    run_pipeline,
    trigger='cron',
    hour=17,
    minute=0
)

print("Scheduler started...")

scheduler.start()