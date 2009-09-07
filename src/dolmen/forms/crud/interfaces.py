# -*- coding: utf-8 -*-

from zope.schema import Object
from zope.schema.interfaces import IField
from zope.interface import Interface, Attribute
from zope.location.interfaces import ILocation
from zope.configuration.fields import GlobalObject


class IAdding(ILocation):
    """Defines an abstraction layer for the adding mechanism.
    Historically, the interface was located in the zope.app.container.
    """
    context = Attribute("The context of the adding object")
    request = Attribute("The HTTP request")
    content_name = Attribute("Name of the content being added") 


class IFieldUpdate(Interface):
    """Defines a field update adapter. A field update adapter is called
    when an object is updated. It adapts the field itself and the object
    on which it has been modified. It allows high pluggability in forms
    treatments.
    """
    field = Object(
        required = True,
        title = u"The field that has been updated.",
        schema = IField
        )

    object = GlobalObject(
        required = True,
        title = u"The object concerned by the field update.",
        )


class IFieldsCustomization(Interface):
    """Defines a form customization. A form customization is an adapter
    that allows to modify the fields of a form and their rendering.
    """
    context = Attribute("The context of the customized form")
    request = Attribute("The HTTP request")
    form = Attribute("The form object")

    def __call__(self):
        """Returns an instance of IFields, representing the fields that a
        form needs to display.
        """


__all__ = ['IAdding', 'IFieldUpdate', 'IFieldsCustomization']
