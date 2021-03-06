.. _debugging:

*********
Debugging
*********

Writing C++ routines is no easy task. Many times a program ends
abrutly with an error. A common error is a "*segmentation fault*"
error. When a program displays this message it usually means that the
program was trying to access a memory location outside its address
space. Many other errors may occurr but finding these errors is
usually a time consuming task and several debugging techniques are
needed to find them.

A common debugging technique is to print messages on your program so
that you may debug or trace the execution of the program. Excentury
provides three macro functions to aid in future debugging tasks.
These functions expand to a command if the ``DEBUG`` macro is defined
before the inclusion of ``excentury.h``. There are three values that
the ``DEBUG`` macro can take. These three values are the several
levels of debugging which can facilitate the debugging task at hand
and in the future.

To explore what each of these levels do we will consider the file
``example.cpp`` which looks as follows

.. code-block:: cpp
    :linenos:

    #include <excentury/excentury.h>

    int main() {
        debug("This message is only seen with DEBUG set to 2\n");
        trace("This message is only seen with DEBUG set to 3\n");
        printf("Hello world\n");
        exitif(true, NULL, "This is a test to check that DEBUG is on.\n");
        printf("Debug was turned off...\n");
    }

Notice that a compilation without defining the ``DEBUG`` macro will result
in the following

.. code-block:: sh

    $ g++ example.cpp -o example.run
    $ ./example.run
    Hello world
    Debug was turned off...

This is because ``debug``, ``trace`` and ``exitif`` expanded to
nothing, *i.e.*, ``example.cpp`` expanded to

.. code-block:: cpp

    #include <excentury/excentury.h>

    int main() {
        printf("Hello world\n");
        printf("Debug was turned off...\n");
    }

Level 1: ``exitif``
===================

This is the most basic level and it will allow you to use the
``exitif`` function.

.. code-block:: cpp

    exitif(condition, function_call, ...)

This is a macro which expands to the following:

.. code-block:: cpp

    if (condition) {
        printf(...);
        function_call;
        exit(1);
    }

To can either define ``DEBUG`` before inclusion of
``excentury/excentury.h`` or define it during the call to ``g++``

.. code-block:: sh

    $ g++ -DDEBUG=1 example.cpp -o example.run1
    $ ./example.run1
    Hello world
    ERROR CAUGHT BY example.cpp line 7 executing: 

        int main()

    The error occurred because:  true

    This is a test to check that DEBUG is on.

In this case, notice that since ``exitif`` was defined and the
condition to exit was satisfied (any statement that evalutes to
``true``) the program printed a statement explaining the error
detected and halted the execution of the program.

Level 2: ``debug``
==================

This level provides the function ``debug``. These messages should
only be used while debuging. If the messages could help in the future
then we should replace ``debug`` with the level 3 function ``trace``.
The ``debug`` function behaves as ``printf`` but will only be
expanded in levels 2 and 3.

.. code-block:: sh

    $ g++ -DDEBUG=2 example.cpp -o example.run2
    $ ./example.run2
    This message is only seen with DEBUG set to 2
    Hello world
    ERROR CAUGHT BY example.cpp line 7 executing: 

        int main()

    The error occurred because:  true

    This is a test to check that DEBUG is on.

Notice the message from level 1 was displayed as well as the message
provided to the ``debug`` function. Again, these messages are meant
to be temporary in order to find out what is going on. We could have
used the ``printf`` function but soon we will not be able to
differentiate between the actual statements that we want to display
and those that were temporary debugging messages.

Level 3: ``trace``
==================

Provides the function ``trace`` which will display messages when
level 3 is active. These messages are meant to be permanent messages
and should be designed to help the user have a better idea of what is
going on with the program.

.. code-block:: sh

    $ g++ -DDEBUG=3 example.cpp -o example.run3
    $ ./example.run3
    This message is only seen with DEBUG set to 2
    This message is only seen with DEBUG set to 3
    Hello world
    ERROR CAUGHT BY example.cpp line 7 executing: 

        int main()

    The error occurred because:  true

    This is a test to check that DEBUG is on.

The debugging level 3 is really meant to be used as a last resort
tool. If done correctly, the debugging level 1 should catch the
errors. If this is not enough then we may display messages by using
level 2. If all fails then we may want to activate the ``trace``
messages to see if there are any useful messages.
