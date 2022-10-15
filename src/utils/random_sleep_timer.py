import logging, time, random

def random_sleep_timer(min_delay_between_request: int, max_delay_between_request: int) -> None:
    timer: int = random.randint(min_delay_between_request, max_delay_between_request)
    logging.debug(f"Sleeping for {timer} seconds")
    time.sleep(timer)