=================
dolmen.forms.crud
=================

`dolmen.forms.crud` is a module which helps developers create their
C.R.U.D forms using `Grok`, `megrok.z3cform` and `dolmen.content`. It
provides a collection of base classes to add, edit, and access
content. It provides adapters to customize the fields of a form.


Adding view
===========

`dolmen.forms.crud` provides an abstraction for the 'adding'
action. It allows pluggability at the container level and handles
naming and persistence. More explicitly, it's a named adapter that
will query the add form, check the constraints, choose a name (using a
INameChooser) and finally, if everything went smoothly, add it on the
context.

A base adding view is registered out-of-the-box as a named traversable
adapter called 'add'. It uses the following pattern:
++add++factory_name. `factory_name` must be the name of a
`dolmen.content.IFactory` component.

Let's first create a container in which we'll test the adding view::

  >>> import dolmen.content
  >>> from dolmen.forms.crud.tests import Sietch

  >>> sietch = Sietch()
  >>> sietch.title = u'Tabr'
  >>> dolmen.content.IBaseContent.providedBy(sietch)
  True
  
  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()
  >>> root['sietch'] = sietch

With the container created, the adding view should be available and operational.
Let's have a quick overview::
    
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> addingview = getMultiAdapter((sietch, request), name='add')
  >>> addingview
  <dolmen.forms.crud.addview.Adder object at ...>


The adding view component explicitly checks the security requirement
on the factory. To test that behavior, we set up two
accounts. 'zope.manager' has all the permissions granted while
'zope.manfred' only has the 'zope.View' credentials. Our factory
explicitly requires a 'zope.ManageContent' permission to be
called. Let's try to access it with Manfred::

  >>> import zope.security.management as security  
  >>> from zope.security.testing import Principal, Participation

  >>> manager = Principal('zope.manager', 'Manager')
  >>> manfred = Principal('zope.manfred', 'Manfred')

  >>> security.newInteraction(Participation(manfred))
  >>> addingview.traverse('fremen', [])
  Traceback (most recent call last):
  ...
  Unauthorized: <class 'dolmen.forms.crud.tests.Fremen'> requires the 'zope.ManageContent' permission.
  >>> security.endInteraction()

Manfred is not authorized, however Manager should successfully be able
to access the addingview::

  >>> security.newInteraction(Participation(manager))
  >>> addingview.traverse('fremen', [])
  Traceback (most recent call last):
  ...
  NotFound: Object: <dolmen.forms.crud.tests.Sietch object at ...>, name: 'fremen'

The adding view is available for our item. Though, as we have no add form
registered, a NotFound error will be raised if we try to access our
current factory.

Let's create and register a very basic generic crud
add form::

  >>> import dolmen.forms.crud as crud
  >>> class AddForm(crud.Add):
  ...     '''Generic add form.
  ...     '''
  
  >>> import grokcore.component
  >>> grokcore.component.testing.grok_component('addform', AddForm)
  True

  >>> addform = addingview.traverse('fremen', [])
  >>> addform
  <AddForm object at ...>

Our AddForm is returned as we traverse toward the factory
'fremen'.

Perfect. Our adding view is ready to be used. Before testing the AddForm
itself, let's have a try at the `add` method::

  >>> from dolmen.forms.crud.tests import Fremen

  >>> naib = Fremen()
  >>> added_item = addingview.add(naib)
  >>> added_item
  <dolmen.forms.crud.tests.Fremen object at ...>

  >>> added_item.__name__
  u'Fremen'
  >>> added_item.__parent__ is sietch
  True

An IAdding component should always be locatable::

  >>> addingview.__parent__
  <dolmen.forms.crud.tests.Sietch object at ...>
  >>> addingview.__name__
  u''

The `add` method checks if the constraints are respected. If the
container has defined restrictions or if some interface contract is
violated, we get an error::

  >>> from dolmen.forms.crud.tests import Harkonnen

  >>> rabban = Harkonnen()
  >>> addingview.add(rabban)
  Traceback (most recent call last):
  ...
  InvalidItemType: (<...Sietch object at ...>, <...Harkonnen object at ...>, (<InterfaceClass dolmen.forms.crud.tests.IDesertWarrior>,))


The `add` method of the adding view can be called from the AddForm to delegate
the adding operation. The generic adding view already handles the common
operations such as naming and persistence. Still, our add form is responsible
for the factoring of the item. Let's test the important attributes
and methods::

  >>> addform.fields.keys()
  ['title', 'water']

  >>> fremen = addform.create({'title': u'Chani', 'water': 5})
  >>> fremen
  <dolmen.forms.crud.tests.Fremen object at ...>

  >>> fremen.title
  u'Chani'
  >>> fremen.water
  5

The adding view works as intended. The real interest in using such an
abstraction is the ease with which you can switch adding behaviors, just by
registering a new component.


