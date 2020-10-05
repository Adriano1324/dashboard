from app.charts.models import chart as Chart_model
from app.user.validators import User as User_validator
from app.auth.main import authorize_user
from .validators import dashboard as Dashboard_validator
from .models import dashboard as Dashboard_model, chart_on_dashboard
import json
from fastapi import APIRouter, Security
router = APIRouter()


@router.post('/dashboard/create')
async def create_dashboard(dashboard: Dashboard_validator, current_user: User_validator = Security(authorize_user, scopes=['user_auth'])):
    charts = []
    for chart in dashboard.charts:
        new_chart = chart_on_dashboard(
            place_id=chart.place_id,
            chart=Chart_model.objects(owner=current_user, id=chart.chart)[0],
            refresh_time=chart.refresh_time
        )
        charts.append(new_chart)
    new_dashboard = Dashboard_model(
        owner=current_user,
        name=dashboard.name,
        layout_name=dashboard.layout_name,
        charts=charts
    )

    return new_dashboard.save()


@router.get('/my/dashboards')
async def get_my_dashboards(current_user: User_validator = Security(authorize_user, scopes=['user_auth'])):
    return json.loads(Dashboard_model.objects(owner=current_user).to_json())


@router.get('/my/dashboard/{id}')
async def get_my_dashboard(id: str, current_user: User_validator = Security(authorize_user, scopes=['user_auth'])):
    return json.loads(Dashboard_model.objects(id=id, owner=current_user).to_json())


@router.patch('/my/dashboard/update/{id}')
async def update_my_dashboard(id: str, dashboard: Dashboard_validator, current_user: User_validator = Security(authorize_user, scopes=['user_auth'])):
    tmp = {k: v for k, v in dashboard.dict().items() if v is not None}

    charts = []
    for chart in dashboard.charts:
        new_chart = chart_on_dashboard(
            place_id=chart.place_id,
            chart=Chart_model.objects(owner=current_user, id=chart.chart)[0],
            refresh_time=chart.refresh_time
        )
        charts.append(new_chart)
    tmp['charts']=charts
    updated_dashboard = Dashboard_model.objects(id=id, owner=current_user)
    updated_dashboard.update(**tmp)
    return json.loads(updated_dashboard.to_json())
