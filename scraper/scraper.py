import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters,
)
import pymongo

jobs = []

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["jobs_database"]
collection = db["jobs_collection"]
collection.delete_many({})


# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)


# Fired once for each successfully processed job
def on_data(data: EventData):
    print(
        "[ON_DATA]",
        data.title,
        data.company,
        data.company_link,
        data.date,
        data.link,
        data.insights,
        len(data.description),
    )

    process_data(data)


def process_data(data: EventData):
    jobs.append(
        {
            "title": data.title,
            "company": data.company,
            "job_link": data.link,
            "description": data.description,
        }
    )


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print("[ON_METRICS]", str(metrics))


def on_error(error):
    print("[ON_ERROR]", error)


def on_end():
    print("[ON_END]")
    save_jobs()


def save_jobs():
    collection.insert_many(jobs)
    print("[SAVE_JOBS]")


scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.75,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40,  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query="Software Engineer",
        options=QueryOptions(
            locations=["Singapore"],
            skip_promoted_jobs=True,
            limit=5,
            filters=QueryFilters(relevance=RelevanceFilters.RECENT),
        ),
    ),
]

scraper.run(queries)
