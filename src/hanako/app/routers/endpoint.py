from hanako.app.router import Router
from hanako.app.routers import default, settings

router = Router()
router.include_router(default.router)
router.include_router(settings.router)
