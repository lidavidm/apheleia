#!/usr/bin/env python3

import apheleia
import apheleia.manager
import apheleia.entity

manager = apheleia.manager.Manager(apheleia.manager.DirectoryBackend('resources/'))
apheleia.common.prototypeable.defaultManager = manager
#proto = manager.load('/entities/character')
apheleia.entity.Entity.prototyper.paths.append('/base/entities')
apheleia.projection.Component.prototyper.paths.append('/base/components')
apheleia.projection.Projection.prototyper.paths.append('/base/projections')
# cls = apheleia.entity.Entity.getKind('character')
#print(cls.__repr__)
#print(repr(cls()))
# compo = manager.load('/components/position')
# proj = manager.load('/projections/sprite')
print(apheleia.projection.Projection.prototyper.listKinds())
print(apheleia.projection.Projection.getKind('sprite'))
print(apheleia.projection.Projection.getKind('sprite')().draw())
print(manager.load("/vehicles/skirmisher"))
# print(proto, proto.create())
# print(dir(proto.create()))
# print(compo.create())
# print(proj.create().draw())
