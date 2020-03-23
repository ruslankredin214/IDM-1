from ...objects import dp, MySignalEvent
from ...utils import new_message, edit_message

@dp.my_signal_event_handle('+шаб')
def create_template(event: MySignalEvent) -> str:

    if ((event.payload == '' or event.payload == None) and len(event.attachments) == 0) or len(event.args) == 0:
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Нет данных")
            return "ok"

    name = " ".join(event.args)
    data = event.payload

    for temp in event.db.templates:
        if temp['name'] == name:
            event.db.templates.remove(temp)
            event.db.save()
            
    event.db.templates.append(
        {
            "name":name,
            "payload":data,
            "attachments":event.attachments
        }
    )
    event.db.save()
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"✅ Шаблон \"{name}\" добавлен")
    return "ok"


@dp.my_signal_event_handle('-шаб')
def remove_template(event: MySignalEvent) -> str:
        
    if len(event.args) == 0:
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Нет данных")

    name = " ".join(event.args)

    for temp in event.db.templates:
        if temp['name'] == name:
            event.db.templates.remove(temp)
            event.db.save()
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"✅Шаблон \"{name}\" удален.")
            return "ok"
    
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"❗ У вас нет такого \"{name}\" шаблона")
    return "ok"


@dp.my_signal_event_handle('шабы')
def templates(event: MySignalEvent) -> str:

    _message = "🗓 Мои шаблоны:"
    itr = 0
    for temp in event.db.templates:
        itr += 1
        _message += f"\n{itr}. {temp['name']}"

    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=_message)
    return "ok"

@dp.my_signal_event_handle('шаб')
def run_template(event: MySignalEvent) -> str:
    
    if len(event.args) == 0:
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Нет данных")

    name = " ".join(event.args)

    for temp in event.db.templates:
        if temp['name'] == name:
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message=temp['payload'], attachment=",".join(temp['attachments']))
            return "ok"
    
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"❗ У вас нет такого \"{name}\" шаблона")
    return "ok"
