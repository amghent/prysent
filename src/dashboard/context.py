class Context:
    def __init__(self, request) -> None:
        self.context = {
            "user": request.user,
        }

    def get(self) -> dict:
        return self.context
