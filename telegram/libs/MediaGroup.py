# -*- coding: utf-8 -*-
from .Send import Send


class MediaGroup(Send):

    def send(
        self,
        document_paths: list,
        caption: str = None,
        media_type: str = 'document',
        parse_mode: str = None
    ):
        """
        :param parse_mode: HTML, Markdown, MarkdownV2
        :param document_paths:
        :param caption:
        :param media_type: types: 'photo', 'video', 'audio', 'document', 'voice', 'animation'
        :return:
        """
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD

        if not document_paths:
            return self.send_message(f"No files to send. {caption if caption else ''}", out_msg=True)

        if caption and len(caption) > self.__MAX_CAPTCHA_LENGTH:
            document_paths.append(self.msg.make_massage_doc(caption, 'caption.txt'))

        _max_attempts = self.max_request_attempts

        while _max_attempts > 0:
            files, media = {}, []
            for doc_path in document_paths:
                files[basename(doc_path)] = open(self.msg.prepare_documents(doc_path), 'rb')
                media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))

            media[-1]['caption'] = self.msg.prepare_caption(caption) if caption is not None else ''
            media[-1]['parse_mode'] = _parse_mod

            media_group_data = {'chat_id': self.requests.auth.chat_id, 'media': dumps(media)}

            if self.requests.post('sendMediaGroup', data=media_group_data, files=files):
                break

            _max_attempts -= 1
