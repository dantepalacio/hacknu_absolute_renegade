from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from pydub import AudioSegment
# Create your views here.
from django.conf import settings
import os
import io
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
# from .serializers import AudioUploadSerializer

class ConvertAudioView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        # Проверяем, есть ли аудиофайл в запросе
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio file found'}, status=400)

        
        audio_file = request.FILES['audio']
        

        try:
            # Попробуем прочитать аудиофайл и определить его формат
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_file.read()))
            # audio_segment = AudioSegment.from_file(audio_file)
            print("2222")
            # Конвертируем аудиофайл в MP3
            mp3_audio = io.BytesIO()
            
            audio_segment.export(mp3_audio, format='mp3')

            # Сохраняем MP3 файл в папке media
            media_root = settings.MEDIA_ROOT
            mp3_file_path = os.path.join(media_root, 'converted_audio.mp3').replace("\\", "/")

            with open(mp3_file_path, 'wb+') as destination:
                destination.write(mp3_audio.getvalue())

            # Возвращаем URL для скачивания
            mp3_file_url = os.path.join(settings.MEDIA_URL, 'converted_audio.mp3')
            return Response({'audio_url': mp3_file_url})

        except CouldntDecodeError:
            return Response({'error': 'Could not decode audio file'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

