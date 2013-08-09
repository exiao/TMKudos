import datetime
from haystack import indexes
from kudosapp.models import Kudos, Employee


class KudosIndex(indexes.SearchIndex, indexes.Indexable):
    """
    from_employee = models.ForeignKey('employee', related_name='sent_kudos')
    to_employee = models.ForeignKey('employee', related_name='received_kudos')
    created = models.DateTimeField(default=datetime.datetime.now())
    subject = models.CharField(max_length=511)
    body = models.TextField()
    flagged = models.BooleanField(default=False)
    tags = models.CharField(max_length=50, null=True, blank=True)
    """

    text = indexes.CharField(document=True, use_template=True)
    from_employee = indexes.CharField(model_attr='from_employee')
    to_employee = indexes.CharField(model_attr='to_employee')
    subject = indexes.CharField(model_attr='subject')
    body = indexes.CharField(model_attr='body')
    tags = indexes.CharField(model_attr='tags')
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Kudos

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())
