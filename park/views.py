from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.order_by('id').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'contatos/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    telefone = request.POST.get('telefone')
    #email = request.POST.get('email')

    cont = Contato(nome=nome,sobrenome=sobrenome,telefone=telefone)
    cont.save()

    return redirect ('index')

def remocao(request):
    
    
    if request.method != 'POST':
        
        return render(request, 'contatos/remocao.html')

    contato_id = request.POST.get('contato_id')    
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    telefone = request.POST.get('telefone')
    email = request.POST.get('email')
        
    cont = Contato.objects.get(sobrenome=sobrenome)
    if sobrenome != Contato:
        print('erro')
    cont.delete()

    return redirect ('index')



def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(
            request,
            messages.ERROR,
            'Campo termo não pode ficar vazio.'
        )
        return redirect('index')

    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )

    paginator = Paginator(contatos, 20)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