Generic forms
=============

`dolmen.forms.crud` provides a set of ready-to-use base classes that
will auto-generate forms based on `dolmen.content` schemas.


Create
------

The add form implementation is tightly tied to the adding view. As the add
form behavior has been mostly covered above, we'll only test the
presence of the fields and the label on the form itself::

  >>> addform = addingview.traverse('fremen', [])
  >>> addform
  <AddForm object at ...>

  >>> print addform.label
  Fremen training camp

  >>> addform.fields.keys()
  ['title', 'water']
  
  >>> addform.updateForm()
  >>> for action in addform.actions: print action
  save


Read
-----

A special kind of form allows you display your content::

  >>> class DefaultView(crud.Display):
  ...     '''Generic display form.
  ...     '''
  
  >>> grokcore.component.testing.grok_component('display', DefaultView)
  True

  >>> view = getMultiAdapter((fremen, request), name='defaultview')
  >>> view
  <DefaultView object at ...>

The Display form removes the 'title' from the list of fields. This
particular attribute is used directly by the template::

  >>> view.fields.keys()
  ['water']

A display form has no actions::

  >>> view.updateForm()
  >>> for action in view.actions: print action
  Traceback (most recent call last):
  ...
  AttributeError: 'DefaultView' object has no attribute 'actions'

`dolmen.forms.crud` provides a very basic template for that form. As
we can see, the title attribute is used as the HTML header (h1) of the
page::

  >>> print view()
  <div class="defaultview">
    <h1>Chani</h1>
    <div class="field">
      <label for="form-widgets-water">
        <span>Number water gallons owned</span>
      </label>
      <p class="discreet"></p>
      <div class="widget">
        <span id="form-widgets-water"
              class="text-widget required int-field">5</span>
      </div>
    </div>
  </div>


Update
------

An edit form can be registered simply by sublassing the Edit base class::

  >>> class EditForm(crud.Edit):
  ...     '''Generic edit form.
  ...     '''
  ...     def nextURL(self):
  ...         return u"We don't have a persistent data."

  >>> grokcore.component.testing.grok_component('editform', EditForm)
  True

This form registered, we can check if all the fields are ready to be
edited::

  >>> request = TestRequest(form={
  ...     'form.widgets.water': '25',
  ...     'form.widgets.title': u'Stilgar',
  ...     'form.buttons.apply': u'Apply'}
  ...     )

  >>> editform = getMultiAdapter((fremen, request), name='editform')
  >>> editform
  <EditForm object at ...>

  >>> editform.updateForm()
  >>> for action in editform.actions: print action
  apply

  >>> editform.fields.keys()
  ['title', 'water']

The values should now be set::

  >>> fremen.title
  u'Stilgar'
  >>> fremen.water
  25

Form customization
==================

To customize forms, the usual solution is to subclass them and to work
with the subclass. `dolmen.forms.crud` proposes a new component to
customize your forms. Defined by the `IFieldsCustomization` interface,
it's an adapter that allows you to interact at the field level.

In a `IFieldsCustomization`, the customization happens at the __call__
level. The forms, while they update the objects fields, query a
`IFieldsCustomization` adapter and call it, giving the fields as an
argument.

Let's implement an example::

  >>> class RemoveWater(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Add, None)
  ...
  ...    def __call__(self, fields):
  ...       """Alters the form fields"""
  ...       return fields.omit('water')

  >>> from zope.interface import verify
  >>> verify.verifyClass(crud.IFieldsCustomization, RemoveWater)
  True

We can now register and test the customization::

  >>> grokcore.component.testing.grok_component('custom', RemoveWater)
  True

  >>> addform = addingview.traverse('fremen', [])
  >>> for field in addform.fields: print field
  title

One important thing is noticeable here : the 'RemoveWater' adapter was
registered for the 'Fremen' component. To be able to lookup the
registery for suitable adapters, the add form uses a special lookup
function : `dolmen.forms.crud.utils.queryClassMultiAdapter`.

We can test a more complex example, returning a brand new instance of
Fields::

  >>> import dolmen.forms.base
  >>> class AddFieldToView(crud.FieldsCustomizer):
  ...    grokcore.component.adapts(Fremen, crud.Display, None)
  ...
  ...    def __call__(self, fields):
  ...       """Returns a new instance of Fields.
  ...       """
  ...       schema = dolmen.content.schema.bind().get(self.context)
  ...       return dolmen.forms.base.Fields(*schema)

  >>> grokcore.component.testing.grok_component('viewer', AddFieldToView)
  True

Checking the fields, we should get *all* the fields defined by the
Fremen schema::

  >>> view = getMultiAdapter((fremen, request), name='defaultview')
  >>> view.fields.keys()
  ['title', 'water']


Events and field updates
========================

When using the generic `dolmen.forms.crud` forms, some events are
triggered for you. They represent the lifecycle of the manipulated object.

