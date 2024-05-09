# -*- coding: utf-8 -*-
from .Caption import Caption
from .Message import Message
from .Send import Send
from .telegram_request import TelegramRequests


class MediaGroup(Send):

    def __init__(self, requests: TelegramRequests):
        super().__init__(requests=requests)
        self.message = Message(self.requests)
        self.caption = Caption()

    def send(
        self,
        document_paths: list,
        caption: str = None,
        media_type: str = 'document',
        parse_mode: str = None,
        max_request_attempts: int = 10
    ) -> None:
        """
        :param max_request_attempts:
        :param parse_mode: HTML, Markdown, MarkdownV2
        :param document_paths:
        :param caption:
        :param media_type: types: 'photo', 'video', 'audio', 'document', 'voice', 'animation'
        :return:
        """

        if not document_paths:
            return self.message.send(f"No files to send. {caption if caption else ''}", out_msg=True)

        if caption and len(caption) > self.__MAX_CAPTCHA_LENGTH:
            document_paths.append(self.message.make_doc(caption, 'caption.txt'))

        while max_request_attempts > 0:
            files, media = {}, []
            for doc_path in document_paths:
                files[basename(doc_path)] = open(self.msg.prepare_documents(doc_path), 'rb')
                media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))

            media[-1]['caption'] = self.msg.prepare_caption(caption) if caption is not None else ''
            media[-1]['parse_mode'] = parse_mode or self.__DEFAULT_PARSE_MOD

            media_group_data = {'chat_id': self.requests.auth.chat_id, 'media': dumps(media)}

            if self.requests.post('sendMediaGroup', data=media_group_data, files=files):
                break

            max_request_attempts -= 1
