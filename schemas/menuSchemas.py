from pydantic import BaseModel

class MenuSchema(BaseModel):
    menu_name: str
    menu_icon: str
    menu_url: str
    permissions: str
    

    class Config:
        from_attributes = True