from fastapi import HTTPException
from models import ORM_CLS, ORM_OBJECT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def add_item(session: AsyncSession, item: ORM_OBJECT) -> ORM_OBJECT:
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == "23505":
            raise HTTPException(status_code=409, detail="Item already exists")
        raise err
    return item


async def get_item(session: AsyncSession, orm_cls: ORM_CLS, item_id: int) -> ORM_OBJECT:
    orm_obj = await session.get(orm_cls, item_id)
    if orm_obj is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return orm_obj


async def get_item_by_qs(session: AsyncSession, title: str | None,
                         description: str | None, price: str | None, creator: str | None):
    sql_str = 'SELECT * from advertisement'
    flag = 0
    if title:
        sql_str += f" WHERE title = '{title}'"
        flag = 1
    if description:
        if flag == 0:
            sql_str += f" WHERE description LIKE '%{description}%'"
        else:
            sql_str += f" AND description LIKE '%{description}%'"
        flag = 1
    if price:
        price = float(price)
        if flag == 0:
            sql_str += f' WHERE price = {price}'
        else:
            sql_str += f' AND price = {price}'
        flag = 1
    if creator:
        if flag == 0:
            sql_str += f" WHERE creator = '{creator}'"
        else:
            sql_str += f" AND creator = '{creator}'"
    sql = text(sql_str)
    orm_objects = await session.execute(sql)
    orm_objects_dict = orm_objects.mappings().all()
    if not orm_objects_dict:
        raise HTTPException(status_code=404, detail="Item not found")
    return orm_objects_dict


async def delete_item(session: AsyncSession, orm_cls: ORM_CLS, item_id) -> None:
    orm_obj = await get_item(session, orm_cls, item_id)
    await session.delete(orm_obj)
    await session.commit()
