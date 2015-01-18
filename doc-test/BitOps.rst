.. generated with `chpldoc --docs-text-only modules/standard/BitOps.chpl` and
   then modified to include rst directives...

Module: BitOps
==============

Bit Manipulation Functions
 
.. function:: inline proc clz(x: uint(64)(<DefExprType>))

    count leading zeros

    :arg x: unsigned integer of size `bits`
    :arg bits: 8, 16, 32, 64

    :returns: the number of 0 bits before the most significant 1 bit in `x` as
              `x.type`
   

.. function:: inline proc clz(x: int(64)(<DefExprType>))
      
    count leading zeros

    :arg x: integer of size `bits`
    :arg bits: 8, 16, 32, 64

    :returns: the number of 0 bits before the most significant 1 bit in `x` as
              `x.type`
   

.. function:: inline proc ctz(x: uint(64)(<DefExprType>))
      
    count trailing zeros

    :arg x: unsigned integer of size `bits`
    :arg bits: 8, 16, 32, 64

    :returns: the number of 0 bits after the least significant 1 bit in `x` as
              `x.type`
   

.. function:: inline proc ctz(x: int(64)(<DefExprType>))
      
    count trailing zeros

    :arg x: integer of size `bits`
    :arg bits: 8, 16, 32, 64

    :arg returns: the number of 0 bits after the least significant 1 bit in `x` as
             `x.type`
   

.. function:: inline proc popcount(x: uint(64)(<DefExprType>))
      
    population count

    :arg x: unsigned integer of size `bits`
    :arg bits: 8, 16, 32, 64

    :arg returns: the number of 1 bits set in `x` as `x.type`
   

.. function:: inline proc popcount(x: int(64)(<DefExprType>))
      
    population count

    :arg x: integer of size `bits`
    :arg bits: 8, 16, 32, 64

    :arg returns: the number of 1 bits set in `x` as `x.type`
   

.. function:: proc bitMatMultOr(x: uint(64)(64), y: uint(64)(64)): uint(64)(64)

.. function:: inline proc bitRotLeft(x, shift)

.. function:: inline proc bitRotRight(x: uint(64)(64), shift)
