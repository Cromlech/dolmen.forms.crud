# -*- coding: utf-8 -*-

import zope.component
import grokcore.component as grok
from dolmen.content import IFactory
from dolmen.forms.crud import IAdding
from zope.app.container.interfaces import IContainer
from zope.app.container.interfaces import INameChooser
from zope.app.container.constraints import checkObject
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable


class Adder(grok.MultiAdapter):
    grok.name('add')
    grok.adapts(IContainer, IHTTPRequest)
    grok.implements(IAdding)
    grok.provides(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context
        self.__name__ = u""
        self.content_name = None


    def traverse(self, name, ignore):
        """See dolmen.content.interfaces.IFactory
        """
        factory = zope.component.queryUtility(IFactory, name)
        
        if factory is None:
            raise NotFound(self.context, name, self.request)

        self.content_name = name
        return zope.component.getMultiAdapter((self, self.request),
                                              name=factory.addform)
        

    def add(self, content):
        """See dolmen.forms.crud.adding.IAdding
        """
        container = self.context
        chooser = INameChooser(container)

        # check precondition
        checkObject(container, self.content_name, content)

        name = chooser.chooseName('', content)
        
        container[name] = content
        return container[name]


    def nextURL(self):
        """See dolmen.forms.crud.adding.IAdding
        """
        return str(zope.component.getMultiAdapter(
            (self.context, self.request), name=u"absolute_url"))
