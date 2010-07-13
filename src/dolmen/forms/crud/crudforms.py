# -*- coding: utf-8 -*-

import zope.i18n
import dolmen.content as content
import zeam.form.ztk as form
import grokcore.component as grok

from dolmen.forms.base import ApplicationForm, DISPLAY
from dolmen.forms.crud import actions as formactions, i18n as _
from dolmen.forms.crud.interfaces import IFactoryAdding, IFieldsCustomization
from dolmen.forms.crud.utils import queryClassMultiAdapter

from zeam.form.base import Fields, Actions
from zope.cachedescriptors.property import CachedProperty
from zope.component import queryMultiAdapter
from zope.i18nmessageid import Message


class Add(ApplicationForm):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    grok.baseclass()
    grok.title(_(u"Add"))
    grok.name('dolmen.add')
    grok.context(IFactoryAdding)

    submissionError = None

    @property
    def label(self):
        name = self.context.factory.name
        if isinstance(name, Message):
            name = zope.i18n.translate(name, context=self.request)
        return zope.i18n.translate(
            _(u"add_action", default="Add: $name",
              mapping={'name': name}), context=self.request)

    @CachedProperty
    def fields(self):
        ifaces = self.context.factory.getSchema()
        fields = Fields(*ifaces).omit('__parent__')

        modifier = queryClassMultiAdapter(
            (self.context.factory.factory, self, self.request),
            self.context, IFieldsCustomization)

        if modifier is not None:
            return modifier(fields)
        return fields

    @CachedProperty
    def actions(self):
        add = formactions.AddAction(_("Add"), self.context.factory)
        return Actions(add, formactions.CancelAction(_("Cancel")))


class Edit(ApplicationForm):
    grok.baseclass()
    grok.name('edit')
    grok.title(_(u"Edit"))
    grok.context(content.IBaseContent)

    ignoreContent = False
    ignoreRequest = False
    actions = Actions(formactions.UpdateAction(_("Update")),
                      formactions.CancelAction(_("Cancel")))

    submissionError = None

    @property
    def label(self):
        label = _(u"edit_action", default=u"Edit: $name",
                  mapping={"name": self.context.title})
        return zope.i18n.translate(label, context=self.request)

    @CachedProperty
    def fields(self):
        iface = content.schema.bind().get(self.context)
        fields = Fields(*iface).omit('__parent__')
        modifier = queryMultiAdapter(
            (self.context, self, self.request), IFieldsCustomization)

        if modifier is not None:
            return modifier(fields)
        return fields


class Display(ApplicationForm):
    grok.baseclass()
    grok.title(_(u"View"))
    grok.context(content.IBaseContent)

    mode = DISPLAY
    ignoreRequest = True
    ignoreContent = False

    @property
    def label(self):
        return self.context.title

    @CachedProperty
    def fields(self):
        iface = content.schema.bind().get(self.context)
        fields = form.Fields(*iface).omit('__parent__', 'title')
        modifier = queryMultiAdapter(
            (self.context, self, self.request), IFieldsCustomization)

        if modifier is not None:
            return modifier(fields)
        return fields


class Delete(ApplicationForm):
    """A confirmation for to delete an object.
    """
    grok.baseclass()
    grok.title(_(u"Delete"))
    grok.context(content.IBaseContent)

    label = _(u"Delete")
    description = _(u"Are you really sure ?")
    submissionError = None
    actions = Actions(formactions.DeleteAction(_("Delete")),
                      formactions.CancelAction(_("Cancel")))
