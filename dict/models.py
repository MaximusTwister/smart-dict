from datetime import datetime

from django.db import models
from django.urls import reverse_lazy
from django.core.files import File
from django.utils import timezone
from slugify import slugify

from dict.google_api.google_tts_api import google_tts_api


class WordCard(models.Model):
    word_foreign = models.CharField(max_length=50, blank=False, unique=True)
    word_native = models.CharField(max_length=50, blank=False)
    context_foreign = models.TextField(max_length=100, blank=True)
    context_native = models.TextField(max_length=100, blank=True)
    word_foreign_audio = models.FileField(upload_to='media/word', blank=True)
    context_foreign_audio = models.FileField(upload_to='media/context', blank=True)
    score = models.IntegerField(default=0)
    dictionary = models.ForeignKey('Dictionary', on_delete=models.SET_NULL, related_name='cards', null=True)
    is_learning = models.BooleanField(default=False)
    last_learn_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.word_foreign

    def get_absolute_url(self):
        return reverse_lazy('card_handle_url', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        print(f'\n*** [Save WordCard Method] kwargs: {kwargs}')
        word_objects = {'word': self.word_foreign, 'context': self.context_foreign}
        audio_objects = {'word': self.word_foreign_audio, 'context': self.context_foreign_audio}
        for word_type, word in word_objects.items():
            print(f'*** [Save WordCard Method] Trying to save: {word} with length: {len(word)}')

            if bool(audio_objects[word_type]) is False and len(word) > 1:
                full_path_temp = google_tts_api(word)
                print(f'*** [Save WordCard Method] Google TTS Created')
            else:
                print(f'*** [Save WordCard Method] Skip Google TTS for this word')
                continue

            file_name = f'{word}.mp3'
            print(f'*** [Save WordCard Method] Saving filename: {file_name}')
            with open(full_path_temp, 'rb') as out:
                if word_type == 'word':
                    self.word_foreign_audio.save(file_name, File(file=out), save=False)
                else:
                    self.context_foreign_audio.save(file_name, File(file=out), save=False)
            print(f'*** [Save WordCard Method] Saved')

        print(f'*** [Save WordCard Method] Save Super')
        super(WordCard, self).save(*args, **kwargs)
        print(f'*** [Save WordCard Method] Save Super Done')

    class Meta:
        ordering = ['-pk']


class Dictionary(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=False, null=True)
    words_to_learn = models.IntegerField(default=20)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Dictionary, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('dict_view_url', kwargs={'slug': self.slug})


class TemporaryWord(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=True)

    def get_absolute_url(self):
        return reverse_lazy('dict_view_url', kwargs={'pk': self.pk})
