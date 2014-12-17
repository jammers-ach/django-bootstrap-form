'''Views for using the django class base views'''
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from inspect import ismethod,isfunction

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class EditObjView(LoginRequiredMixin,View):
    '''Edits an exisiting object'''
    obj_klass = None
    form_klass = None
    template = 'bootstrapform/generic_edit.html'
    ajax_template = 'bootstrapform/generic_edit_ajax.html'
    obj_name = None
    _settings_ovr = {'edit':True}


    def get_extra_settings(self):
        '''Extra settings common to every view'''
        if(self.obj_name == None):
            self.obj_name = self.obj_klass.__name__

        return {'obj_name':self.obj_name}

    def get(self, request,obj_id):
        obj = self.obj_klass.objects.get(id=obj_id)
        form = self.form_klass(instance=obj)
        settings = {'f':form}
        settings.update(self.get_extra_settings())
        settings.update(self._settings_ovr)

        if('ajax' in request.GET and request.GET['ajax'] == 'true'):
            return render(request,self.ajax_template,settings)
        else:
            return render(request,self.template,settings)

    def post(self,request,obj_id):
        obj = self.obj_klass.objects.get(id=obj_id)
        form = self.form_klass(request.POST,request.FILES,instance=obj)
        if(form.is_valid()):
            #Save object but don't commit
            obj = form.save(commit=False)
            #Run pre commit, save and post commit functions
            self.pre_commit(obj)
            obj.save()
            self.post_commit(obj)

            #TODO custom save messages
            messages.success(request,'Saved')
            obj.log_change(request.user,'changed',form)
            form = self.form_klass(instance=obj)

        else:
            messages.error(request,'There was an error in the form')

        settings = {'f':form}
        settings.update(self.get_extra_settings())
        settings.update(self._settings_ovr)

        return render(request,self.template,settings)


    def pre_commit(self,obj):
        '''After form validation, but pre save'''
        pass

    def post_commit(self,obj):
        '''After saving the objct'''
        pass


class NewObjView(EditObjView):
    '''creates a new object'''
    _settings_ovr = {'edit':False}
    redirect_page = ''

    def post(self,request):
        ajax = 'ajax' in request.POST and request.POST['ajax'] == 'true'
        form = self.form_klass(request.POST,request.FILES)
        if(form.is_valid()):
            #Save object but don't commit
            obj = form.save(commit=False)
            #Run pre commit, save and post commit functions
            self.pre_commit(obj)
            obj.save()
            self.post_commit(obj)

            #todo custom save messages
            if(ajax):
                obj.log_creation(request.user,'Added (quickly)',)
            else:
                messages.success(request,'added')
                obj.log_creation(request.user,'Added',)

            if(ajax):
                return HttpResponse('OK\n%d,%s' % (obj.id,obj)) #TODO escape the object here
            else:
                return redirect(reverse(self.redirect_page,kwargs={'obj_id':obj.id}))
        else:
            if(not ajax):
                messages.error(request,'There was an error in the form')
            else:
                print request.POST,form.errors

        settings = {'f':form}
        settings.update(self.get_extra_settings())
        if(ajax):
            return render(request,self.ajax_template,settings)
        else:
            return render(request,self.template,settings)

    def get(self,request):
        form = self.form_klass()
        settings = {'f':form}
        settings.update(self.get_extra_settings())
        settings.update(self._settings_ovr)
        if('ajax' in request.GET and request.GET['ajax'] == 'true'):
            return render(request,self.ajax_template,settings)
        else:
            return render(request,self.template,settings)


def getattr_from_func(obj,attr):
    attr = getattr(obj,attr)

    if(ismethod(attr) or isfunction(attr)):
        return attr()
    else:
        return attr

class TableObjView(EditObjView):
    '''Displays all the objects as a table, with a new button
    '''
    template = 'bootstrapform/generic_list.html'
    ajax_template = 'bootstrapform/generic_list_ajax.html'
    edit_url = ''
    new_url = ''

    filter_res = True
    columns = (('ID','id'),)

    def get_extra_settings(self):
        settings = super(TableObjView,self).get_extra_settings()
        settings['edit_url'] = self.edit_url
        settings['new_url'] = self.new_url

        return settings

    def get(self,request):
        objs = self.get_objects(request)
        heading = self.make_table_heading(request)
        rows = [[obj.id,self.make_table_row(obj)] for obj in objs]

        settings = {'objects':objs,
                    'heading':heading,
                    'rows':rows,
                    'filter':self.filter_res,
                    }

        settings.update(self.get_extra_settings())
        settings.update(self._settings_ovr)
        if('ajax' in request.GET and request.GET['ajax'] == 'true'):
            return render(request,self.ajax_template,settings)
        else:
            return render(request,self.template,settings)




    def get_objects(self,request):
        '''Gets all the objects to put in the gable'''
        return self.obj_klass.objects.order_by('-id')


    def make_table_row(self,obj):
        '''Returns a row of the table for obj (obj)'''
        return [getattr_from_func(obj,x) for x in zip(*self.columns)[1]]

    def make_table_heading(self,request):
        '''Returns the table heading '''
        return zip(*self.columns)[0]
