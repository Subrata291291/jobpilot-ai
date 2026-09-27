from tools.web_fetch import WebFetchTool


tool = WebFetchTool()

result = tool.fetch(
    "https://www.hirist.tech/j/nowpurchase-frontend-developer-single-page-application-1475524"
)

print("\nFetched Job Page:")
print("=================")

if result:
    print(result)
else:
    print("Could not fetch this job page.")