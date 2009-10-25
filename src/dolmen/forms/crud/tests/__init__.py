# -*- coding: utf-8 -*-

import zope.schema
import megrok.layout
import dolmen.content
import grokcore.component as grok
from zope.interface import Interface
from zope.app.container.constraints import contains


class IDesertWarrior(dolmen.content.IBaseContent):
    """Defines a warrior living in the desert.
    """
    water = zope.schema.Int(
        title = u"Number water gallons owned",
        default = 1,
        required = True
        )


class IDesertCave(dolmen.content.IBaseContent):
    """Defines a cave carved in the mountains by the Coriolis storms.
    """
    contains(IDesertWarrior)


class Sietch(dolmen.content.Container):
    """A grotto located on Arrakis.
    """
    dolmen.content.name('sietch')
    dolmen.content.schema(IDesertCave)
    dolmen.content.nofactory()
    

class TrainingCamp(dolmen.content.Factory):
    """A camp that produces Fremen warriors.
    """
    dolmen.content.name(u"fremen")
    title = u"Fremen training camp"


class Fremen(dolmen.content.Content):
    """Inhabitants on the deep deserts. They live in sietches.
    """
    dolmen.content.name(u'Fremen Warrior')
    dolmen.content.schema(IDesertWarrior)
    dolmen.content.factory(TrainingCamp)
    dolmen.content.require('zope.ManageContent')


class Harkonnen(dolmen.content.Content):
    """A native of Giedi Prime.
    """
    dolmen.content.name('Harkonnen')
    dolmen.content.nofactory()


class MyLayout(megrok.layout.Layout):
    grok.context(Interface)

    def render(self):
        return self.view.content()
