### Quick Start
1. `docker-compose up --build -d`
2. visit http://localhost:5000
3. go to the register page to create a random user
4. follow the buttons
5. `docker-compose down` to destroy everything

NOTE: you may need to run `sudo docker-compose up --build -d` again if you want to poke around due to volume mount default
to `root`. Probably can be solved using
* user_id mapping
* or use [rootless docker](https://www.katacoda.com/courses/docker/rootless)


### How to use
* visit http://localhost:8481 to see what data has been created in MongoDB
* Follow the ugly buttons (sorry about that...)
* "Generate Webhook Endpoint for User" button to generate a webhook url
  * which will lead you to a page with two options, "Kick off WebHook" or "Observe WebHook"
  * Copy that GUID number and find it inside *MongoDB Express GUI* (aka. http://localhost:8481), you won't see 'Payload'
  * Now click on "Kick off WebHook" button, then go back to *MongoDB Express GUI* and click on the "find" button there 
  again to see 'Payload' been added. (However, in this case, there is not really any payload...)

### Requirements:
* [x] Support multiple unique endpoints to enable simultaneous testing of several webhooks at once.
* [x] Be a stateless service with a backing datastore for persistence.
* [x] Have a functional health check.
* [x] Execute within a Docker container.

### ToDos:

* [x] Add data to MongoDB
* [x] Add a stub trigger event
* ~~Add concurrency~~
* [x] Have some GUI.. (well, somewhat a GUI...)

### Further improvements:
* [ ] Add JWT
* [ ] Better frontend for usability or at least bare-minimal of ease of navigation
* [ ] Logout...
* [ ] Test with a true WebHook service from other applications, such as Google Hangout, GitHub etc.