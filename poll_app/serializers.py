from rest_framework import serializers

from poll_app.models import Poll, Votes, Person


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('__all__')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ('__all__')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('__all__')
