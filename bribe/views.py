from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from bribe.models import Report,Tag
from django.contrib import auth
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required


class ReportForm(ModelForm):                                                # Create the form class.
    class Meta:
        model = Report


#view for the user page for submitting messages
#def user(request):
#	return render_to_response('user.html')

'''
#submission of messages by users
def submit(request):
    if request.method == 'POST':
        report = request.POST['report']
        tags = request.POST['tags'].split(',')
        value_a = 'a' in tags
        value_b = 'b' in tags
        value_c = 'c' in tags
        value_d = 'd' in tags
        value_e = 'e' in tags
    temp = Report(report = report, passed='', a=value_a, b= value_b,c = value_c, d= value_d, e=value_e)
    temp.save()
    return render_to_response('submit.html', {'report':report,'tags':tags})
'''


'''
def moderator(user):
    user_profile = user.get_profile()
    pref_tags = str(user_profile.preferences).split(',')
    print "pref_tags:", pref_tags
    tag_object_list = Tag.objects.filter(tagname__in=pref_tags)
    print "tag_object_list",tag_object_list
    user_relevant_reports = Report.objects.filter(tag__in=tag_object_list)
    print "user_relevant_reports",list(set(user_relevant_reports))

    #TODO: Return that report which has a review_status = 'False'
    # Without loss of generality I can assume the first report in the Queryset to be returned to the user.
    selected_report = list(set(user_relevant_reports))[0]

    # Creating a form so that the user is able to update the report status (or even change a report where necessary)
    report_update_form = ReportForm(instance=selected_report)

    return render_to_response('moderator.html', {'report': selected_report,'report_form':report_update_form})


def logina(request):
	return render_to_response('login.html')

def login1(request):
    if request.method=="POST":
        print request.user
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return(moderator(user))
        else:
            return HttpResponseRedirect("/logina/")
    else:
        return moderator(request.user)
'''


@login_required
def moderator_view(request):
    user = request.user
    user_profile = user.get_profile()

    if request.method != 'POST':                                            #presenting a message to the moderator
        pref_tags = str(user_profile.preferences).split(',')                #moderator preferences
        print "pref_tags:", pref_tags
        tag_object_list = Tag.objects.filter(tagname__in=pref_tags)         #list of tagged objects
        print "tag_object_list",tag_object_list
        user_relevant_reports = list(set(Report.objects.filter(
                                        tag__in=tag_object_list,
                                    review_status = False)))                #list of reports that can be presented to the moderator
        print "user_relevant_reports",user_relevant_reports

                                                                            # Return that report which has a review_status = 'False'
                                                                            # Without loss of generality I can assume the first report
                                                                            # the Queryset will be returned to the user.
        try:
            selected_report = user_relevant_reports[0]                      # message to be given to the moderator
                                                                            # Creating a form so that the moderator is able to update the report
                                                                            # status (or even change a report where necessary)
            report_update_form = ReportForm(instance=selected_report)
            request.session['selected_report'] = selected_report            #session to be used during updating a message by the moderator.

        except IndexError:                                                  # if no message is available according to the moderator's choice
            selected_report = None
            report_update_form = None

        return render_to_response('moderator.html',
                                 {'report': selected_report,
                                  'report_form':report_update_form})
    else:
        selected_report = request.session['selected_report']
        form = ReportForm(request.POST,instance = selected_report)          # A form bound to the POST data
        if form.is_valid():                                                 # All validation rules pass
            report_obj = form.save(commit = False)
            report_obj.save()
#           return HttpResponseRedirect('/mhome/')                          # Redirect after POST
        return HttpResponseRedirect('/mhome/')                              # Redirect after POST
