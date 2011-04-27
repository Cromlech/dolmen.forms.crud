# -*- coding: utf-8 -*-

import zope.i18n
import dolmen.content as content
import grokcore.component as grok

from dolmen.forms.base import Form, DISPLAY
from dolmen.forms.crud import actions as formactions, i18n as _
from dolmen.forms.crud.interfaces import IFactoryAdding
from dolmen.forms.crud.utils import getFactoryFields, getObjectFields

from dolmen.forms.base import Actions
from zope.interface import Interface
from zope.location import ILocation
from zope.cachedescriptors.property import CachedProperty
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.i18nmessageid import Message


class Add(Form):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    grok.baseclass()
    grok.title(_(u"Add"))
    grok.name('dolmen.add')
    grok.context(IFactoryAdding)

    @property
    def label(self):
        name = getattr(self.context.factory, 'name', None)
        if name is not None:
            if isinstance(name, Message):
                name = zope.i18n.translate(name, context=self.request)
            return zope.i18n.translate(
                _(u"add_action", default="Add: $name",
                  mapping={'name': name}), context=self.request)
        return 'Add'

    @CachedProperty
    def fields(self):
        return getFactoryFields(
            self, self.context.factory, '__parent__', '__name__')

    @CachedProperty
    def actions(self):
        add = formactions.AddAction(_("Add"), self.context.factory)
        return Actions(add, formactions.CancelAction(_("Cancel")))


class Edit(Form):
    grok.baseclass()
    grok.name('edit')
    grok.title(_(u"Edit"))
    grok.context(ILocation)

    ignoreContent = False
    ignoreRequest = False
    actions = Actions(formactions.UpdateAction(_("Update")),
                      formactions.CancelAction(_("Cancel")))

    @property
    def label(self):
        label = _(u"edit_action", default=u"Edit: $name",
                  mapping={"name": self.context.__name__})
        return zope.i18n.translate(label, context=self.request)

    @CachedProperty
    def fields(self):
        edited = self.getContentData().getContent()
        return getObjectFields(
            self, edited, '__parent__', '__name__')


class Display(Form):
    grok.baseclass()
    grok.title(_(u"View"))
    grok.context(ILocation)

    mode = DISPLAY
    ignoreRequest = True
    ignoreContent = False

    @property
    def label(self):
        dc = IDCDescriptiveProperties(self.context, None)
        if dc is not None and dc.title:
            return dc.title
        return getattr(self.context, '__name__', u'')

    @CachedProperty
    def fields(self):
        displayed = self.getContentData().getContent()
        return getObjectFields(
            self, displayed, '__parent__', '__name__', 'title')


class Delete(Form):
    """A confirmation for to delete an object.
    """
    grok.baseclass()
    grok.title(_(u"Delete"))
    grok.context(ILocation)

    label = _(u"Delete")
    description = _(u"Are you really sure ?")
    actions = Actions(formactions.DeleteAction(_("Delete")),
                      formactions.CancelAction(_("Cancel")))
