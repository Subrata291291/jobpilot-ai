from tools.web_search import WebSearchTool


tool = WebSearchTool()

result = tool.search(
    "Find current Frontend Developer jobs in Kolkata India. "
    "Return relevant job titles, companies, locations and URLs."
)

print("\nWeb Search Results:")
print("===================")
print(result)