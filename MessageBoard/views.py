from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from MessageBoard.forms import *
from MessageBoard.models import Advertisement
from MessageBoard.filters import *

######################################################################################################################


class AdsListView(ListView):
    template_name = 'advertisement/list.html'
    context_object_name = 'list_ads'
    paginate_by = 2
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = Advertisement.objects.all().order_by('-create_date').select_related('author')
        return queryset


######################################################################################################################


class AdsSearchView(ListView):
    model = Advertisement
    template_name = 'advertisement/search.html'
    ordering = '-create_date'
    context_object_name = 'list_ads'
    paginate_by = 2
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvFilter(self.request.GET, queryset)
        return self.filterset.qs


######################################################################################################################


class AdDetailView(DetailView, CreateView):
    model = Advertisement
    template_name = 'advertisement/ad_detail.html'
    context_object_name = 'ad'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_ad = context.get('ad')
        context['advertisement_comment'] = current_ad.Advertisement_Comment.all()

        if self.request.user.id is None:
            context['current_user_left_reply'] = False
        else:
            context['current_user_left_reply'] = context['advertisement_comment'].filter(author=self.request.user).exists()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('ad_detail', kwargs={'pk': f'{self.object.adv.pk}'})

    def form_valid(self, form, **kwargs):
        repl = form.save(commit=False)
        repl.author = self.request.user
        repl.adv = Advertisement.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


######################################################################################################################


@login_required(login_url='account_login')
def ad_delete_ask(request, pk):
    ad = Advertisement.objects.get(id=pk)
    context = {
        'ad': ad,
        'question': 'Вы уверены, что хотите удалить это объявление?',
    }
    return render(request, template_name='advertisement/ad_delete.html', context=context)


######################################################################################################################


@login_required(login_url='account_login')
def ad_delete_confirm(request, pk):
    Advertisement.objects.get(id=pk).delete()
    return redirect(to='ads_list')


######################################################################################################################


@login_required(login_url='account_login')
def repl_delete_ask(request, pk, repl_pk):
    ad = Advertisement.objects.get(id=pk)
    current_repl = ad.Advertisement_Comment.get(id=repl_pk)
    context = {
        'reply': current_repl,
        'question': 'Вы уверены, что хотите удалить этот отклик?',
    }
    return render(request, template_name='advertisement/reply_delete.html', context=context)


######################################################################################################################
@login_required(login_url='account_login')
def repl_delete_confirm(request, pk, repl_pk):
    ad = Advertisement.objects.get(id=pk)
    ad.Advertisement_Comment.get(id=repl_pk).delete()
    return redirect(to='ad_detail', pk=pk)


######################################################################################################################


@login_required(login_url='account_login')
def repl_approve_and_disapprove(request, pk, repl_pk):
    ad = Advertisement.objects.get(id=pk)
    current_repl = ad.Advertisement_Comment.get(id=repl_pk)

    if not current_repl.is_approved and not current_repl.is_rejected:
        current_repl.approve()
    elif current_repl.is_approved and not current_repl.is_rejected:
        current_repl.disapprove()
    elif not current_repl.is_approved and current_repl.is_rejected:
        current_repl.unreject()
        current_repl.approve()
    return redirect(request.META.get('HTTP_REFERER'))


######################################################################################################################


@login_required(login_url='account_login')
def repl_reject_and_unreject(request, pk, repl_pk):
    ad = Advertisement.objects.get(id=pk)
    current_repl = ad.Advertisement_Comment.get(id=repl_pk)

    if not current_repl.is_rejected and not current_repl.is_approved:
        current_repl.reject()
    elif current_repl.is_rejected and not current_repl.is_approved:
        current_repl.unreject()
    elif not current_repl.is_rejected and current_repl.is_approved:
        current_repl.disapprove()
        current_repl.reject()
    return redirect(request.META.get('HTTP_REFERER'))


######################################################################################################################


class AdCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Advertisement
    form_class = AdvForm
    template_name = 'advertisement/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.pk})


######################################################################################################################


class AdUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Advertisement
    form_class = AdvForm
    template_name = 'advertisement/edit.html'

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.pk})


######################################################################################################################


class ProfileAdsView(ListView):
    template_name = 'advertisement/my_ads.html'
    ordering = '-create_date'
    context_object_name = 'list_ads'
    paginate_by = 2
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        return context

    def get_queryset(self):
        queryset = Advertisement.objects.filter(author=self.request.user)
        self.filterset = ProfileAdvFilter(self.request.GET, queryset)
        return self.filterset.qs


######################################################################################################################


class ProfileRepliesView(ListView):
    template_name = 'advertisement/profile_repls.html'
    ordering = '-create_date'
    context_object_name = 'profile_repls'
    paginate_by = 2
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        return context

    def get_queryset(self):
        queryset = Comment.objects.filter(author=self.request.user)
        self.filterset = ProfileReplyFilter(self.request.GET, queryset)
        return self.filterset.qs


######################################################################################################################
