from sqlmodel import Field, SQLModel


class Song(SQLModel, table=True):
    song_id: int | None = Field(default=None, primary_key=True)
    song_name: str
    album: str
    band: str
    track: int
    lyrics: str
