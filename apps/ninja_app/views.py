from django.shortcuts import render, redirect, HttpResponse
from random import randint
from time import gmtime, strftime

# Create your views here.
def index(request):
    session = request.session
    session['my_gold'] = session.get('my_gold',0)
    session['messages'] = session.get('messages',[])
    context = {
        'my_gold' : session['my_gold'],
        'messages'  : session['messages']
    }
    return render(request,'ninja_app/index.html', context)

def process(request):
    session = request.session
    session['my_gold'] = session.get('my_gold',0)
    session['action'] = session.get('action', 0)
    buildings = {
        'farm' : [10,20],
        'cave' : [5,10],
        'house' : [2,5],
        'casino' : [0,50],
    }

    if request.method == 'POST':
        result = ''
        building = request.POST['building']
        if building == 'casino':
            # casino
            session['action'] = randint(0,1)
            amount = randint(buildings['casino'][0],buildings['casino'][1])
            if session['action'] == 0:
                session['my_gold'] += amount
                result = 'Earned'
            elif session['action'] == 1 and session['my_gold'] > 0:
                session['my_gold'] -= amount
                result = 'Lost'
        else:
            amount = randint(buildings[building][0],buildings[building][1])
            result = 'Earned'
            session['my_gold'] += amount
        
        current_time = strftime('%Y/%m/%d %r', gmtime())
        message =  result+' '+str(amount)+' golds from the '+building+'! '+ str(current_time)

        message_list = session['messages']
        print type(message_list)
        message_list.append(message)
        session['messages'] = message_list


    return redirect('/')


def clear_up(request):
    request.session['messages'] = []
    request.session['my_gold'] = 0
    return redirect('/')