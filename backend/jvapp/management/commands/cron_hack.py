import asyncio
import threading

from django.core.management import BaseCommand

from jvapp.management.commands.ats_jobs import save_ats_data
from scraper.scraper.runSpiders import run_crawlers

"""
Tried a couple of async methods. Scrapy doesn't play nicely with other async operations, but
other tasks might be able to run together. This code currently doesn't work, but could be updated
once other tasks need to be run
"""


async def run_task(fn, writer, task_name, wait_minutes, *args, **kwargs):
    while True:
        writer(f'Running {task_name}')
        fn(*args, **kwargs)
        writer(f'Completed {task_name}')
        writer(f'Waiting {wait_minutes} for next run of {task_name}')
        await asyncio.sleep(wait_minutes * 60)
        
        
def worker(event, fn, writer, task_name, wait_minutes, *args, **kwargs):
    while not event.isSet():
        writer(f'Running {task_name}')
        fn(*args, **kwargs)
        writer(f'Completed {task_name}')
        writer(f'Waiting {wait_minutes} for next run of {task_name}')
        event.wait(wait_minutes * 60)


class Command(BaseCommand):
    help = 'Testing a kinda cron job'

    def handle(self, *args, **options):
        writer = self.stdout.write
        success_style = self.style.SUCCESS
        event = threading.Event()
        task_1 = threading.Thread(target=worker, args=(
            event,
            lambda: save_ats_data(writer, success_style),
            writer, '<save ATS jobs>', 30
        ))
        task_2 = threading.Thread(target=worker, args=(
            event, run_crawlers, writer, '<job web scraper>', 4
        ))
        task_1.start()
        task_2.start()

        while not event.isSet():
            try:
                event.wait(15)
            except KeyboardInterrupt:
                event.set()
                break
        
        # async def main_command():
        #     task_1 = asyncio.create_task(run_task(
        #         lambda: save_ats_data(writer, success_style),
        #         writer, '<save ATS jobs>', 30
        #     ))
        #     task_2 = asyncio.create_task(run_task(run_crawlers, writer, '<job web scraper>', 4))
        #     await task_1
        #     await task_2
        #
        # asyncio.run(main_command())
