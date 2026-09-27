from tools.web_search import WebSearchTool
from services.job_extractor import JobExtractor


search_tool = WebSearchTool()

search_results = search_tool.search(
    "Find current Frontend Developer jobs in Kolkata India. "
    "Return relevant job titles, companies, locations and URLs."
)

extractor = JobExtractor()

jobs = extractor.extract(search_results)

print("\nStructured Jobs:")
print("================")

for job in jobs:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Skills: {job['skills']}")
    print(f"URL: {job['url']}")
    print("----------------")