# -*- coding: utf-8 -*-

import zope.schema
import megrok.layout
import dolmen.content
import grokcore.component as grok
from zope.interface import Interface
from zope.container.constraints import contains
from zope.dublincore.property import DCProperty

class IDesertWorm(dolmen.content.IContent):
    """Defines a gigantic worm living in the desert.
    """
    length = zope.schema.Float(
        title=u"Size of worm from head to tails in meters",
        default=300.0,
        required=True,
        )


class IDesertWarrior(dolmen.content.IContent):
    """Defines a warrior living in the desert.
    """
    water = zope.schema.Int(
        title=u"Number water gallons owned",
        default=1,
        required=True,
        )

class IDesertWarrior(dolmen.content.IContent):
    """Defines a warrior living in the desert.
    """
    title = DCProperty('title')
    water = zope.schema.Int(
        title=u"Number water gallons owned",
        default=1,
        required=True,
        )


class IDesertCave(dolmen.content.IContent):
    """Defines a cave carved in the mountains by the Coriolis storms.
    """
    contains(IDesertWarrior, IDesertWorm)


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
    
    We support Dublin Core
    """
    zope.implements(IAnnotatable) # to use default DCproperty handling
    dolmen.content.name(u'Fremen Warrior')
    dolmen.content.schema(IDesertWarrior)
    dolmen.content.factory(TrainingCamp)
    dolmen.content.require('zope.ManageContent')
    
class ShaiHulud(dolmen.content.Content):
    """Gigantixc desert worm of Arrakis
    """
    dolmen.content.name(u'Shai Hulud')
    dolmen.content.schema(IDesertWorm)
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
