from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    date_now = datetime.now().date()
    # print(type(date_now))


# ________________________________________________________________________
#получаем участников голосования

    # fin2 = Poll.objects.get(id=4).persons.all()
    # print(fin2)
    # print(fin2)
    # for i in fin2:
    #     print(i.persons.all())

# ________________________________________________________________________

    # ________________________________________________________________________
    # получаем победителей голосования

    # fin2 = Poll.objects.get(id=6, is_active=False)
    # print(fin2.winner)
    # print(fin2)
    # for i in fin2:
    #     print(i.persons.all())

    # ________________________________________________________________________

    # fin = Poll.objects.filter(date_start__lt=date_now).exclude(date_end__gte=date_now)
    # fin = Poll.objects.filter(date_end__lt=date_now)
    # print(fin)
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


    polls = Poll.objects.all()
    finished_polls = []
    for poll in polls:
        if poll.is_active == False:
            finished_polls.append(poll)
        else:
            if date_now > poll.date_end:
                votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
                if not votes:
                    winner = None
                    Poll.objects.filter(id=poll.id).update(winner=winner)
                else:
                    d = {}
                    for item in votes:
                        d[item['id__count']] = item['person_id']
                    max_id = max(d)
                    winner = d[max_id]
                    # print(f'Poll {poll.title}: Winner - {winner}')
                    Poll.objects.filter(id=poll.id).update(winner=winner)
                    # Poll.objects.filter(id=i.id).update(is_active=False)
                finished_polls.append(poll)
                Poll.objects.filter(id=poll.id).update(is_active=False)
            else:
                votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
                if votes:
                    d = {}
                    # говнокод для поиска максимума
                    for item in votes:
                        d[item['id__count']] = item['person_id']
                    max_id = max(d)
                    if max_id >= poll.max_vote:
                        winner = d[max_id]
                        # print(f'Poll {poll.title}: Winner - {winner}')
                        finished_polls.append(poll)
                        Poll.objects.filter(id=poll.id).update(is_active=False)
                        Poll.objects.filter(id=poll.id).update(winner=winner)
    print(finished_polls)


#получить победителя
    # poll = Poll.objects.get(id=7)
    # if poll.is_active == False:
    #     if poll.winner:
    #         winner = poll.winner
    #     else:
    #         votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
    #         if not votes:
    #             winner = None
    #             Poll.objects.filter(id=poll.id).update(winner=winner)
    #         else:
    #             d = {}
    #             for item in votes:
    #                 d[item['id__count']] = item['person_id']
    #             max_id = max(d)
    #             winner = d[max_id]
    #             Poll.objects.filter(id=poll.id).update(winner=winner)
    # else:
    #     if poll.date_start < date_now <= poll.date_end:
    #         votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
    #         #если в таблице нет голосов для этого голосования
    #         if votes:
    #             d = {}
    #             # говнокод для поиска максимума
    #             for item in votes:
    #                 d[item['id__count']] = item['person_id']
    #             max_id = max(d)
    #             if max_id >= poll.max_vote:
    #                 winner = d[max_id]
    #                 Poll.objects.filter(id=poll.id).update(is_active=False)
    #                 Poll.objects.filter(id=poll.id).update(winner=winner)
    #
    # print(f'winner ---- {winner}')


        # s = Votes.objects.filter(poll=i.id).values('person_id').annotate(Count('id'))
        # if not s:
        #     winner = None
        #     print(f'Poll {i.title}: Winner - {winner}')
        #     Poll.objects.filter(id=i.id).update(is_active=False)
        # else:
        #     d = {}
        #     for item in s:
        #         d[item['id__count']] = item['person_id']
        #     max_id = max(d)
        #     winner = d[max_id]
        #     print(f'Poll {i.title}: Winner - {winner}')
        #     Poll.objects.filter(id=i.id).update(winner=winner)
        #     Poll.objects.filter(id=i.id).update(is_active=False)


    #
    # polls = Poll.objects.all()
    # print(polls)
    # active_polls = []
    # for poll in polls:
    #     if poll.date_start < date_now <= poll.date_end:
    #         votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
    #         #если в таблице нет голосов для этого голосования
    #         if not votes:
    #             active_polls.append(poll)
    #         else:
    #             d = {}
    #             # говнокод для поиска максимума
    #             for item in votes:
    #                 d[item['id__count']] = item['person_id']
    #             max_id = max(d)
    #             if max_id < poll.max_vote:
    #                 active_polls.append(poll)
    #             else:
    #                 Poll.objects.filter(id=poll.id).update(is_active=False)
    # print(active_polls)



    # active = Poll.objects.filter(date_start__lte=date_now).exclude(date_end__gte=date_now).exclude(is_active=False)
    # active = Poll.objects.filter(date_end__gte=date_now).exclude(date_start__gt=date_now).exclude(is_active=False)
    # print(active)
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
    date_now = datetime.now().date()
    polls = Poll.objects.all()
    active_polls = []
    for poll in polls:
        if poll.is_active != False:
            if poll.date_start < date_now <= poll.date_end:
                votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
                #если в таблице нет голосов для этого голосования
                if not votes:
                    active_polls.append(poll)
                else:
                    d = {}
                    # говнокод для поиска максимума
                    for item in votes:
                        d[item['id__count']] = item['person_id']
                    max_id = max(d)
                    if max_id < poll.max_vote:
                        active_polls.append(poll)
                    else:
                        winner = d[max_id]
                        Poll.objects.filter(id=poll.id).update(is_active=False)
                        Poll.objects.filter(id=poll.id).update(winner=winner)


    queryset = active_polls
    serializer_class = PollSerializer


