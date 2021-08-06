class Tweet:
    def __init__(
        self,
        status_id: str,
        author_id: str,
        author_name: str,
        date: str,
        text: str,
        media_url: list
    ):
        self.status_id = status_id
        self.author_id = author_id
        self.author_name = author_name
        self.date = date
        self.text = text
        self.media_url = media_url
