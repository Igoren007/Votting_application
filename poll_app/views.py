from django.db.models import Count
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework import generics
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from poll_app.serializers import *
from .tasks import send_mail_task, make_xls_export


# Create your views here.


def export_xls(request):
    # 3. вьюха не решает задачу генерации и отправки файла на почту;
    # результат из make_xls_export не передается в send_mail_task; все работает за
    # счет того, что файл генерируется по общей маске даты.
    make_xls_export.delay()
    filename = f'Results_{datetime.now().date()}.xls'
    response = FileResponse(open(filename, 'rb'))
    send_mail_task.delay()

    return response


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
                        # 4. смена признака происходит во вьюхах GET, что противоречит
                        # принципам REST; если вьюху не дернуть, признак не сменится???
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
                # 5. что такое агрегация, как ее можно применить здесь?
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
    # 6. нет проверок, что:
    #  - голосование активно;
    #  - не достигнут максимум (если он задан);
    #  - допускается конкурентность.
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
