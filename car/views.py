from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from django.views.generic import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse


# Create your views here.


@login_required
def addcar(request):
    if request.method == 'POST':
        form = forms.CarForm(request.POST)
        if form.is_valid():
            messages.success(request,'Car Add Successfully')
            form.save()
            return redirect('homepage')
    else:
        form = forms.CarForm()
    return render(request,'addcar.html',{'form':form})


class DetailViewOfCar(DetailView):
    model = models.CarModel
    pk_url_kwarg = 'pk'
    template_name = 'car_detail.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form = forms.CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context




@login_required    
def buynow(request,id):  
    one_car = models.CarModel.objects.get(pk=id) 
    if request.user: 
        order_history = models.Cart( 
            car_name=one_car.car_name, 
            car_description=one_car.description, 
            car_price=one_car.car_price, 
            car_brand=one_car.car_brand_name, 
            car_image=one_car.image, 
            user=request.user, 
        ) 
        if(one_car.quantity==0):
            messages.success(request,'This Car is Out Of Stock Buy Another One')
        else:
            messages.success(request,'Add Cart Successfully')
            order_history.save()
            one_car.quantity -=1
    one_car.save()
    return redirect('homepage')
    

@login_required
def profile(request,id):
    data = models.Cart.objects.filter(user=request.user)
    print(data)
    return render(request,'profile.html',{'data':data})






@login_required
def updateprofile(request):
    if request.method == 'POST':
        profile_form = forms.UserChangeForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('updateprofile')
    else:
        profile_form = forms.UserChangeForm(instance = request.user)
    return render(request, 'update_profile.html',{'form' : profile_form, 'type' : 'Update Profile'})


    


@login_required
def passchange1(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(request.user, data = request.POST)
        if pass_form.is_valid():
            pass_form.save()
            messages.success(request,'Password Updated successfully')
            update_session_auth_hash(request, pass_form.user)
            return redirect('profile')
    else:
        pass_form = PasswordChangeForm(request.user)
    return render(request, 'pass_change.html',{'form' : pass_form, 'type' : 'Using Old Password Change The Password : '})
    


 