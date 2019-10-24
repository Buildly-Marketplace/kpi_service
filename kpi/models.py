from datetime import timedelta
from decimal import Decimal
import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords


class IndicatorType(models.Model):
    indicator_type = models.CharField(max_length=135, blank=True)
    description = models.TextField(max_length=765, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.UUIDField('Organization UUID', null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.indicator_type) or ''

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(IndicatorType, self).save(*args, **kwargs)


class IndicatorTypeAdmin(admin.ModelAdmin):
    list_display = ('indicator_type','description','create_date','edit_date')
    display = 'Indicator Type'


class Objective(models.Model):
    name = models.CharField(max_length=135, blank=True, help_text="Objective for workflowleve1 to associate with indicator")
    workflowlevel1 = models.UUIDField('WorkflowLevel1 UUID', null=True, blank=True)
    description = models.TextField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.UUIDField('User UUID', null=True, blank=True)

    class Meta:
        ordering = ('workflowlevel1','name')

    def __unicode__(self):
        return '{}'.format(self.name) or ''

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Objective, self).save(*args, **kwargs)


class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('workflowlevel1','name')
    search_fields = ('name','workflowlevel1')
    list_filter = ('workflowlevel1__country__country',)
    display = 'Objectives'


class Outcome(models.Model):
    name = models.CharField(max_length=255, blank=True, help_text="Hoped for Outcome of objective")
    objective = models.ManyToManyField(Objective)
    indicator = models.ForeignKey("Indicator", null=True, on_delete=models.SET_NULL)
    achieved_percent = models.DecimalField(max_digits=20, decimal_places=4,blank=True, null=True, help_text="Percent achieved")
    description = models.TextField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.UUIDField('User UUID', null=True, blank=True)

    class Meta:
        ordering = ('indicator__name','name')

    def __unicode__(self):
        return '{}'.format(self.name) or ''

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Outcome, self).save(*args, **kwargs)


class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('name','indicator__name')
    search_fields = ('name','indicator__name')
    list_filter = ('name',)
    display = 'Outcomes'


class Level(models.Model):
    name = models.CharField(max_length=135, blank=True,help_text="Results framework or general indicator collection or label for level")
    workflowlevel1 = models.UUIDField('WorkflowLevel1 UUID', null=True, blank=True)
    sort = models.IntegerField(default=0)
    organization = models.UUIDField('Organization UUID', null=True, blank=True)
    parent_id = models.IntegerField(default=0)
    global_default = models.BooleanField(default=0)
    description = models.TextField(max_length=765, blank=True)
    color = models.CharField(max_length=135, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.UUIDField('User UUID', null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.name) or ''

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Level, self).save(*args, **kwargs)


class IndicatorManager(models.Manager):
    def get_queryset(self):
        return super(IndicatorManager, self).get_queryset().prefetch_related('workflowlevel1').select_related('sector')


class Indicator(models.Model):

    DIRECTION_INCREASING = 'increasing'
    DIRECTION_DECREASING = 'decreasing'

    DIRECTION_CHOICES = (
        (DIRECTION_INCREASING, 'Increasing'),
        (DIRECTION_DECREASING, 'Decreasing'),
    )

    ACTUAL_FORMULA_AVG = 'average'
    ACTUAL_FORMULA_USER_DEFINED = 'user_defined'

    ACTUAL_FORMULA_CHOICES = (
        (ACTUAL_FORMULA_AVG, 'Average'),
        (ACTUAL_FORMULA_USER_DEFINED, 'User defined'),
    )

    indicator_uuid = models.CharField(max_length=255,verbose_name='Indicator UUID', default=uuid.uuid4, unique=True, blank=True)
    indicator_type = models.ManyToManyField(IndicatorType, blank=True, help_text="If indicator was pulled from a service select one here")
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.SET_NULL, help_text="The results framework level goal, objective etc. for this indicator")
    objectives = models.ManyToManyField(Objective, blank=True,verbose_name="Objective", related_name="obj_indicator", help_text="Internal stated objective")
    outcomes = models.ManyToManyField(Outcome, blank=True, verbose_name="Outcomes", related_name="out_indicator", help_text="Achieved outcomes")
    name = models.CharField(max_length=255, null=False)
    definition = models.TextField(null=True, blank=True, help_text="Descriptive text for broader definiton and goal")
    comments = models.TextField(max_length=255, null=True, blank=True, help_text="")
    workflowlevel1 = models.UUIDField('WorkflowLevel1 UUID', null=True, blank=True)
    key_performance_indicator = models.BooleanField("Key Performance Indicator?", default=False, help_text="Yes/No is this a key measurement for the overall effort")
    create_date = models.DateTimeField(null=True, blank=True, help_text="")
    edit_date = models.DateTimeField(null=True, blank=True, help_text="")
    history = HistoricalRecords()
    notes = models.TextField(max_length=500, null=True, blank=True, help_text="")
    created_by = models.ForeignKey('auth.User', related_name='indicators', null=True, blank=True, on_delete=models.SET_NULL)
    objects = IndicatorManager()
    direction = models.CharField(blank=True, null=True, max_length=15, choices=DIRECTION_CHOICES)
    actuals = models.DecimalField(max_digits=20, decimal_places=4,blank=True, null=True, help_text="Sum of collected datas achieved")
    created_by = models.UUIDField('User UUID', null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        super(Indicator, self).save(*args, **kwargs)


    @property
    def just_created(self):
        if self.create_date >= timezone.now() - timedelta(minutes=5):
            return True
        return False

    @property
    def name_clean(self):
        return self.name.encode('ascii', 'ignore')

    @property
    def objectives_list(self):
        return ', '.join([x.name for x in self.objectives.all()])

    @property
    def indicator_types(self):
        return ', '.join([x.indicator_type for x in self.indicator_type.all()])

    @property
    def levels(self):
        if self.level:
            return self.level.name
        return None

    def __unicode__(self):
        return self.name


class PeriodicTarget(models.Model):
    indicator = models.ForeignKey(Indicator, null=True, blank=False, on_delete=models.SET_NULL)
    period = models.CharField(max_length=255, null=True, blank=True)
    target = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    customsort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.period, self.target)


class IndicatorSort(models.Model):
    workflowlevel1 = models.UUIDField('WorkflowLevel1 UUID', null=True, blank=True)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.SET_NULL)
    sort_array = ArrayField(models.IntegerField('Indicator IDs', blank=True), blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('workflowlevel1', 'level')
        verbose_name = "Indicator Sort"
        verbose_name_plural = "Indicator Sort"

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(IndicatorSort, self).save()

    def __unicode__(self):
        return unicode(self.workflowlevel1)