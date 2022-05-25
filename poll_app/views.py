from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from poll_app.models import Poll, Votes, Person

# # Create your views here.
from poll_app.serializers import *

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def index(request):

    # s = Votes.objects.values('person_id').annotate(Count('id')).filter(person=3)
    # s = Votes.objects.values('person_id').annotate(Count('id'))
    # s = Votes.objects.values('person_id').annotate(Count('id')).filter(poll=1)
    date_now = datetime.now()


# ________________________________________________________________________
#получаем участников голосования

    fin2 = Poll.objects.get(id=4).persons.all()
    print(fin2)
    # print(fin2)
    # for i in fin2:
    #     print(i.persons.all())

# ________________________________________________________________________

    # ________________________________________________________________________
    # получаем победителей голосования

    fin2 = Poll.objects.get(id=6, is_active=False)
    print(fin2.winner)
    # print(fin2)
    # for i in fin2:
    #     print(i.persons.all())

    # ________________________________________________________________________

    # fin = Poll.objects.filter(date_start__lt=date_now).exclude(date_end__gte=date_now)
    # for i in fin:
    #     s = Votes.objects.filter(poll=i.id).values('person_id').annotate(Count('id'))
    #     if not s:
    #         winner = None
    #         print(f'Poll {i.title}: Winner - {winner}')
    #         Poll.objects.filter(id=i.id).update(is_active=False)
    #     else:
    #         d = {}
    #         for item in s:
    #             d[item['id__count']] = item['person_id']
    #         max_id = max(d)
    #         winner = d[max_id]
    #         print(f'Poll {i.title}: Winner - {winner}')
    #         Poll.objects.filter(id=i.id).update(winner=winner)
    #         Poll.objects.filter(id=i.id).update(is_active=False)


    # active = Poll.objects.filter(date_start__lte=date_now).exclude(date_end__lte=date_now).exclude(is_active=False)
    # for i in active:
    #     s = Votes.objects.filter(poll=i.id).values('person_id').annotate(Count('id'))
    #     #если в таблице нет голосов для этого голосования
    #     if not s:
    #         print(f'Голосование активно {i.title}')
    #     else:
    #         d = {}
    #         # говнокод для поиска максимума
    #         for item in s:
    #             d[item['id__count']] = item['person_id']
    #         max_id = max(d)
    #         if max_id < i.max_vote:
    #             print(f'Голосование активно {i.title}')
    #         else:
    #             winner = d[max_id]
    #             print(f'Poll {i.title}: Winner - {winner}')
    #             Poll.objects.filter(id=i.id).update(winner=winner)
    #             Poll.objects.filter(id=i.id).update(is_active=False)



    # active = Poll.objects.filter(date_start__lt=date_now).exclude(date_end__lte=date_now)

    # print('Active: ', active)
    # pool = Poll.objects.get(id=1)
    # print(pool.persons.all())
    #
    # pools = Poll.objects.select_related('persons').all()
    # print(pools)

    return HttpResponse('123')


class PollAPIView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollActiveAPIView(generics.ListAPIView):
    date_now = datetime.now()
    active = Poll.objects.filter(date_start__lte=date_now).exclude(date_end__lte=date_now).exclude(is_active=False)
    for i in active:
        s = Votes.objects.filter(poll=i.id).values('person_id').annotate(Count('id'))
        #если в таблице нет голосов для этого голосования
        if not s:
            print(f'Голосование активно {i.title}')
        else:
            d = {}
            # говнокод для поиска максимума
            for item in s:
                d[item['id__count']] = item['person_id']
            max_id = max(d)
            if max_id < i.max_vote:
                print(f'Голосование активно {i.title}')
            else:
                winner = d[max_id]
                print(f'Poll {i.title}: Winner - {winner}')
                Poll.objects.filter(id=i.id).update(winner=winner)
                Poll.objects.filter(id=i.id).update(is_active=False)
    queryset = Poll.objects.filter(date_start__lte=date_now).exclude(date_end__lte=date_now).exclude(is_active=False)
    serializer_class = PollSerializer


class PollFinishedAPIView(generics.ListAPIView):
    date_now = datetime.now()
    finished = Poll.objects.filter(date_start__lt=date_now).exclude(date_end__gte=date_now) | Poll.objects.filter(is_active=False)
    for i in finished:
        s = Votes.objects.filter(poll=i.id).values('person_id').annotate(Count('id'))
        if not s:
            winner = None
            print(f'Poll {i.title}: Winner - {winner}')
            Poll.objects.filter(id=i.id).update(is_active=False)
        else:
            d = {}
            for item in s:
                d[item['id__count']] = item['person_id']
            max_id = max(d)
            winner = d[max_id]
            print(f'Poll {i.title}: Winner - {winner}')
            Poll.objects.filter(id=i.id).update(winner=winner)
            Poll.objects.filter(id=i.id).update(is_active=False)
    queryset = finished
    serializer_class = PollSerializer


#голосование за персонажа
@api_view(['POST',])
def add_vote(request):
    serializer = VoteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET',])
def get_winner(request, pk):
    if request.method == 'GET':
        winner = Poll.objects.get(pk=pk).winner
    item_serializer = PersonSerializer(winner, many=False)
    return JsonResponse(item_serializer.data, safe=False)


@api_view(['GET',])
def get_members(request, pk):
    if request.method == 'GET':
        members = Poll.objects.get(pk=pk).persons
    item_serializer = PersonSerializer(members, many=True)
    return JsonResponse(item_serializer.data, safe=False)


#подробная информация о голосовании
class PollAPIViewDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
