from typing import Any, Dict, Type, Union, Iterable, Optional

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment):
    """
    telegram 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return self.data["text"]
        return ""

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def photo(
        file: Union[str, bytes], caption: Optional[str] = None
    ) -> "MessageSegment":
        return MessageSegment("photo", {"file": file, "caption": caption})

    @staticmethod
    def voice(
        file: Union[str, bytes], caption: Optional[str] = None
    ) -> "MessageSegment":
        return MessageSegment("voice", {"file": file, "caption": caption})

    @staticmethod
    def animation(
        file: Union[str, bytes],
        thumb: Union[str, bytes] = None,
        caption: Optional[str] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "animation", {"file": file, "thumb": thumb, "caption": caption}
        )

    @staticmethod
    def audio(
        file: Union[str, bytes],
        thumb: Union[str, bytes] = None,
        caption: Optional[str] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "audio", {"file": file, "thumb": thumb, "caption": caption}
        )

    @staticmethod
    def document(
        file: Union[str, bytes],
        thumb: Union[str, bytes] = None,
        caption: Optional[str] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "document", {"file": file, "thumb": thumb, "caption": caption}
        )

    @staticmethod
    def video(
        file: Union[str, bytes],
        thumb: Union[str, bytes] = None,
        caption: Optional[str] = None,
    ) -> "MessageSegment":
        return MessageSegment(
            "video", {"file": file, "thumb": thumb, "caption": caption}
        )


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type["MessageSegment"]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)

    @classmethod
    def parse_obj(cls, obj: Dict[str, Any]) -> "Message":
        msg = []
        for key in obj:
            if key == "text":
                msg.append(
                    MessageSegment(
                        key, {key: obj[key], "entities": obj.get("entities")}
                    )
                )
            elif key == "photo":
                msg.append(
                    MessageSegment(
                        key,
                        {
                            "file": obj[key][0]["file_id"],
                            "caption": obj.get("caption"),
                            "caption_entities": obj.get("caption_entities"),
                        },
                    )
                )
            elif key in [
                "animation",
                "audio",
                "document",
                "video",
                "voice",
            ]:
                msg.append(
                    MessageSegment(
                        key,
                        {
                            key: obj[key],
                            "caption": obj.get("caption"),
                            "caption_entities": obj.get("caption_entities"),
                        },
                    )
                )
            elif key in ["sticker", "video_note", "dice", "poll"]:
                msg.append(MessageSegment(key, {key: obj[key]}))
        return cls(msg)
