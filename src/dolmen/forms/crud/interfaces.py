# -*- coding: utf-8 -*-

from zope.schema import Object
from zope.interface import Interface, Attribute
from cromlech.content import IFactory


class IAdding(Interface):
    """Defines an abstraction layer for the adding mechanism.
    Historically, the interface was located in the `zope.app.container`.
    """
    context = Attribute("The context of the adding object")
    request = Attribute("The HTTP request")

    def add(component):
        """Adds the component in the context.
        """


class IFactoryAdding(IAdding):
    """An IFactoryAdding extends an IAdding by adding the notion of Factory.
    """
    factory = Object(
        missing_value=None,
        title=u"The factory generating the content.",
        schema=IFactory)
