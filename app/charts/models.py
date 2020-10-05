from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ReferenceField,
    StringField,
    ListField,
    FloatField,
    BooleanField,
    IntField,
    ListField,
    QuerySet
    )
from app.databases.models import Database
from app.user.models import User
from sqlalchemy import create_engine

import json
import pandas as pd

class Chart_query(QuerySet):
    
    def get_data(self):
        
        choices={
            'postgres':'postgresql+pg8000',
            'mysql':'mysql+mysqlconnector'
        }
        self = self[0]
        engine = create_engine(
                '{type}://{user}:{password}@{server}/{database}'.format(
                    type= choices[self.data.database.typ],
                    user=self.data.database.user, 
                    password=self.data.database.password, 
                    server=self.data.database.server,
                    database=self.data.database.database),
                 pool_recycle=3600)
        data = engine.execute(self.data.query)
        df = pd.DataFrame(data.fetchall())
        df.columns = data.keys()
        datasets = []
        for dataset in self.data.datasets:
            new = {
                'label':dataset.label,
                'data': df[dataset.column_name].tolist(),
                'backgroundColor': dataset.background_color if len(dataset.background_color)>1 else dataset.background_color[0],
                'borderColor': dataset.border_color if len(dataset.border_color)>1 else dataset.border_color[0],
                'borderWidth': dataset.border_width
            }
            datasets.append(new)
        result = {
            'type': self.typ,
            'data':{
                'labels':df[self.data.labels_column_name].tolist(),
                'datasets':datasets
            },
            'options':json.loads(self.options.to_json())
        }
        return result


class datasets(EmbeddedDocument):
    
    label = StringField(default="label")
    column_name = StringField()
    background_color = ListField()
    border_color = ListField()
    border_width = FloatField()


class chart_data(EmbeddedDocument):
    database = ReferenceField(Database)
    query = StringField()
    labels_column_name = StringField()
    datasets = ListField(EmbeddedDocumentField(datasets))

class labels(EmbeddedDocument):
    fontColor = StringField(default='black')
    fontSize = IntField(default=12)

class legend(EmbeddedDocument):
    position = StringField(default='top')
    align = StringField(default= 'center')
    display = BooleanField(default= True)
    labels = EmbeddedDocumentField(labels)


class title(EmbeddedDocument):
    display = BooleanField(default=True)
    position = StringField(default="top")
    text = StringField(default="CHART")




class chart_options(EmbeddedDocument):
    legend = EmbeddedDocumentField(legend)
    title = EmbeddedDocumentField(title)


class chart(Document):
    owner = ReferenceField(User)
    name = StringField(default='My chart')
    typ = StringField(default='bar')
    data = EmbeddedDocumentField(chart_data)
    options = EmbeddedDocumentField(chart_options)
    meta = {'queryset_class': Chart_query}

