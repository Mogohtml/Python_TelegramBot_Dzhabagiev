import logging

from telegram.ext import Application as PTBApplication, ApplicationBuilder

from app.core.repositories.events import EventRepository
from app.core.repositories.users import UserRepository
from app.core.services.event_service import EventService
from app.core.services.user_service import UserService

from app.handlers import HANDLERS
from app.infra.postgres.db import Database
from settings.config import AppSettings


class Application(PTBApplication):
    user_service: UserService  # Add type annotation
    event_service: EventService  # Add type annotation

    def __init__(self, app_settings: AppSettings, **kwargs):
        super().__init__(**kwargs)
        self._settings = app_settings
        self.database = Database(app_settings.POSTGRES_DSN)
        self._register_handlers()

        event_repository = EventRepository(database=self.database)
        self.event_service = EventService(repository=event_repository)

        user_repository = UserRepository(database=self.database)
        self.user_service = UserService(repository=user_repository)

    @staticmethod
    async def initialize_dependencies(application: "Application") -> None:
        await application.database.initialize()


    @staticmethod
    async def shutdown_dependencies(application: "Application") -> None:
        await application.database.shutdown()

    def run(self) -> None:
        self.run_polling()

    def _register_handlers(self):
        for handler in HANDLERS:
            self.add_handler(handler)

def configure_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

def create_app(app_settings: AppSettings) -> Application:
    application = (ApplicationBuilder()
                   .application_class(Application, kwargs={"app_settings": app_settings})
                   .post_init(Application.initialize_dependencies)    # type: ignore[arg-type]
                   .post_shutdown(Application.shutdown_dependencies)  # type: ignore[arg-type]
                   .token(app_settings.TELEGRAM_API_KEY.get_secret_value()).build())
    return application # type: ignore[return-value]

def main():
    configure_logging()
    settings = AppSettings()
    app = create_app(settings)
    app.run()

if __name__ == '__main__':
    main()
