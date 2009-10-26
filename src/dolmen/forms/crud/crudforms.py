# -*- coding: utf-8 -*-

import grokcore.security as grok

import dolmen.content as content
import dolmen.forms.base as form
from dolmen.forms.crud import utils, interfaces as crud

from zope.event import notify
from zope.i18nmessageid import MessageFactory
from zope.security.interfaces import Unauthorized
from zope.security.management import checkPermission
from zope.component import queryMultiAdapter, getUtility
from zope.cachedescriptors.property import CachedProperty
from zope.lifecycleevent import Attributes, ObjectCreatedEvent

_ = MessageFactory("dolmen")


class Add(form.PageAddForm):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    grok.baseclass()
    grok.name('dolmen.add')
    grok.context(crud.IFactoryAdding)

    form_name = _(u"Add")

    @property
    def label(self):
        return self.context.factory.title

    @CachedProperty
    def fields(self):
        ifaces = self.context.factory.getSchema()
        fields = form.Fields(*ifaces).omit('__parent__')
        
        modifier = utils.queryClassMultiAdapter(
            (self.context.factory.factory, self, self.request),
            self.context,
            crud.IFieldsCustomization
            )

        if modifier is not None:
            return modifier(fields)
        return fields

    def nextURL(self):
        return self.context.nextURL()

    def createAndAdd(self, data):
        obj = self.create(data)
        self.add(obj)
        return obj

    def add(self, object):
        return self.context.add(object)

    def create(self, data):
        obj = self.context.factory()
        utils.notify_object_creation(self.fields, obj, data)
        return obj

    @form.button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            self.redirect(self.url(obj))


class Edit(form.PageEditForm):
    grok.baseclass()
    grok.context(content.IBaseContent)
    form.extends(form.PageEditForm, ignoreButtons=True)
    
    form_name = _(u"Edit")

    @property
    def label(self):
        return _(u"edit_action", default=u"Edit: $name",
                 mapping={"name": self.context.title})

    def nextURL(self):
        return self.url(self.context)

    @CachedProperty
    def fields(self):
        iface = content.schema.bind().get(self.context)
        fields = form.Fields(*iface).omit('__parent__')
        modifier = queryMultiAdapter(
            (self.context, self, self.request),
            crud.IFieldsCustomization
            )
        if modifier is not None:
            return modifier(fields)
        return fields

    def nextURL(self):
        return self.redirect(self.url(self.context))

    @form.button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = form.apply_data_event(self.fields, self.context, data)
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage
        self.redirect(self.nextURL())


class Display(form.PageDisplayForm):
    grok.baseclass()
    grok.context(content.IBaseContent)

    ignoreContext = False

    @property
    def label(self):
        return self.context.title

    @CachedProperty
    def fields(self):
        iface = content.schema.bind().get(self.context)
        fields = form.Fields(*iface).omit('__parent__', 'title')
        modifier = queryMultiAdapter(
            (self.context, self, self.request),
            crud.IFieldsCustomization
            )
        if modifier is not None:
            return modifier(fields)
        return fields
