import types
from pyrogram import Client
from typing import Any, Optional
from pyrogram.types import Message
from pyrogram.file_id import FileId
from pyrogram.raw.types.messages import Messages
from biisal.server.exceptions import FIleNotFound


def parse_file_id(message: "Message") -> Optional[FileId]:
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

def parse_file_unique_id(message: "Messages") -> Optional[str]:
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id

async def get_file_ids(client: Client, chat_id: int, id: int) -> types.SimpleNamespace:
    message = await client.get_messages(chat_id, id)
    if message.empty:
        raise FIleNotFound
    media = get_media_from_message(message)
    file_unique_id = parse_file_unique_id(message)
    file_id = parse_file_id(message)
    obj = types.SimpleNamespace(
        file_size=getattr(media, "file_size", 0),
        mime_type=getattr(media, "mime_type", ""),
        file_name=getattr(media, "file_name", ""),
        unique_id=file_unique_id,
    )
    for attr in (
        "dc_id", "file_type", "media_id", "access_hash", "file_reference",
        "volume_id", "local_id", "thumbnail_source", "thumbnail_size",
        "chat_id", "chat_access_hash",
    ):
        setattr(obj, attr, getattr(file_id, attr, None))
    return obj

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media


def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, 'file_name', "")

def get_media_file_size(m):
    media = get_media_from_message(m)
    return getattr(media, "file_size", 0)
