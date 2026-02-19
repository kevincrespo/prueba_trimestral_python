# main.py
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from db import get_db
from models import Incidencia
from auth import router as auth_router
from deps import get_current_user
from fastapi import Depends

app = FastAPI(
    title="FastAPI + Swagger + MySQL (Incidencias)",
    description="Proyecto para la segunda prueba trimestral de Python",
    version="1.0.0"
)

app.include_router(auth_router)

class IncidenciaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    descripcion: str = Field(min_length=1)
    prioridad: str = Field(min_length=1, max_length=20)
    estado: str = Field(min_length=1, max_length=20)

class IncidenciaResponse(IncidenciaCreate):
    # id: int
    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)
    id: int

@app.get("/")
def root():
    return {"ok": True, "mensaje": "API de incidencias lista. Ve a /docs"}

@app.get("/incidencias", response_model=list[IncidenciaResponse])
def listar_incidencias(db: Session = Depends(get_db)):
    return db.query(Incidencia).all()

@app.get("/quien-soy")
def quien_soy(usuario: str = Depends(get_current_user)):
    return {"mensaje": f"Hola {usuario}, estás autenticado"}


# POST PROTTEGIDO
@app.post(
    "/incidencias",
    response_model=IncidenciaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_incidencia(
    data: IncidenciaCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    nueva = Incidencia(
        titulo=data.titulo,
        descripcion=data.descripcion,
        prioridad=data.prioridad,
        estado=data.estado
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
