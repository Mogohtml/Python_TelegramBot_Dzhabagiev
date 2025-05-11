from telegram.ext import BaseHandler, CommandHandler
from app.handlers.commands import (
    start,
    register_user_handler,
    create_event_handler,
    read_event_handler,
    edit_event_handler,
    delete_event_handler,
    display_event_handler,
    display_event_sorted_handler
)

HANDLERS: tuple[BaseHandler, ...] = (
    CommandHandler("start", start),
    CommandHandler("register_user_handler", register_user_handler),
    CommandHandler("create_event", create_event_handler),
    CommandHandler("read_event", read_event_handler),
    CommandHandler("edit_event", edit_event_handler),
    CommandHandler("delete_event", delete_event_handler),
    CommandHandler("display_events", display_event_handler),
    CommandHandler("sorted_events", display_event_sorted_handler),
)
