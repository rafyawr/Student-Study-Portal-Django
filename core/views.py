from django.shortcuts import render, redirect
from youtubesearchpython import VideosSearch
from .models import ToDo, Notes, Homework
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'core/home.html')

def home(request):
    return render(request, 'home.html')


from youtubesearchpython import VideosSearch

def youtube_view(request):
    if request.method == 'POST':
        text = request.POST.get('search', '')

        # Always trust the user's input — no modification
        video_search = VideosSearch(text, limit=10)
        results = video_search.result().get('result', [])

        result_list = []
        for i in results:
            result_dict = {
                'title': i.get('title'),
                'duration': i.get('duration'),
                'thumbnail': i.get('thumbnails', [{}])[0].get('url'),
                'channel': i.get('channel', {}).get('name'),
                'link': i.get('link'),
                'views': i.get('viewCount', {}).get('short'),
                'published': i.get('publishedTime'),
                'description': ''.join([desc.get('text', '') for desc in i.get('descriptionSnippet', [])]) if i.get('descriptionSnippet') else ''
            }
            result_list.append(result_dict)

        context = {
            'results': result_list,
            'search_text': text,  # send back user input to display on page
        }
        return render(request, 'youtube.html', context)

    else:
        return render(request, 'youtube.html')




@login_required
def notes(request):
    notes = Notes.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Notes.objects.create(user=request.user, title=title, description=description)
            return redirect('notes') 

    context = {
        'notes': notes,
    }
    return render(request, 'notes.html', context)



def note_detail(request, pk):
    note = Notes.objects.get(pk=pk, user=request.user)

    context ={
        "note":note
    }

    return render(request, 'notes-details.html', context)


def delete_note(request, pk):
    note = Notes.objects.get(pk=pk, user=request.user)
    note.delete()
    return redirect('notes')


@login_required
def homework(request):
    homeworks = Homework.objects.filter(user=request.user)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due = request.POST.get('due')
        is_finished = request.POST.get('is_finished') == 'on'  # Checkbox

        if subject and title and description and due:
            Homework.objects.create(
                user=request.user,
                subject=subject,
                title=title,
                description=description,
                due=due,
                is_finished=is_finished
            )
            return redirect('homework')

    context = {
        'homeworks': homeworks
    }
    return render(request, 'homework.html', context)



def delete_homework(request, homework_id):
    homework = Homework.objects.get(id=homework_id, user=request.user)
    homework.delete()
    return redirect('homework')


def dictionary_view(request):
    input_word = None
    phonetics = None
    definition = None
    example = None
    audio = None

    input_word = None
    word_data = None

    if request.method == 'POST':
        input_word = request.POST.get('word')
        if input_word:
            api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{input_word}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    word_data = data[0]

    context = {
        'input': input_word,
        'word_data': word_data,
    }
    return render(request, 'dictionary.html', context)

def wikipedia_view(request):
    if request.method == 'POST':
        text = request.POST.get('search_query')
        if text:
            try:
                search_results = wikipedia.search(text)
                if search_results:
                    # Take the first best match
                    page = wikipedia.page(search_results[0])
                    context = {
                        'title': page.title,
                        'link': page.url,
                        'details': page.summary
                    }
                else:
                    context = {'error_message': 'No results found. Try another query.'}
            except wikipedia.exceptions.DisambiguationError as e:
                context = {'error_message': f"Your search query is too vague. Suggestions: {e.options}"}
            except wikipedia.exceptions.PageError:
                context = {'error_message': "Page not found. Try refining your query."}
        else:
            context = {'error_message': 'Please enter a search query.'}
    else:
        context = {}

    return render(request, 'wikipedia.html', context)


@login_required
def todo(request):
    todos = ToDo.objects.filter(user=request.user)
    todos_done = todos.filter(is_finished=True)
    return render(request, 'todo.html', {'todos': todos, 'todos_done': todos_done})

def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        ToDo.objects.create(user=request.user, title=title)
    return redirect('todo')

def delete_todo(request, todo_id):

    if request.method == 'POST':
        todo = ToDo.objects.get(id=todo_id, user=request.user)
        todo.delete()
    return redirect('todo')


def conversion(request):
    if request.method == 'POST':
        measurement = request.POST.get('measurement')
        
        if measurement == 'length':
            input = True
            measure1 = request.POST.get('measure1')
            measure2 = request.POST.get('measure2')
            input_value = request.POST.get('input')
            answer = ''
            if input_value and int(input_value) >= 0:
                if measure1 == 'yard' and measure2 == 'foot':
                    answer = f'{input_value} yard = {int(input_value) * 3} foot'
                elif measure1 == 'foot' and measure2 == 'yard':
                    answer = f'{input_value} foot = {int(input_value) / 3} yard'
            context = {'answer': answer, "input": input, "measurement":measurement}
            return render(request, 'conversion.html', context)

        if measurement == 'mass':
            input = True
            measure1 = request.POST.get('measure1')
            measure2 = request.POST.get('measure2')
            input_value = request.POST.get('input')
            answer = ''
            if input_value and int(input_value) >= 0:
                if measure1 == 'pound' and measure2 == 'kilogram':
                    answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
                elif measure1 == 'kilogram' and measure2 == 'pound':
                    answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'
            context = {'answer': answer, "input": input, "measurement":measurement}
            return render(request, 'conversion.html', context)
    else:
        return render(request, 'conversion.html', {'input':False})

def books(request):
    if request.method == 'GET' and 'book_name' in request.GET:
        book_name = request.GET['book_name']
        results = search_books(book_name)
    else:
        results = []  

    context = {
        'results': results,
    }
    return render(request, 'books.html', context)

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])

        results = []
        for item in items:
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'Unknown Title')
            subtitle = volume_info.get('subtitle', '')
            description = volume_info.get('description', 'No description available.')
            thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
            categories = volume_info.get('categories', [])
            pageCount = volume_info.get('pageCount', '')
            averageRating = volume_info.get('averageRating', '')

            book_data = {
                'title': title,
                'subtitle': subtitle,
                'description': description,
                'thumbnail': thumbnail,
                'categories': categories,
                'pageCount': pageCount,
                'averageRating': averageRating,
                'preview': volume_info.get('previewLink', ''),
            }
            results.append(book_data)
        
        return results
    else:
        return [] 
    







