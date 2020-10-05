from mongoengine import (
    Document, 
    QuerySet,
    StringField,
    ListField,
    ReferenceField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField)

from app.charts.models import chart
from app.user.models import User
class dashboard_query(QuerySet):
    pass

class chart_on_dashboard(EmbeddedDocument):
    place_id = StringField()
    chart = ReferenceField(chart)
    refresh_time = IntField(default=0)


class dashboard(Document):
    owner = ReferenceField(User)
    name = StringField(default='Dashboard')
    layout_name = StringField(default='Default_layout')
    charts = ListField(EmbeddedDocumentField(chart_on_dashboard))
