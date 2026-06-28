import asyncio
import random
import logging

class AsyncRetry:
    def __init__(self, retries=5, base_delay=0.5, backoff=2):
        self.retries = retries
        self.base_delay = base_delay
        self.backoff = backoff

    async def run(self, func, *args, **kwargs):
        delay = self.base_delay

        for attempt in range(self.retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.retries - 1:
                    logging.error(f"Max retries reached: {e}")
                    raise

                jitter = random.uniform(0, delay * 0.3)
                await asyncio.sleep(delay + jitter)
                delay *= self.backoff