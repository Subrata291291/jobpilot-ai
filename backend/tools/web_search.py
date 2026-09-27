from tools.providers.factory import get_search_provider


class WebSearchTool:

    def __init__(self):
        self.provider = get_search_provider()

    def search(self, query: str) -> str:
        return self.provider.search(query)