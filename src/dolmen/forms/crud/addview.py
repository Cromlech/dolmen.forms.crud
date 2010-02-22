# -*- coding: utf-8 -*-

import dolmen.content
import grokcore.component as grok

from dolmen.forms.crud import IFactoryAdding
from zope.component import queryMultiAdapter, queryUtility
from zope.container.constraints import checkObject
from zope.container.interfaces import IContainer, INameChooser
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema.fieldproperty import FieldProperty
from zope.security.interfaces import Unauthorized
from zope.security.management import checkPermission
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.traversing.interfaces import ITraversable


class Adder(grok.MultiAdapter):
    grok.name('add')
    grok.adapts(IContainer, IHTTPRequest)
    grok.implements(IFactoryAdding)
    grok.provides(ITraversable)

    __name__ = u""
    factory = FieldProperty(IFactoryAdding['factory'])

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def traverse(self, name, ignore):
        """See dolmen.content.interfaces.IFactory
        """
        factory = queryUtility(dolmen.content.IFactory, name)

        if factory is not None:
            permission = dolmen.content.require.bind().get(factory.factory)
            if checkPermission(permission, self.context):
                self.factory = factory
                addform = queryMultiAdapter(
                    (self, self.request), name=factory.addform)
                if addform is not None:
                    return addform
            else:
                raise Unauthorized("%r requires the %r permission." %
                                   (factory.factory, permission))
        raise NotFound(self.context, name, self.request)

    def add(self, content):
        """See dolmen.forms.crud.interfaces.IAdding
        """
        container = self.context

        # check precondition
        checkObject(container, '__temporary__', content)

        # choose name in container
        chooser = INameChooser(container)
        name = chooser.chooseName('', content)

        # assign object and returns it
        container[name] = content
        return container.get(name, None)

    def nextURL(self):
        """See dolmen.forms.crud.interfaces.IAdding
        """
        return absoluteURL(self.context, self.request)
