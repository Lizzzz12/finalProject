class BaseScraper:
    def fetch(self, url):
        raise NotImplementedError

    def parse(self, content):
        raise NotImplementedError