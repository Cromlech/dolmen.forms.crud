#!/usr/bin/python
# -*- coding: utf-8 -*-

from zeam.form.ztk.actions import CancelAction
from dolmen.forms.base.utils import apply_data_event
from zeam.form import base
from zeam.form.base.markers import SUCCESS, FAILURE
from zope.event import notify
from zope.i18nmessageid import MessageFactory
from zope.lifecycleevent import ObjectCreatedEvent

_ = MessageFactory("dolmen.forms.crud")


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

        obj = self.factory(**data)
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

        apply_data_event(form.fields, form.context, data)

        form.flash(_(u"Content updated"))
        form.redirect(form.url(form.context))

        return SUCCESS


class DeleteAction(base.Action):
    """Delete action for any locatable context.
    """
    successMessage = _(u"The object has been deleted.")
    failureMessage = _(u"This object could not be deleted.")
    
    def __call__(self, form):
        container = form.context.__parent__
        name = form.context.__name__

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
