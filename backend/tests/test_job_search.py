from tools.job_search import JobSearchTool


tool = JobSearchTool()

results = tool.search(
    role="Frontend Developer",
    skills=["React.js", "JavaScript"],
    location="Kolkata",
)

print("\nMatching Jobs:")
print("================")

for job in results:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Skills: {', '.join(job['skills'])}")
    print(f"URL: {job['url']}")
    print("----------------")