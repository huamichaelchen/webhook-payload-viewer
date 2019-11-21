### Quick Start

1. `docker-compose up --build -d`
2. visit http://localhost:5000

### Requirements:


* [ ] Support multiple unique endpoints to enable simultaneous testing of several webhooks at once.
* [x] Be a stateless service with a backing datastore for persistence.
* [x] Have a functional health check.
* [x] Execute within a Docker container.

### ToDos:

1. Add data to MongoDB
2. Add a stub trigger event
3. Add concurrency
4. Have some GUI..
