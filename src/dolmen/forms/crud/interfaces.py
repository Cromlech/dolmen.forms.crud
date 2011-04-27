# -*- coding: utf-8 -*-

from zope.schema import Object
from zope.location.interfaces import ILocation
from zope.interface import Interface, Attribute
from zope.component.interfaces import IFactory


class IAdding(ILocation):
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
    See `dolmen.content.IFactory` definition for more information.
    """
    factory = Object(
        missing_value=None,
        title=u"The factory generating the content.",
        schema=IFactory)


class IFieldsCustomization(Interface):
    """Defines a form customization. A form customization is an adapter
    that allows to modify the fields of a form and their rendering.
    """
    context = Attribute("The context of the customized form")
    request = Attribute("The HTTP request")
    form = Attribute("The form object")

    def __call__(fields):
        """Must returns an instance of z3c.form.Fields or a modified
        versions of the original fields arg.
        """
