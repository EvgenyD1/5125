import crud
import fastapi
import models
import schema
from constants import STATUS_SUCCESS_RESPONSE
from dependencies import SessionDependency
from lifespan import lifespan

app = fastapi.FastAPI(
    title="Test Application", version="0.0.1", description="...", lifespan=lifespan
)


@app.get("/v1/advertisement/{advertisement_id}", response_model=schema.GetAdvResponse)
async def get_adv(advertisement_id: int, session: SessionDependency):
    adv = await crud.get_item(session, models.Adv, advertisement_id)
    return adv.dict


@app.get("/v1/advertisement")
async def get_adv_by_qs(session: SessionDependency, title: str = None,
                        description: str = None, price: str = None, creator: str = None):
    advs = await crud.get_item_by_qs(session, title, description, price, creator)
    return advs


@app.post("/v1/advertisement", response_model=schema.CreateAdvResponse)
async def create_adv(adv_json: schema.CreateAdvRequest, session: SessionDependency):
    adv = models.Adv(**adv_json.dict())
    adv = await crud.add_item(session, adv)
    return adv.id_dict


@app.patch("/v1/advertisement/{advertisement_id}", response_model=schema.UpdateAdvResponse)
async def update_todo(
    advertisement_id: int, adv_json: schema.UpdateAdvRequest, session: SessionDependency
):

    adv = await crud.get_item(session, models.Adv, advertisement_id)
    adv_patch = adv_json.dict(exclude_unset=True)
    for field, value in adv_patch.items():
        setattr(adv, field, value)
    await crud.add_item(session, adv)
    return adv.id_dict


@app.delete("/v1/advertisement/{advertisement_id}", response_model=schema.DeleteAdvResponse)
async def delete_adv(advertisement_id: int, session: SessionDependency):
    await crud.delete_item(session, models.Adv, advertisement_id)
    return STATUS_SUCCESS_RESPONSE
