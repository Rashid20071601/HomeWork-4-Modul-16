# Импорт библиотек
from fastapi import FastAPI, Path, status, Body, HTTPException
from typing import Annotated, List
from pydantic import BaseModel


# Инициализация приложения
app = FastAPI()
# База данных сообщений
messages_db = []



class Message(BaseModel):
    id: int = None
    text: str


# Получение всех сообщений
@app.get('/')
async def get_all_messages() -> List[Message]:
    return messages_db


# Получение сообщения по ID
@app.get('/message/{message_id}')
async def get_message(message_id: int) -> Message:
    try:
        return messages_db[message_id]
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')


# Создание нового сообщения
@app.post('/message')
async def create_message(message: Message) -> str:
    message.id = len(messages_db)
    messages_db.append(message)
    return 'Message is created!'


# Обновление сообщения
@app.put('/message/{message_id}')
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return 'Message is updated!'
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')

# Удаление сообщения по ID
@app.delete('/message/{message_id}')
async def kill_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f'Message with ID {message_id} is deleted!'
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')


# Удаление всех сообщений
@app.delete('/')
async def kill_all_messages() -> str:
    messages_db.clear()
    return 'All messages is deleted!'
