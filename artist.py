class Artist:
    def __init__(self, id: int, artist_name: str, nationality: str, lifespan: int, biography: str):
        self.id = id
        self.artist_name = artist_name
        self.nationality = nationality
        self.lifespan = lifespan
        self.biography = biography

    def __str__(self):
        return f"Audio(id={self.id}, artist_name={self.artist_name}, nationality={self.nationality}, lifespan={self.lifespan}, biography={self.biography})"