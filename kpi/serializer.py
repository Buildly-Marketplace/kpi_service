from rest_framework import serializers
from indicators import models as idm


class IndicatorSerializer(serializers.HyperlinkedModelSerializer):
    indicator_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.Indicator
        fields = '__all__'


class ReportingPeriodSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.ReportingPeriod
        fields = '__all__'


class IndicatorTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.IndicatorType
        fields = '__all__'


class ObjectiveSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.Objective
        fields = '__all__'


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.Level
        fields = '__all__'


class OutcomeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.Outcome
        fields = '__all__'


class IndicatorSortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = idm.IndicatorSort
        fields = '__all__'

