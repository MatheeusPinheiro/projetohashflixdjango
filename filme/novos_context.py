from .models import Filme


def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[:8]
    return {"lista_filmes_recentes": lista_filmes}


def lista_filmes_alta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[:8]
    return {"lista_filmes_alta": lista_filmes}


def filme_destaque(request):
    filme = Filme.objects.order_by('-data_criacao')[0]
    if filme:
        return {"filme_destaque": filme}
    else:
        filme =  None
        return {"filme_destaque": filme}
    