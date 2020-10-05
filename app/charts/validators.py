from pydantic import BaseModel
from typing import List, Optional

class datasets(BaseModel):
    label : str
    column_name : str
    background_color : List[ str ]
    border_color : List[ str ]
    border_width : float


class chart_data(BaseModel):
    database : str
    query : str
    labels_column_name : str
    datasets : List[ datasets ]

class labels(BaseModel):
    fontColor : str
    fontSize : int

class legend(BaseModel):
    position : str
    align : str
    display : bool
    labels : labels

class title(BaseModel):
    display : bool
    position : str
    text : str

class chart_options(BaseModel):
    legend : legend
    title : title


class chart(BaseModel):
    name : str
    typ : str
    data : chart_data
    options : chart_options




class Update_datasets(BaseModel):
    label : Optional[ str ] 
    column_name : Optional[ str ]
    background_color : Optional[ List[ str ] ]
    border_color : Optional[ List [ str ] ]
    border_width : Optional[ float ] 


class Update_chart_data(BaseModel):
    database : Optional[ str ] 
    query : Optional[ str ] 
    labels_column_name : Optional[ str ] 
    datasets : Optional [ List[ Update_datasets ] ]

class Update_labels(BaseModel):
    fontColor : Optional[ str ]
    fontSize : Optional[ int ]

class Update_legend(BaseModel):
    position : Optional[ str ] 
    align : Optional[ str ]
    display : Optional[ bool ] 
    labels : Optional[ Update_labels ]

class Update_title(BaseModel):
    display : Optional[ bool ]
    position : Optional[ str ] 
    text : Optional[ str ] 

class Update_chart_options(BaseModel):
    legend : Optional[ Update_legend ]
    title : Optional[ Update_title ]


class Update_chart(BaseModel):
    name : Optional[ str ]
    typ : Optional[ str ]
    data : Optional[ Update_chart_data ]
    options : Optional[ Update_chart_options ]