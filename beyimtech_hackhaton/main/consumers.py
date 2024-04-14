from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from asgiref.sync import async_to_sync
from pydub import AudioSegment
import json
import base64
from .openai_api_handler import ApiHandler
from io import BytesIO
import ffmpeg
import os
from .ml_model import model

class ChattyBotConsumer(AsyncWebsocketConsumer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count_message = 0

        self.ml_model = model.LSTM()

    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'chat',
            self.channel_layer
        )
 

    async def receive(self, text_data):
        '''text_data: {"message":str, "audio":blob}
        
        '''
        api_handler = ApiHandler()
        # Получаем сообщение от клиента
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        audio_blob = text_data_json.get("audio")

        if self.count_message == 10:
            self.count_message = 0

            if audio_blob:
                blob_bytes = audio_blob.read()
                mp3_buffer = BytesIO()

                process = (
                    ffmpeg.input('pipe:', format='wav')
                    .output(mp3_buffer, format='mp3')
                    .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, input=blob_bytes)
                )
                process.communicate()
                mp3_data = mp3_buffer.getvalue()

                media_path = os.path.join(settings.MEDIA_ROOT, 'converted_audio.mp3')

                with open(media_path, "wb") as mp3_file:
                    mp3_file.write(mp3_data)
                # Делаем текст None, так как пришло аудио
                transcript_message = api_handler.transcript_text(media_path)

            else:
                audio_bytes = None
                message = text_data_json['message']

            answer = api_handler.get_conclusion()

            conclusion_response_json = api_handler.get_conclusion()
            self.ml_model = model.train(self.ml_model, conclusion_response_json.get("json_salary"))

            salaries, salaries_predicted = model.savedModelForecast(self.ml_model, conclusion_response_json.get("json_salary"))
            await self.send(text_data=json.dumps({
                'message': answer,
                'salaries_real': salaries,
                'salaries_predicted': salaries_predicted,

            }))

        else:
            if audio_blob:
                blob_bytes = audio_blob.read()
                mp3_buffer = BytesIO()

                process = (
                    ffmpeg.input('pipe:', format='wav')
                    .output(mp3_buffer, format='mp3')
                    .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, input=blob_bytes)
                )
                process.communicate()
                mp3_data = mp3_buffer.getvalue()

                media_path = os.path.join(settings.MEDIA_ROOT, 'converted_audio.mp3')

                with open(media_path, "wb") as mp3_file:
                    mp3_file.write(mp3_data)
                # Делаем текст None, так как пришло аудио
                print('QQSDQCWVES ',media_path)
                transcript_message = api_handler.transcript_text(media_path)
                print('!$@%$@$@$', transcript_message)
                answer = api_handler.send_message_to_chat(transcript_message)
            else:
                audio_bytes = None
                message = text_data_json['message']
                answer = api_handler.send_message_to_chat(message)

            self.count_message += 1

        # Обрабатываем сообщение, например, отправляем его обратно клиенту
        await self.send(text_data=json.dumps({
            'message': answer,
        }))
