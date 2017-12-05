To run with test input:
    cat test_input.txt | python bomdotcom.py

To run tests:
    python test_bomdotcom.py

Some notes:

Didn't have a lot of time to work on this, so I decided on making as simple /
elegant a solution as possible would be best. But I definitely wanted
to lump in some tests. So I made a minimal test class to test the input
processing.

Things I'd like to have done:

    * Make a nice slick CLI for this, which outputs usage if no input is
      received.
    * More testing, including edge cases.
    * Refactor to make other methods more testable.
    * Focus on efficiency. The sorting isn't ideal.
    * More logging and comments.

Ben Friedland
www.bugben.com
