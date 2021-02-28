# foobartory
Robots creating foo and bars.

## How to use:
:warning: You need python >= 3.7 to execute the program, because it uses `asyncio`.
```shell
# clone the repository
$ git clone git@github.com:tbcvl/foobartory.git
# execute the file
$ python3.8 foobartory/foobartory.py
```
:information_source: The output is very verbose (~3k logs) and the program takes ~20 seconds to run.
You may want to put the logs in a dedicated file:
```shell
$ python3.8 foobartory/foobartory.py > output.txt
```

## How to hack:
The "second" in the game is 1/100 second in real life.
If you want to change this, for example to able to read the logs in real time,
you can change the var `second_multiplier` in the code:
```diff
 class Factory:
-    second_multiplier = 1 / 100
+    second_multiplier = 1
     foo_list = []
```

## Example of output, to understand what the program does
```
INFO - Factory starts
INFO - robot #1 created
INFO - robot #2 created
INFO - robot #1 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 1 foos now
INFO - robot #2 created Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, 1 bars now
INFO - robot #1 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 2 foos now
...
INFO - robot #1 succeeded to assemble Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5 and Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, 1 foobars now
WARNING - robot #1 failed to assemble, no bar available
INFO - robot #2 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 3 foos now
WARNING - not enough euros and foos, robot #2 can not create new robot
...
INFO - robot #2 succeeded to assemble Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5 and Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, 4 foobars now
WARNING - not enough euros and foos, robot #1 can not create new robot
...
INFO - robot #3 created Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, 30 bars now
INFO - robot #4 created
INFO - robot #2 created new robot #4
INFO - robot #4 created Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, 30 bars now
...
INFO - robot #3 sold Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5 and Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, we have 97 euros now
INFO - robot #2 created new robot #11
WARNING - not enough euros and foos, robot #7 can not create new robot
...
INFO - robot #19 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 2 foos now
WARNING - robot #20 failed to assemble, Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5 is lost, Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe is reused
INFO - robot #22 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 2 foos now
INFO - robot #12 created Bar id #d72eb65b-9034-491f-8499-b20f23a7afbe, 441 bars now
INFO - robot #14 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 5 foos now
INFO - robot #18 created Foo id #4af2d42e-c2ed-4980-95ac-dcdc05ee0ff5, 6 foos now
INFO - robot #30 created
INFO - robot #29 created new robot #30
INFO - SUCCESS! 30 robots created!

```