class PollFinishedAPIView(generics.ListAPIView):
    date_now = datetime.now().date()
    polls = Poll.objects.all()
    finished_polls = []
    for poll in polls:
        if poll.is_active == False:
            finished_polls.append(poll)
        else:
            if date_now > poll.date_end:
                votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
                if not votes:
                    winner = None
                    Poll.objects.filter(id=poll.id).update(winner=winner)
                else:
                    d = {}
                    for item in votes:
                        d[item['id__count']] = item['person_id']
                    max_id = max(d)
                    winner = d[max_id]
                    Poll.objects.filter(id=poll.id).update(winner=winner)
                finished_polls.append(poll)
                Poll.objects.filter(id=poll.id).update(is_active=False)
            else:
                votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
                if votes:
                    d = {}
                    # говнокод для поиска максимума
                    for item in votes:
                        d[item['id__count']] = item['person_id']
                    max_id = max(d)
                    if max_id >= poll.max_vote:
                        winner = d[max_id]
                        finished_polls.append(poll)
                        Poll.objects.filter(id=poll.id).update(is_active=False)
                        Poll.objects.filter(id=poll.id).update(winner=winner)

    queryset = finished_polls
    serializer_class = PollSerializer


#голосование за персонажа
@api_view(['POST',])
def add_vote(request):
    serializer = VoteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


#получить победителя голосования
@api_view(['GET',])
def get_winner(request, pk):
    date_now = datetime.now().date()
    poll = Poll.objects.get(id=pk)
    if poll.is_active == False:
        if poll.winner:
            winner = poll.winner
        else:
            votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
            if not votes:
                winner = None
                Poll.objects.filter(id=poll.id).update(winner=winner)
            else:
                d = {}
                for item in votes:
                    d[item['id__count']] = item['person_id']
                max_id = max(d)
                winner = d[max_id]
                Poll.objects.filter(id=poll.id).update(winner=winner)
    else:
        if poll.date_start < date_now <= poll.date_end:
            votes = Votes.objects.filter(poll=poll.id).values('person_id').annotate(Count('id'))
            # если в таблице нет голосов для этого голосования
            if votes:
                d = {}
                # говнокод для поиска максимума
                for item in votes:
                    d[item['id__count']] = item['person_id']
                max_id = max(d)
                if max_id >= poll.max_vote:
                    winner = d[max_id]
                    Poll.objects.filter(id=poll.id).update(is_active=False)
                    Poll.objects.filter(id=poll.id).update(winner=winner)

    item_serializer = PersonSerializer(winner, many=False)
    return JsonResponse(item_serializer.data, safe=False)


#получить участников голосования
@api_view(['GET',])
def get_members(request, pk):
    members = Poll.objects.get(pk=pk).persons
    item_serializer = PersonSerializer(members, many=True)
    return JsonResponse(item_serializer.data, safe=False)


#подробная информация о голосовании
class PollAPIViewDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
