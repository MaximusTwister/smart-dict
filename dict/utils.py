import json
import os
from itertools import chain

from django.forms.models import model_to_dict
from django.core.files import File

from dict.models import WordCard, Dictionary
from dict.google_api.google_tts_api import google_tts_api


def set_cards_initial_state(kwargs):
    WordCard.objects.filter(is_learning=True).update(is_learning=False)
    all_words = WordCard.objects.filter(dictionary__slug=kwargs['slug'])
    all_words_amount = all_words.count()
    words_to_learn_setting = Dictionary.objects.get(slug=kwargs['slug']).words_to_learn

    print(f'=== All Words: {all_words} -- {all_words_amount}')
    print(f'=== Words to learn Setting: {words_to_learn_setting}')

    conditions = {
        '<40': all_words.filter(score__lte=40),
        '41_30': all_words.filter(score__range=(41, 70)),
        '71_100': all_words.filter(score__range=(71, 100))
    }

    none_qs = WordCard.objects.none()
    qs_list = []

    for condition, filtered in conditions.items():
        if len(filtered) <= 0:
            continue
        for _ in range(int(words_to_learn_setting/3)):
            all_words_amount = all_words.count()
            while all_words_amount > 0:
                obj = filtered.order_by('?')[0]
                print(f'Random object: {obj} -- Condition: {condition}')
                all_words_amount -= 1
                if obj not in qs_list:
                    qs_list.append(obj)
                    obj.is_learning = True
                    obj.save()
                    break
                else:
                    continue

    final_qs = list(chain(none_qs, qs_list))
    print(f"QS list: {qs_list} -- Final QS: {final_qs}")


def get_random_card():
    print('\n=== Get Random Card Function')
    obj = WordCard.objects.filter(is_learning=True).order_by('?')[0]
    print(f'=== Random Card to Return: {obj}')
    return obj


def clean_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    print(f'\n=== [Clean Kwargs] Model: {model}')
    print(f'=== [Clean Kwargs] Fields: {model_fields}')
    return {k: v for k, v in arg_dict.items() if k in model_fields}


def update_word_card_with_data(request, kwargs):
    print(f'\n=== [Update Word Card] KWARGS: {kwargs}')
    print(f'=== [Update Word Card] Json: {request.body.decode("utf-8")}')
    new_data = json.loads(request.body.decode('utf-8'))
    new_data.setdefault('word_id', kwargs['pk'])
    print(f'=== [Update Word Card] JsonDict: {new_data}')

    if new_data.get('set_initial', None) is not False:
        print('=== [Update Word Card] GET STATE: <CLEAR CARDS>')
        set_cards_initial_state(kwargs)

    new_data_clean = clean_kwargs(WordCard, {k: v for (k, v) in new_data.items() if v is not None})
    print(f'=== [Update Word Card] Clean New Data : {new_data_clean}')

    old_data = model_to_dict(WordCard.objects.get(pk=new_data['word_id']))
    print(f"=== [Update Word Card] Old Data: {old_data}")
    new_data_clean_diff = dict(set(new_data_clean.items()) - set(old_data.items()))
    print(f'=== [Update Word Card] Save to DB: {new_data_clean_diff} -- {len(new_data_clean_diff)}')

    if len(new_data_clean_diff) == 0:
        print(f'=== [Update Word Card] Nothing to Save')
        return True

    title_to_audio_type = {'word_foreign': 'word_foreign_audio', 'context_foreign': 'context_foreign_audio'}
    for word_title, audio_title in title_to_audio_type.items():
        obj = WordCard.objects.get(pk=new_data['word_id'])
        if word_title not in new_data_clean_diff.keys():
            continue

        try:
            if word_title == 'word_foreign':
                old_file_path = obj.word_foreign_audio.path
                new_data_clean_diff['word_foreign_audio'] = ''
            elif word_title == 'context_foreign':
                old_file_path = obj.context_foreign_audio.path
                new_data_clean_diff['context_foreign_audio'] = ''
            else:
                old_file_path = None
            print(f'=== [Update Word Card] Delete Old Audio: {audio_title} => {old_file_path}')
            os.remove(old_file_path)
            print(f'=== [Update Word Card] Old Audio was Deleted')
        except (ValueError, FileNotFoundError) as e:
            print(f'=== [Update Word Card] Error: {e}')

    WordCard.objects.filter(pk=new_data['word_id']).update(**new_data_clean_diff)
    WordCard.objects.get(pk=new_data['word_id']).save()
    print('=== [Update Word Card] Done')
    return True
