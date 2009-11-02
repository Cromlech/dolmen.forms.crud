# -*- coding: utf-8 -*-

import dolmen.content as content
import dolmen.forms.base as form
import grokcore.component as grok

from zope.component import queryMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.crud import utils, interfaces as crud

_ = MessageFactory("dolmen")


class Add(form.PageAddForm):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    grok.baseclass()
    grok.title(_(u"Add"))
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
    grok.title(_(u"Edit"))
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
    grok.title(_(u"View"))
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


class Delete(form.PageForm):
    """A confirmation for to delete an object.
    """
    grok.baseclass()
    grok.title(_(u"Delete"))
    grok.context(content.IBaseContent)

    label = _(u"Confirm deletion")
    form_name = _(u"Are you really sure ?")
    fields = {}

    successMessage = _("This object has been deleted")
    failureMessage = _("This object could not be deleted")

    _deleted = False
    
    @form.button.buttonAndHandler(_('Confirm'), name='confirm')
    def handleConfirm(self, action):
        container = self.context.__parent__
        name = self.context.__name__
        
        if name in container:
            try:
                del container[name]
                self._deleted = True
            except ValueError, e:
                pass
        
        if self._deleted is True:
            self.status = self.successMessage
            self.redirect(self.url(container))
        else:
            self.status = self.failureMessage
            self.redirect(self.url(self.context))
