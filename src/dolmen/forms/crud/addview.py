# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.content import IFactory
from dolmen.forms.crud import IAdding
from zope.component import queryMultiAdapter, queryUtility
from zope.publisher.interfaces import NotFound
from zope.traversing.interfaces import ITraversable
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.container.constraints import checkObject
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.container.interfaces import IContainer, INameChooser


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
        factory = queryUtility(IFactory, name)
        
        if factory is not None:
            self.content_name = name
            addform = queryMultiAdapter((self, self.request),
                                        name=factory.addform)
            if addform is not None:
                return addform
            
        raise NotFound(self.context, name, self.request)
        

    def add(self, content):
        """See dolmen.forms.crud.interfaces.IAdding
        """
        container = self.context

        # check precondition
        checkObject(container, self.content_name, content)

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
