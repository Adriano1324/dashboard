from pydantic import BaseModel
from typing import List
class chart_on_dashboard(BaseModel):
    place_id:str
    chart:str
    refresh_time:int

class dashboard(BaseModel):
    name:str
    layout_name:str
    charts:List[chart_on_dashboard]