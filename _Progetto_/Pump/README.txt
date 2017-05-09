PUMP OBJECT README
Once the pump has registered into the Service Catalog it listen to its mqtt topic.


Message sent through the broker MUST contain only one of the following string:

"ON"  --> 	Switch on the relay which control the pump

or

"OFF" -->	Switch off the relay which control the pump

[NO JSON]