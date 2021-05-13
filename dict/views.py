import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import CreateView, DetailView, FormView

from .models import Dictionary, WordCard, TemporaryWord
from .forms import DictForm, NewCardForm
from .utils import get_random_card, update_word_card_with_data, set_cards_initial_state
from dict.google_api.google_translate_api import translate_text


class IndexView(View):
    def get(self, request):
        context = {'temp_words': TemporaryWord.objects.all(), 'form': NewCardForm}
        return render(request, 'dict/index.html', context=context)


class CardNew(View):
    def post(self, request, *args, **kwargs):
        print(f'\n=== Card New KWARGS: {kwargs}')
        update_result = update_word_card_with_data(request=request, kwargs=kwargs)
        if update_result is True:
            return JsonResponse({'result': True}, status=200)
        else:
            return JsonResponse({'result': False}, status=200)


class DictLearnView(View):
    def get(self, request, *args, **kwargs):
        print(f'\n=== Dict Learn View GET KWARGS: {kwargs}')
        if kwargs.get('pk') == 0:
            set_cards_initial_state(kwargs)
            random_card_to_learn = get_random_card()
            return render(request, 'dict/index.html', {'card_to_learn': random_card_to_learn})
        else:
            return render(request, 'dict/index.html', {'card_to_learn': WordCard.objects.get(pk=kwargs['pk'])})

    def post(self, request, *args, **kwargs):
        print(f'\n=== Dict Learn View POST KWARGS: {kwargs}')
        update_word_card_with_data(request=request, kwargs=kwargs)
        random_card_to_learn = get_random_card()
        return HttpResponse(json.dumps({'addr': random_card_to_learn.pk}))


class DictView(FormView, DetailView):
    slug = None
    model = Dictionary
    form_class = NewCardForm
    template_name = 'dict/dict_view.html'
    context_object_name = 'dict_view'

    def get_context_data(self, **kwargs):
        context = super(DictView, self).get_context_data(**kwargs)
        context['form'] = NewCardForm
        return context

    def post(self, request, *args, **kwargs):
        print(f'=== Dict View POST KWARGS: {kwargs}')
        updated_post = request.POST.copy()

        dict_obj = Dictionary.objects.get(slug=kwargs['slug'])
        # updated_post.update({'dictionary': dict_obj})
        print(f'=== Dict View POST: {updated_post}')

        form = NewCardForm(updated_post)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.dictionary = dict_obj
            new_card.save()
            return redirect('dict_view_url', kwargs['slug'])
        else:
            print(form.errors)
            print('=== Dict View POST Error Validation')

    def get_success_url(self, *args, **kwargs):
        print(f'=== Get Success URL: {args} {kwargs} {self.slug}')
        return reverse_lazy('dict_view_url', kwargs={'slug': self.slug})


class DictNew(CreateView):
    form_class = DictForm
    template_name = 'dict/dict_new.html'


class CardHandle(View):
    def post(self, request, *args, **kwargs):
        print(f'\n=== Card Handle KWARGS: {kwargs}')
        update_result = update_word_card_with_data(request=request, kwargs=kwargs)
        if update_result is True:
            return JsonResponse({'result': True}, status=200)
        else:
            return JsonResponse({'result': False}, status=200)


@ensure_csrf_cookie
def bot_handler(request):
    if request.method == 'GET':
        print(f'\n=== Bot Word GET Request')
        temp_words = TemporaryWord.objects.all()
        return JsonResponse(serializers.serialize('json', temp_words), safe=False)

    if request.method == 'POST':
        print(f'\n=== Bot Word POST')
        print(f'=== Bot Word Json: {request.body.decode("utf-8")}')
        json_dict = json.loads(request.body.decode('utf-8'))
        print(f'=== Bot Word JsonDict: {json_dict}')
        TemporaryWord.objects.create(title=json_dict['word'])
        return JsonResponse({'result': True}, status=200)


class EditBotWord(View):
    def get(self, request, *args, **kwargs):
        print(f'\n=== Edit Bot Word KWARGS: {kwargs}')
        word = TemporaryWord.objects.get(pk=kwargs['pk'])

        if kwargs['mode'] == 'del':
            print(f'\n=== Delete Bot Word : {word}')
        elif kwargs['mode'] == 'save':
            print(f'\n=== Save Bot Word : {word}')
            word_foreign = word.title
            word_native = translate_text(target='ru', text=word_foreign)
            dict_obj = Dictionary.objects.get(pk=3)
            WordCard.objects.create(word_foreign=word_foreign, word_native=word_native, dictionary=dict_obj)
        else:
            print(f'\n=== Edit Bot Word WRONG ARGUMENTS: {kwargs}')
            return redirect('index_url')

        word.delete()
        return redirect('index_url')
