import json
import random
import traceback
import uuid
from asyncio import AbstractEventLoop
from uuid import UUID

from aio_pika import connect_robust, IncomingMessage, Message
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.models.recommendation import Recommendation
from app.models.user import User
from app.settings import settings
from app.services.book_catalog_service import BookCatalogService
from app.services.recommendation_service import RecommendationService

from app.repositories.bd_books_repo import BookRepo


async def send_new_recommendation(rec: Recommendation):
    print(f'Sending recommendation... {rec.json()}')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()

    message_body = json.dumps(rec.json())
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='uzorov_update_queue'
    )
    # Close the channel and connection
    await channel.close()
    await connection.close()


async def process_new_recommendation(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        user_id = data['user_id']

        book_catalog_service = BookCatalogService()  # Создаем экземпляр сервиса
        books = book_catalog_service.get_books()
        rec_book = random.choice(books)

        recommendation_service = RecommendationService()

        rec = recommendation_service.create_recommendation(user_id=user_id, recommended_book_id=rec_book.id)

        await send_new_recommendation(rec=rec)
    except:
        traceback.print_exc()
    finally:
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    new_book_queue = await channel.declare_queue('uzorov_update_queue', durable=True)

    await new_book_queue.consume(process_new_recommendation)

    print('Started RabbitMQ consuming for the library...')
    return connection
