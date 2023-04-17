from piece import Piece
from artist import Artist
from audio import Audio
from supabase_client import SupabaseClient
from internet_archive_client import *
from elevenlabs_client import *
from timon_supabase_client import *
from urllib.parse import unquote
from bad_file_list import bad_file_list

client = SupabaseClient()

PIECE_COLLECTION_IDENTIFIER = '1885564100'
ARTIST_COLLECTION_IDENTIFIER = '39215337'

def create_audio_for_piece(piece: Piece):
    # root_path = '/Users/kaseym/Downloads/MP3s'
    existing_audio = client.get_audio_by_piece(piece)
    if existing_audio: 
        print('Audio already exists for piece: ', piece)
        return

    if not piece.overview:
        return

    print('Generating audio for piece: ', piece)

    file_name = '{}.mp3'.format(piece.title)
    # file_path = os.path.join(root_path, file_name)

    mp3_bytesIO = text_to_speech(piece.overview)
    mp3_bytesIO.name = file_name
    url = upload_file(PIECE_COLLECTION_IDENTIFIER, mp3_bytesIO)

    new_audio = Audio(
        id=None,
        created_at=None,
        entity_type="piece",
        entity_id=piece.id,
        link=url
    )

    client.add_audio(new_audio)

def create_audio_for_artist(artist: Artist):
    # root_path = '/Users/kaseym/Downloads/MP3s'
    existing_audio = client.get_audio_by_artist(artist)
    if existing_audio: 
        print('Audio already exists for artist: ', artist)
        return

    if not artist.biography:
        return
    
    print('Generating audio for artist: ', artist)

    file_name = '{}.mp3'.format(artist.artist_name)
    # file_path = os.path.join(root_path, file_name)

    mp3_bytesIO = text_to_speech(artist.biography)
    if not mp3_bytesIO:
        return
    
    mp3_bytesIO.name = file_name
    url = upload_file(ARTIST_COLLECTION_IDENTIFIER, mp3_bytesIO)

    new_audio = Audio(
        id=None,
        created_at=None,
        entity_type="artist",
        entity_id=artist.id,
        link=url
    )

    client.add_audio(new_audio)

def select_pieces() -> List[Piece]:
    pieces = client.get_all_pieces()
    selected_pieces = []

    for piece in pieces:
        if piece.overview != 'Not found':
            selected_pieces.append(piece)
            # print(piece, '\n\n')
    print(f'{len(selected_pieces)} pieces found')
    return selected_pieces

def select_artists() -> List[Artist]:
    selected_pieces = select_pieces()
    selected_artists = []

    for piece in selected_pieces:
        artist = client.get_artist_by_name(piece.artist)
        if artist and artist.biography != 'Not found':
            selected_artists.append(artist)
    print(f'{len(selected_artists)} artists found')
    return selected_artists

def map_audits():
    audits = get_all_audits()
    for audit in audits:
        if audit.content:
            piece = client.get_piece_by_id(audit.art_id)
            # print("piece_title:", piece.title, "audit_content:", audit.content)
            if piece.overview == 'Not found':
                piece.overview = audit.content
                client.update_piece(piece)

def remove_tainted_audios():
    pieces = client.get_all_pieces()
    deleted_audio_log = ""

    for piece in pieces:
        if piece.overview == 'Not found':
            audio = client.get_audio_by_piece(piece)
            if audio:
                client.delete_audio(audio.id)
                deleted_audio_log += str(audio) + '\n'
    
    with open('deleted_audios.txt', 'w') as file:
        file.write(deleted_audio_log)

def main():
    """
    The main function of the program.
    """
    # piece_id = 72324
    # piece = get_piece(id=piece_id)
    # full_pipeline(piece)

    # map_audits()

    # selected_pieces = select_pieces()
    # for piece in selected_pieces:
    #     create_audio_for_piece(piece)

    # selected_artists = select_artists()
    # for artist in selected_artists:
    #     create_audio_for_artist(artist)

    # remove_tainted_audios()


if __name__ == '__main__':
    main()