import httpx


class HttpClient:
    def __init__(self) -> None:
        ...

    def client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient()
