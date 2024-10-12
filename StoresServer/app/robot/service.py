from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from model.history import Purchase as PurchaseModel
from model.item import PurchaseItem as PurchaseItemModel
from model.item import StoreItem as StoreItemModel
from model.store import Store as StoreModel
from store.schemes import Store, StoreItem


async def get_user_recommendations(
        store_id: str,
        user_id: str,
        db: sessionmaker[AsyncSession]
) -> list[StoreItem]:
    async with db() as session:
        recommendations = []

        last_purchases = (await session.execute(
            select(StoreItemModel)
            .join(PurchaseItemModel, PurchaseItemModel.store_item_id == StoreItemModel.id)
            .join(PurchaseModel, PurchaseModel.id == PurchaseItemModel.purchase_id)
            .where(
                PurchaseModel.user_id == user_id,
                PurchaseModel.store_id == store_id
            )
            .order_by(PurchaseModel.created_at.desc())
            .limit(2)
        )).all()
        last_purchases = list(map(lambda x: x[0], last_purchases))
        recommendations.extend(last_purchases)

        user_popular_purchases = (await session.execute(
            select(StoreItemModel)
            .join(PurchaseItemModel, StoreItemModel.id == PurchaseItemModel.store_item_id)
            .group_by(StoreItemModel.id)
            .where(
                PurchaseItemModel.purchase_id.in_(
                    select(PurchaseModel.id)
                    .where(
                        PurchaseModel.user_id == user_id,
                        PurchaseModel.store_id == store_id
                    )
                )
            )
            .order_by(func.sum(PurchaseItemModel.count).desc())
            .limit(4)
        )).all()
        user_popular_purchases = list(map(lambda x: x[0], user_popular_purchases))
        recommendations.extend(user_popular_purchases)

        store_popular_purchases = (await session.execute(
            select(StoreItemModel)
            .join(PurchaseItemModel, StoreItemModel.id == PurchaseItemModel.store_item_id)
            .group_by(StoreItemModel.id)
            .where(
                PurchaseItemModel.purchase_id.in_(
                    select(PurchaseModel.id)
                    .where(
                        PurchaseModel.store_id == store_id
                    )
                )
            )
            .order_by(func.sum(PurchaseItemModel.count).desc())
            .limit(2)
        )).all()
        store_popular_purchases = list(map(lambda x: x[0], store_popular_purchases))
        recommendations.extend(store_popular_purchases)

        items_for_recommendations = []
        items_ids = []

        for item in recommendations:
            if item.id in items_ids:
                continue
            else:
                items_for_recommendations.append(StoreItem(
                    id=str(item.id),
                    name=item.name,
                    description=item.description,
                    logo_url=item.logo_url,
                    category=item.category,
                    price_penny=item.price_penny,
                    store_id=str(item.store_id),
                    balance=item.balance
                ))
                items_ids.append(item.id)

        return items_for_recommendations


async def get_store_list(
        ids: list[str],
        db: sessionmaker[AsyncSession]
) -> list[Store]:
    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.id.in_(ids))
        )).scalars().all()

        return list(map(
            lambda x: Store(
                id=str(x.id),
                name=x.name,
                description=x.description,
                logo_url=x.logo_url,
                store_type=x.store_type,
                items=[]
            ),
            stores
        ))
