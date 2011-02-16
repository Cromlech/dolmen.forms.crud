# -*- coding: utf-8 -*-

from dolmen.forms.crud import i18n as _
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from zeam.form import base
from zeam.form.base.markers import SUCCESS, FAILURE
from zeam.form.ztk.actions import CancelAction  # Convenience import
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent


class AddAction(base.Action):
    """Add action for an IAdding context.
    """

    def __init__(self, title, factory):
        super(AddAction, self).__init__(title)
        self.factory = factory

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        obj = self.factory()
        set_fields_data(form.fields, obj, data)
        notify(ObjectCreatedEvent(obj))
        form.context.add(obj)

        form.flash(_(u"Content created"))
        form.redirect(form.url(obj))

        return SUCCESS


class UpdateAction(base.Action):
    """Update action for any locatable object.
    """

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        apply_data_event(form.fields, form.getContentData(), data)
        form.flash(_(u"Content updated"))
        form.redirect(form.url(form.context))

        return SUCCESS


class DeleteAction(base.Action):
    """Delete action for any locatable context.
    """
    successMessage = _(u"The object has been deleted.")
    failureMessage = _(u"This object could not be deleted.")

    def __call__(self, form):
        content = form.getContentData().getContent()
        container = content.__parent__
        name = content.__name__

        if name in container:
            try:
                del container[name]
                form.status = self.successMessage
                form.flash(form.status)
                form.redirect(form.url(container))
                return SUCCESS
            except ValueError:
                pass

        form.status = self.failureMessage
        form.flash(form.status)
        form.redirect(form.url(form.context))
        return FAILURE
