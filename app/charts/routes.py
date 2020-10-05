from fastapi import APIRouter, Security

import json

from app.auth.main import get_current_active_user
from app.user.validators import User as User_validator
from app.databases.models import Database as Database_model
from .validators import chart as Chart_validator, Update_chart
from .models import chart as chart_model, chart_data, datasets, chart_options, legend, labels, title
router = APIRouter()


@router.get('/charts/my')
async def My_charts(current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    return json.loads(chart_model.objects(owner=current_user).to_json())


@router.get('/chart/my/{id}')
async def My_chart(id: str, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    return json.loads(chart_model.objects(id=id, owner=current_user).to_json())


@router.get('/chart/data/{id}')
async def get_chart_data(id: str, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    return chart_model.objects(id=id, owner=current_user).get_data()


@router.post('/chart/create')
async def create_chart(chart: Chart_validator, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    dataset_list = []
    for dataset in chart.data.datasets:
        new_dataset = datasets(
            label=dataset.label,
            column_name=dataset.column_name,
            background_color=dataset.background_color,
            border_color=dataset.border_color,
            border_width=dataset.border_width
        )
        dataset_list.append(new_dataset)

    db = Database_model.objects(owner=current_user, id=chart.data.database)
    new_chart = chart_model(
        name=chart.name,
        owner=current_user,
        typ=chart.typ,
        data=chart_data(
            database=db[0],
            query=chart.data.query,
            labels_column_name=chart.data.labels_column_name,
            datasets=dataset_list
        ),
        options=chart_options(
            legend=legend(
                position=chart.options.legend.position,
                align=chart.options.legend.align,
                display=chart.options.legend.display,
                labels=labels(
                    fontColor=chart.options.legend.labels.fontColor,
                    fontSize=chart.options.legend.labels.fontSize
                )
            ),
            title=title(
                display=chart.options.title.display,
                position=chart.options.title.position,
                text=chart.options.title.text
            )
        )
    )
    new_chart.save()
    return new_chart.to_json()


@router.post('/chart/watch')
async def watch_chart(chart: Chart_validator, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    dataset_list = []
    for dataset in chart.data.datasets:
        new_dataset = datasets(
            label=dataset.label,
            column_name=dataset.column_name,
            background_color=dataset.background_color,
            border_color=dataset.border_color,
            border_width=dataset.border_width
        )
        dataset_list.append(new_dataset)

    db = Database_model.objects(owner=current_user, id=chart.data.database)
    new_chart = chart_model(
        name=chart.name,
        owner=current_user,
        typ=chart.typ,
        data=chart_data(
            database=db[0],
            query=chart.data.query,
            labels_column_name=chart.data.labels_column_name,
            datasets=dataset_list
        ),
        options=chart_options(
            legend=legend(
                position=chart.options.legend.position,
                align=chart.options.legend.align,
                display=chart.options.legend.display,
                labels=labels(
                    fontColor=chart.options.legend.labels.fontColor,
                    fontSize=chart.options.legend.labels.fontSize
                )
            ),
            title=title(
                display=chart.options.title.display,
                position=chart.options.title.position,
                text=chart.options.title.text
            )
        )
    )
    tmp = new_chart.save()
    tmp = chart_model.objects(id=new_chart.id)
    try:
        result = tmp.get_data()
    except Exception as e:
        print(e)
        tmp.delete()
    finally:
        tmp.delete()
    return result


@router.patch("/chart/update/{id}")
async def update_user(id: str, chart: Update_chart, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    tmp = {k: v for k, v in chart.dict().items() if v is not None}
    dataset_list = []
    try:
        for dataset in chart.data.datasets:
            new_dataset = datasets(
                label=dataset.label,
                column_name=dataset.column_name,
                background_color=dataset.background_color,
                border_color=dataset.border_color,
                border_width=dataset.border_width
            )
            dataset_list.append(new_dataset)
        tmp['data']['datasets'] = dataset_list
    except Exception as e:
        pass
    try:
        db = Database_model.objects(owner=current_user, id=chart.data.database)
        tmp['data']['database'] = db[0]
    except Exception as e:
        pass
    updated_chart = chart_model.objects(id=id, owner=current_user)
    updated_chart.update(**tmp)
    return json.loads(updated_chart.to_json())


@router.delete("/chart/delete/{id}")
async def delete_chart(id: str, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    return chart_model.objects(id=id, owner=current_user).delete()
