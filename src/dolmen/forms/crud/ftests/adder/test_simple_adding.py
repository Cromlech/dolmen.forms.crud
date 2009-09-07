"""
Adding view
===========

`dolmen.forms.crud` provides an abstraction for the 'adding' action.
It allows pluggability at the container level and does handle the
naming/persistence duet. More explicitly, it's a named adapter that will
query the AddForm, call the object checking methods, choose a name using
a INameChooser and finally, if everything went smoothly, set it on the context.

A base AddView is registered out-of-the-box as a named traversable adapter
called 'add'. It uses the following pattern: ++add++factory_name.
`factory_name` must be the name of a `dolmen.content.IFactory` component.


Let's first create a container in which we'll test the adding view :

  >>> sietch = Sietch()
  >>> sietch.title = u'Tabr'
  >>> dolmen.IBaseContent.providedBy(sietch)
  True
  
  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()
  >>> root['sietch'] = sietch


The container created, the adding view should be available and operational.
Let's have a quick overview:

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> from z3c.form.interfaces import IFormLayer

  >>> from zope.publisher.interfaces import browser
  >>> class BaseFormSkin(IFormLayer, browser.IDefaultBrowserLayer):
  ...     '''A skin layer for forms.
  ...     '''

  >>> request = TestRequest(skin=BaseFormSkin)

  >>> addingview = getMultiAdapter((sietch, request), name='add')
  >>> addingview
  <dolmen.forms.crud.addview.Adder object at ...>


The adding view is available for our item. Though, if we try to access our
current factory, a NotFound error will be raised : we have no add form
registered.

  >>> addingview.traverse('fremen', [])
  Traceback (most recent call last):
  ...
  NotFound: Object: <dolmen.forms.crud.ftests...>, name: 'fremen'


Let's try to check, now, if we create and register a very basic generic crud
AddForm:

  >>> import dolmen.forms.crud as crud
  >>> class AddForm(crud.Add):
  ...     '''Generic add form.
  ...     '''
  
  >>> import grokcore.component.testing as testing
  >>> testing.grok_component('addform', AddForm)
  True

  >>> form = addingview.traverse('fremen', [])
  >>> form
  <dolmen.forms.crud.ftests.adder.test_simple_adding.AddForm object at ...>

Here we go. Our AddForm is returned as we traverse toward the factory 'fremen'.
Let's have a look at the adding view property and methods :

  >>> addingview.content_name
  'fremen'
  >>> addingview.nextURL()
  'http://127.0.0.1/sietch'

Perfect. Our adding view is ready to be used. Before testing the AddForm
itself, let's have a try at the `add` method :

  >>> naib = Fremen()
  >>> added_item = addingview.add(naib)
  >>> added_item
  <dolmen.forms.crud.ftests.adder.test_simple_adding.Fremen object at ...>
  >>> added_item.__name__
  u'Fremen'
  >>> added_item.__parent__ is sietch
  True


The `add` method checks if the constraints are respected. If the container has
a defined restriction (using zope.app.container.constraints), we get an error
if the contract is violated.

  >>> rabban = Harkonnen()
  >>> addingview.add(rabban)
  Traceback (most recent call last):
  ...
  InvalidItemType: (<...Sietch object at ...>, <...Harkonnen object at ...>, (<InterfaceClass dolmen.forms.crud.ftests.adder.test_simple_adding.IDesertWarrior>,))


The `add` method of the adding view can be called from the AddForm, to delegate
the adding operation. The generic adding view already handles the common
operations such as naming and persistence. Still, our AddForm is responsible
of the factoring of the item. Let's test very quickly the important attributes
and methods :

  >>> form.update()
  >>> form.updateForm()
  >>> form.fields
  <z3c.form.field.Fields object at ...>
  >>> factored_item = form.create({'title': u'Shani', 'water': 5})
  >>> factored_item
  <dolmen.forms.crud.ftests.adder.test_simple_adding.Fremen object at ...>
  >>> factored_item.title
  u'Shani'
  >>> factored_item.water
  5

The adding view works as intended. The real interest in using such an
abstraction is to be able to easily switch adding behaviors just by
registering a new component.
"""

import zope.schema
import dolmen.content as dolmen
from zope.app.container.constraints import contains


class IDesertWarrior(dolmen.IBaseContent):
    """Defines a warrior living in the desert.
    """
    water = zope.schema.Int(
        title = u"Number water gallons owned",
        default = 1,
        required = True
        )


class IDesertCave(dolmen.IBaseContent):
    """Defines a cave carved in the mountains by the Coriolis storms.
    """
    contains(IDesertWarrior)


class Sietch(dolmen.Container):
    """A grotto located on Arrakis.
    """
    dolmen.name('sietch')
    dolmen.schema(IDesertCave)
    dolmen.nofactory()
    

class TrainingCamp(dolmen.Factory):
    """A camp that produces Fremen warriors.
    """
    dolmen.name(u"fremen")
    title = u"Fremen training camp"


class Fremen(dolmen.Content):
    """Inhabitants on the deep deserts. They live in sietches.
    """
    dolmen.name(u'Fremen Warrior')
    dolmen.schema(IDesertWarrior)
    dolmen.factory(TrainingCamp)


class Harkonnen(dolmen.Content):
    """A native of Giedi Prime.
    """
    dolmen.name('Harkonnen')
    dolmen.nofactory()
