from . import common
from . import projection
from . import entity
from . import manager

manager.Prototype.define('entity', entity.Entity)
manager.Prototype.define('component', projection.Component)
manager.Prototype.define('projection', projection.Projection)
