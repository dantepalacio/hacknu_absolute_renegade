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

class ChattyBotConsumer(AsyncWebsocketConsumer):
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
        # Получаем сообщение от клиента
        text_data_json = json.loads(text_data)
        
        message = text_data_json['message']
        audio_blob = text_data_json.get("audio")
        print(text_data_json)

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
            message = None
        else:
            audio_bytes = None
    

        answer = ''
        # Обрабатываем сообщение, например, отправляем его обратно клиенту
        await self.send(text_data=json.dumps({
            'message': answer
        }))