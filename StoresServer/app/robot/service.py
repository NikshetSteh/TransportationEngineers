from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from model.history import Purchase as PurchaseModel
from model.item import PurchaseItem as PurchaseItemModel
from model.item import StoreItem as StoreItemModel
from store.schemes import StoreItem


async def get_user_recommendations(
        store_id: str,
        user_id: str,
        db: sessionmaker[AsyncSession]
) -> list[StoreItem]:
    async with db() as session:
        recommendations = []

        last_purchases = (await session.execute(
            select(PurchaseModel).where(
                PurchaseModel.user_id == user_id,
                PurchaseModel.store_id == store_id
            ).order_by(PurchaseModel.created_at.desc()).limit(1)
        )).one_or_none()
        if last_purchases is not None:
            last_purchases_items = (await session.execute(
                select(PurchaseItemModel).where(
                    PurchaseItemModel.purchase_id == last_purchases.id
                )
            )).scalars().all()

            recommendations.extend(last_purchases_items)

        user_popular_purchases = (await session.execute(
            select([PurchaseItemModel.store_item, func.count(PurchaseItemModel.store_item_id).label('count')])
            .where(
                PurchaseItemModel.purchase_id == select([PurchaseModel.id]).where(PurchaseModel.user_id == user_id)
            )
            .group_by(PurchaseItemModel.store_item_id)
            .order_by(func.count(PurchaseItemModel.store_item_id).desc())
            .limit(4)
        )).all()
        user_popular_purchases = list(map(lambda x: x[0], user_popular_purchases))
        recommendations.extend(user_popular_purchases)

        store_popular_purchases = (await session.execute(
            select([PurchaseItemModel.store_item_id, func.count(PurchaseItemModel.store_item_id).label('count')])
            .where(
                PurchaseItemModel.purchase_id == select([PurchaseModel.id]).where(PurchaseModel.store_id == store_id)
            )
            .group_by(PurchaseItemModel.store_item_id)
            .order_by(func.count(PurchaseItemModel.store_item_id).desc())
            .limit(2)
        )).all()
        store_popular_purchases = list(map(lambda x: x[0], store_popular_purchases))
        recommendations.extend(store_popular_purchases)

        items_for_recommendations = []
        items_ids = []

        for item in recommendations:
            if item.store_item_id in items_ids:
                continue
            else:
                buffer = (await session.execute(
                    select(StoreItemModel).where(StoreItemModel.id == item.store_item_id)
                )).one_or_none()
                if buffer is not None:
                    items_for_recommendations.append(StoreItem(
                        id=str(buffer[0].id),
                        name=buffer[0].name,
                        description=buffer[0].description,
                        logo_url=buffer[0].logo_url,
                        category=buffer[0].category,
                        price_penny=buffer[0].price_penny,
                        store_id=str(buffer[0].store_id)
                    ))
                    items_ids.append(item.store_item_id)

        return items_for_recommendations
