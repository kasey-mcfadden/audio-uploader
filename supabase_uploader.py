from typing import List, Optional
from dotenv import load_dotenv
from supabase import create_client
import os
load_dotenv()

# Define the Supabase URL and anon key from environment variables
supabase_url = os.environ.get('NEXT_PUBLIC_SUPABASE_URL')
supabase_anon_key = os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')

# Create a Supabase client instance
client = create_client(supabase_url, supabase_anon_key)

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
        return f'Piece(id={self.id}, title={self.title}, displaydate={self.displaydate}, artist={self.artist}, location={self.location}, overview={self.overview}, description={self.description})'

def get_all_pieces() -> List[Piece]:
    """Gets all pieces of artwork from the database.

    Returns:
        A list of Piece objects representing the artwork.
    Raises:
        Exception: If no pieces are found.
    """
    response = client.from_('pieces').select('*').execute()
    pieces = response.data
    if not pieces:
        raise Exception('No pieces found')

    # Map each piece to a new Piece object
    return [Piece(
        id=piece['id'],
        title=piece['title'],
        displaydate=piece['displaydate'],
        artist=piece['artist'],
        location=piece['location'],
        overview=piece['overview'],
        description=piece['description'],
    ) for piece in pieces]

def search_pieces(title: str, artist: str):
    """Searches for pieces of artwork by title and artist.

    Args:
        title: The title of the artwork.
        artist: The artist who created the artwork.

    Returns:
        A Piece object representing the artwork, if it is found. Otherwise, None.
    """
    search_term = f'{title} {artist}'
    response = client.rpc('search_pieces', {'search_term': search_term}).limit(1).execute()
    piece = response.data[0] if response.data else None
    if not piece:
        raise Exception('Piece not found')

    # Create a new Piece object from the response data
    return Piece(
        id=piece['id'],
        title=piece['title'],
        displaydate=piece['displaydate'],
        artist=piece['artist'],
        location=piece['location'],
        overview=piece['overview'],
        description=piece['description']
    )

def get_piece_by_title(title: str) -> Optional[Piece]:
    """Gets a piece of artwork by title.

    Args:
        title: The title of the artwork to retrieve.

    Returns:
        A Piece object representing the artwork, if it is found. Otherwise, None.
    """
    response = client.from_('pieces').select('*').eq('title', title).limit(1).execute()
    piece = response.data[0] if response.data else None
    if not piece:
        raise Exception('Piece not found')

    # Create a new Piece object from the response data
    return Piece(
        id=piece['id'],
        title=piece['title'],
        displaydate=piece['displaydate'],
        artist=piece['artist'],
        location=piece['location'],
        overview=piece['overview'],
        description=piece['description']
    )

def main():
    """
    The main function of the program.
    """
    # pieces: List[Piece] = get_all_pieces()
    # for piece in pieces:
    #     print(piece.title)

    title = 'The Flight with Obelisk at the Left'
    piece: Piece = get_piece_by_title(title)
    print(piece)

if __name__ == '__main__':
    main()