To check on all the events triggered, we can set up a simple event
logging list and a generic handler::

  >>> from zope.component import provideHandler
  >>> from zope.component.interfaces import IObjectEvent
  >>> logger = []
  
  >>> def event_logger(object, event):
  ...   logger.append(event)

  >>> provideHandler(event_logger, (Fremen, IObjectEvent))


Adding events
-------------

In order to notify the lifecycle handlers, two main events
are fired while an object is created using an add form::

  >>> arrakin = root['arrakin'] = dolmen.content.Container()
  >>> addingview = getMultiAdapter((arrakin, request), name='add')
  >>> addform = addingview.traverse('fremen', [])

  >>> chani = addform.createAndAdd({'title': u'Chani'})

We iterate through the logger to check the events triggered during the
object creation::

  >>> for event in logger: print event
  <dolmen.forms.crud.events.ObjectInitializedEvent object at ...> 
  <zope.app.container.contained.ObjectAddedEvent object at ...>
    
We can see that there is no `zope.lifecycleevent.ObjectCreatedEvent`
fired. Instead, we have a `dolmen.forms.crud.ObjectInitializedEvent`.
Let's have a closer look at this homegrown event::

  >>> from zope.lifecycleevent import IObjectCreatedEvent
  >>> init_event = logger[0]

  >>> IObjectCreatedEvent.providedBy(init_event)
  True

  >>> for desc in init_event.descriptions:
  ...   print "%r: %s" % (desc.interface, desc.attributes)
  <InterfaceClass dolmen.content.interfaces.IBaseContent>: ('title',)
  

Editing events
--------------

Let's have the same introspection check with the edit form::

  >>> logger = []

We provide data for the update::

  >>> request = TestRequest(form={
  ...     'form.widgets.water': '10',
  ...     'form.widgets.title': u'Sihaya',
  ...     'form.buttons.apply': u'Apply'}
  ...     )

  >>> editform = getMultiAdapter((chani, request), name='editform')
  >>> editform.updateForm()

We check the trigged events::

  >>> for event in logger: print event
  <zope.app.event.objectevent.ObjectModifiedEvent object at ...>

In depth, we can check if the updated fields are correctly set in the
event's descriptions::

  >>> for desc in logger[0].descriptions:
  ...   print "%r: %s" % (desc.interface, desc.attributes)
  <InterfaceClass dolmen.forms.crud.tests.IDesertWarrior>: ('water',)
  <InterfaceClass dolmen.content.interfaces.IBaseContent>: ('title',)

  >>> chani.title
  u'Sihaya'
  >>> chani.water
  10


Field update
------------

`dolmen.forms.base` provides the description of a new component that
can be used to atomize the updating process of an object:
`IFieldUpdate`. An implementation is available in `dolmen.forms.crud`,
using an event handler, listening on ObjectModifiedEvent and
ObjectInitializedEvent::

  >>> updates = []

  >>> from zope.schema import TextLine
  >>> from zope.component import adapter, provideAdapter
  >>> from zope.interface import implementer
  >>> from dolmen.forms.base import IFieldUpdate

  >>> @implementer(IFieldUpdate)
  ... @adapter(Fremen, TextLine)
  ... def updated_textfield(field, context):
  ...    updates.append((field, context))

  >>> provideAdapter(updated_textfield, name="updatetext")


Using an add form, the IFieldUpdate adapters should be called during an objects creation::

  >>> desert = root['desert'] = dolmen.content.Container()
  >>> addingview = getMultiAdapter((desert, request), name='add')
  >>> addform = addingview.traverse('fremen', [])

  >>> kynes = addform.createAndAdd({'title': u'liet'})
  >>> print updates
  [(<dolmen.forms.crud.tests.Fremen object at ...>, <zope.schema._bootstrapfields.TextLine object at ...>)]


We can do the same thing for the edit form::

  >>> updates = []

  >>> request = TestRequest(form={
  ...     'form.widgets.water': '50',
  ...     'form.widgets.title': u'Imperial weather specialist',
  ...     'form.buttons.apply': u'Apply'}
  ...     )

  >>> editform = getMultiAdapter((kynes, request), name='editform')
  >>> editform.updateForm()

  >> kynes.title
  u'Imperial weather specialist'

  >>> updates
  [(<dolmen.forms.crud.tests.Fremen object at ...>, <zope.schema._bootstrapfields.TextLine object at ...>)]

Updating a field without a registered IFieldUpdate adapter shouldn't do
anything::

 >>> updates = []

  >>> request = TestRequest(form={
  ...     'form.widgets.water': '40',
  ...     'form.buttons.apply': u'Apply'}
  ...     )

  >>> editform = getMultiAdapter((kynes, request), name='editform')
  >>> editform.updateForm()

  >>> updates
  []
