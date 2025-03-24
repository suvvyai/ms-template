import importlib
import pkgutil

from fastapi import APIRouter

router = APIRouter()

package_name = "app.routers"
package = importlib.import_module(package_name)

routers = []

for _, module_name, _ in pkgutil.iter_modules(package.__path__):  # type: ignore
    module = importlib.import_module(f"{package_name}.{module_name}")
    if "router" in dir(module):
        routers.append(module.router)

for r in routers:
    router.include_router(r)
