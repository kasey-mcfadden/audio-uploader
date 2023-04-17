class Piece:
    def __init__(self, id: int, title: str, displaydate: str, artist: str, location: str, overview: str, description: str):
        """Represents a piece of artwork from the database."""
        self.id = id
        self.title = title
        self.displaydate = displaydate
        self.artist = artist
        self.location = location
        self.overview = overview
        self.description = description

    def __str__(self) -> str:
        # return f'Piece(\nid={self.id}, \ntitle={self.title}, \ndisplaydate={self.displaydate}, \nartist={self.artist}, location={self.location}, overview={self.overview}, description={self.description})'
        return f'Piece(\nid={self.id}, \ntitle={self.title}, \ndisplaydate={self.displaydate}, \nartist={self.artist})\n'
    