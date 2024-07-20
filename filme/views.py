from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.views.generic import TemplateView,ListView,DetailView,FormView,UpdateView
from .forms import CriarContaForm, FormHomepage
from filme.models import Filme, Usuario
from django.contrib.auth.mixins import LoginRequiredMixin


class Homepage(FormView):
    template_name = 'home.html'
    form_class = FormHomepage
    
    def get(self, request ,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) #Redireciona para a homepage
        
    def get_success_url(self):
        email = self.request.POST.get('email')
        
        usuarios = Usuario.objects.filter(email = email)
        
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')
    
    
class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    
    
class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    
    def get(self, request, *args, **kwargs):
        #descobrir qual filme o usuario esta acessando
        filme = self.get_object()
        #somar 1 nas visualizações daquele filme 
        filme.visualizacoes+= 1
        #salvar os dados no banco de dados
        filme.save()
        
        return super().get( request, *args, **kwargs) #redireciona o usuário para a url final
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        
        filmes_relacionados = self.model.objects.filter(categoria = self.get_object().categoria)[:5]
        context['filmes_relacionados'] = filmes_relacionados
        
        return context


class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme
    
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains= termo_pesquisa)
            return object_list
        else:
            return None
        # return super().get_queryset()
    

class Paginaperfil(LoginRequiredMixin,UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']
    
    def get_success_url(self):
        return reverse('filme:homefilmes')
    
    
class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm
    
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('filme:login')