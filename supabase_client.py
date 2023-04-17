from typing import List, Optional, Union
from dotenv import load_dotenv
from supabase import create_client
import os
from piece import Piece
from artist import Artist
from audio import Audio

load_dotenv()

class SupabaseClient:
    def __init__(self):
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_anon_key = os.environ.get('SUPABASE_ANON_KEY')

        self.client = create_client(supabase_url, supabase_anon_key)

    def add_audio(self, audio: Audio):
        """
        Adds a new audio record to the `audios` table in Supabase.

        Args:
            audio: An Audio object representing the audio to be added.

        Raises:
            Exception: If an error occurs while inserting the audio record.

        Returns:
            None
        """
        insert_dict = {
            "entity_type": audio.entity_type,
            "entity_id": audio.entity_id,
            "link": audio.link
        }
        self.client.from_("audios").insert(insert_dict).execute()
        print("Audio added: ", audio)

    def update_audio(self, audio: Audio):
        """
        Updates an existing audio record in the `audios` table in Supabase based on the `entity_id`.

        Args:
            audio: An Audio object representing the updated audio.

        Raises:
            Exception: If an error occurs while updating the audio record.

        Returns:
            None
        """
        update_dict = {
            "entity_type": audio.entity_type,
            "link": audio.link
        }
        result = self.client.from_("audios").update(update_dict).eq("entity_id", audio.entity_id).execute()
        if result['affected_rows'] == 0:
            raise Exception('No audio found with entity_id: {}'.format(audio.entity_id))
        print("Audio updated: ", audio)

    def delete_audio(self, audio_id: int):
        """
        Deletes an audio record from the `audios` table in Supabase.

        Args:
            audio_id: An integer representing the id of the audio record to be deleted.

        Returns:
            None
        """
        try:
            audio = self.get_audio_by_id(audio_id)
            self.client.from_("audios").delete().match({"id": audio_id}).execute()
            print("Audio deleted:", audio)
        except Exception as e:
            print(f"An error occurred while deleting the audio record for audio_id={audio_id}: {e}")

        
    def get_total_pieces_count(self) -> int:
        """Gets the total number of pieces of artwork in the database.

        Returns:
            An integer representing the total number of pieces of artwork.
        """
        response = self.client.from_('pieces').select("id", count="exact").execute() # We only need the 'id' column for counting purposes

        count = response.count
        print('Total count: ', count)
        return int(count)

    def get_all_pieces(self) -> List[Piece]:
        """Gets all pieces of artwork from the database.

        Returns:
            A list of Piece objects representing the artwork.
        Raises:
            Exception: If no pieces are found.
        """
        
        total_pieces_count = self.get_total_pieces_count()
        LIMIT = 1000
        offset = 0
        all_data = []

        while True:
            response = self.client.from_('pieces').select('*').range(offset, offset + LIMIT - 1).execute()
        
            data = response.data
            if not data:
                break

            all_data.extend(data)
            offset += LIMIT
            print(f'get_all_pieces(): {offset} / {total_pieces_count} pieces retrieved ({round((offset/total_pieces_count) * 100)}%)')

        if not all_data:
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
        ) for piece in all_data]

    def get_all_audios(self) -> List[Audio]:
        """Gets all audio records from the database.

        Returns:
            A list of Audio objects representing the audio records.
        Raises:
            Exception: If no audio records are found.
        """
        response = self.client.from_("audios").select("*").execute()
        audio_list = response.data
        if not audio_list:
            raise Exception('No audio records found')

        # Map each audio to a new Audio object
        return [Audio(
            id=audio['id'],
            created_at=audio['created_at'],
            entity_type=audio['entity_type'],
            entity_id=audio['entity_id'],
            link=audio['link']
        ) for audio in audio_list]

    def get_audio_by_id(self, audio_id: str) -> Audio:
        response = self.client.from_("audios").select("*").eq('id', audio_id).limit(1).execute()
        audio = response.data[0] if response.data else None
        if not audio:
            return None

        return Audio(
            id=audio['id'],
            created_at=audio['created_at'],
            entity_type=audio['entity_type'],
            entity_id=audio['entity_id'],
            link=audio['link']
        )
    
    def get_audio_by_piece(self, piece: Piece) -> Audio:
        entity_id = piece.id
        response = self.client.from_("audios").select("*").eq('entity_type', 'piece').eq('entity_id', entity_id).limit(1).execute()
        audio = response.data[0] if response.data else None
        if not audio:
            return None

        return Audio(
            id=audio['id'],
            created_at=audio['created_at'],
            entity_type=audio['entity_type'],
            entity_id=audio['entity_id'],
            link=audio['link']
        )
    
    def get_audio_by_artist(self, artist: Artist) -> Audio:
        entity_id = artist.id
        response = self.client.from_("audios").select("*").eq('entity_type', 'artist').eq('entity_id', entity_id).limit(1).execute()
        audio = response.data[0] if response.data else None
        if not audio:
            return None

        return Audio(
            id=audio['id'],
            created_at=audio['created_at'],
            entity_type=audio['entity_type'],
            entity_id=audio['entity_id'],
            link=audio['link']
        )

    def search_pieces(self, title: str, artist: str) -> Piece:
        """Searches for pieces of artwork by title and artist.

        Args:
            title: The title of the artwork.
            artist: The artist who created the artwork.

        Returns:
            A Piece object representing the artwork, if it is found. Otherwise, None.
        """
        search_term = f'{title} {artist}'
        response = self.client.rpc('search_pieces', {'search_term': search_term}).limit(1).execute()
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

    def get_piece_by_id(self, piece_id: int) -> Optional[Piece]:
        """Gets a piece of artwork by ID.

        Args:
            piece_id: The ID of the artwork to retrieve.

        Returns:
            A Piece object representing the artwork, if it is found. Otherwise, None.
        """
        response = self.client.from_('pieces').select('*').eq('id', piece_id).limit(1).execute()
        piece = response.data[0] if response.data else None
        if not piece:
            return None

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

    def get_piece_by_title(self, title: str) -> Optional[Piece]:
        """Gets a piece of artwork by title.

        Args:
            title: The title of the artwork to retrieve.

        Returns:
            A Piece object representing the artwork, if it is found. Otherwise, None.
        """
        response = self.client.from_('pieces').select('*').ilike('title', title).limit(1).execute()
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

    def get_artist_by_name(self, name: str) -> Optional[Artist]:
        """Gets an artist by name.

        Args:
            name: The name of the artist to retrieve.

        Returns:
            An Artist object representing the artist, if found. Otherwise, None.
        """
        response = self.client.from_('artists').select('*').eq('artist_name', name).limit(1).execute()
        artist_data = response.data[0] if response.data else None
        if not artist_data:
            return None

        # Create a new Artist object from the response data
        return Artist(
            id=artist_data['id'],
            artist_name=artist_data['artist_name'],
            nationality=artist_data['nationality'],
            lifespan=artist_data['lifespan'],
            biography=artist_data['biography']
        )
    
    def get_piece(self,
            id: Union[int, None] = None, 
            title: Union[str, None] = None, 
            displaydate: Union[str, None] = None, 
            artist: Union[str, None] = None, 
            location: Union[str, None] = None, 
            overview: Union[str, None] = None, 
            description: Union[str, None] = None) -> Piece:
        """Gets a piece of artwork from the database based on the given parameters.

        Args:
            id (int or None): The ID of the piece of artwork.
            title (str or None): The title of the piece of artwork.
            displaydate (str or None): The display date of the piece of artwork.
            artist (str or None): The artist of the piece of artwork.
            location (str or None): The location of the piece of artwork.
            overview (str or None): The overview of the piece of artwork.
            description (str or None): The description of the piece of artwork.
        
        Returns:
            A Piece object representing the matching artwork.
        Raises:
            Exception: If no matching artwork is found.
        """

        query = self.client.from_("pieces").select("*")
        if id is not None:
            query = query.eq("id", id)
        if title is not None:
            query = query.ilike("title", f"%{title}%")
        if displaydate is not None:
            query = query.ilike("displaydate", f"%{displaydate}%")
        if artist is not None:
            query = query.ilike("artist", f"%{artist}%")
        if location is not None:
            query = query.ilike("location", f"%{location}%")
        if overview is not None:
            query = query.ilike("overview", f"%{overview}%")
        if description is not None:
            query = query.ilike("description", f"%{description}%")

        response = query.limit(1).execute()
        piece = response.data[0] if response.data else None
        if not piece:
            raise Exception('Piece not found')

        # Map each piece to a new Piece object
        return Piece(
            id=piece['id'],
            title=piece['title'],
            displaydate=piece['displaydate'],
            artist=piece['artist'],
            location=piece['location'],
            overview=piece['overview'],
            description=piece['description'],
        )

    def get_pieces(self,
            id: Union[int, None] = None, 
            title: Union[str, None] = None, 
            displaydate: Union[str, None] = None, 
            artist: Union[str, None] = None, 
            location: Union[str, None] = None, 
            overview: Union[str, None] = None, 
            description: Union[str, None] = None) -> List[Piece]:
        """Gets pieces of artwork from the database based on the given parameters.

        Args:
            id (int or None): The ID of the piece of artwork.
            title (str or None): The title of the piece of artwork.
            displaydate (str or None): The display date of the piece of artwork.
            artist (str or None): The artist of the piece of artwork.
            location (str or None): The location of the piece of artwork.
            overview (str or None): The overview of the piece of artwork.
            description (str or None): The description of the piece of artwork.
        
        Returns:
            A list of Piece objects representing the matching artwork.
        Raises:
            Exception: If no matching artwork is found.
        """

        query = self.client.from_("pieces").select("*")
        if id is not None:
            query = query.eq("id", id)
        if title is not None:
            query = query.ilike("title", f"%{title}%")
        if displaydate is not None:
            query = query.ilike("displaydate", f"%{displaydate}%")
        if artist is not None:
            query = query.ilike("artist", f"%{artist}%")
        if location is not None:
            query = query.ilike("location", f"%{location}%")
        if overview is not None:
            query = query.ilike("overview", f"%{overview}%")
        if description is not None:
            query = query.ilike("description", f"%{description}%")


        response = query.execute()
        pieces = response.data if response.data else None
        if not pieces:
            raise Exception('Piece not found')

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

    def update_piece(self, piece: Piece):
        """
        Updates an existing artwork record in the `pieces` table in Supabase based on the `id`.

        Args:
            piece: A Piece object representing the updated artwork.

        Raises:
            Exception: If an error occurs while updating the artwork record.

        Returns:
            None
        """
        update_dict = {
            "title": piece.title,
            "displaydate": piece.displaydate,
            "artist": piece.artist,
            "location": piece.location,
            "overview": piece.overview,
            "description": piece.description
        }
        result = self.client.from_("pieces").update(update_dict).eq("id", piece.id).execute()
        if result.count == 0:
            raise Exception('No piece found with id: {}'.format(piece.id))
        print("Piece updated: ", piece)

def main():
    """
    The main function of the program.
    """
    # pieces: List[Piece] = get_all_pieces()
    # for piece in pieces:
    #     print(piece.title)

    client = SupabaseClient()
    audios = client.get_all_audios()
    for audio in audios:
        print(audio)
        if audio.entity_type == 'piece':
            piece: Piece = client.get_piece(id=audio.entity_id)
            print(piece)


if __name__ == '__main__':
    main()