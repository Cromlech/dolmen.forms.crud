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

  >>> request = TestRequest()
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

  >>> addingview.traverse('fremen', [])
  <dolmen.forms.crud.ftests.adder.test_simple_adding.AddForm object at ...>


Here we go. Our AddForm is returned as we traverse toward the factory 'fremen'.
Let's have a look at the adding view property :

  >>> addingview.content_name
  'fremen'


Perfect. Our adding view is ready to be used. Before testing the AddForm
itself, let's have a try at the 'add' method :

  >>> naib = Fremen()
  >>> added_item = addingview.add(naib)
  >>> added_item
  <dolmen.forms.crud.ftests.adder.test_simple_adding.Fremen object at ...>
  >>> added_item.__name__
  u'Fremen'
  >>> added_item.__parent__ is sietch
  True

The adding view works as intended. The real interest in using such an
abstraction is to be able to easily switch adding behaviors just by
registering a new component.
"""

import zope.schema
import dolmen.content as dolmen


class IDesertWarrior(dolmen.IBaseContent):
    """Defines a warrior living in the desert.
    """
    water = zope.schema.Int(
        title = u"Number water gallons owned",
        default = 1,
        required = True
        )


class Sietch(dolmen.Container):
    """A grotto located on Arrakis.
    """
    dolmen.name('sietch')
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
