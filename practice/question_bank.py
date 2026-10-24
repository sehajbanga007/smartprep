"""Local IMAP syllabus question bank (works offline).

Each raw entry: (difficulty, question, correct answer, [3 wrong answers], explanation).
Option letters are assigned deterministically so the correct letter varies (A-D).
"""

TOPICS = ["HTML", "CSS", "JavaScript", "MongoDB", "NoSQL", "Django", "Docker"]
DIFFICULTIES = ["easy", "medium", "hard"]
LETTERS = "ABCD"

_RAW = {
    "HTML": [
        ("easy", "Which element is the semantic choice for a block of main navigation links?", "<nav>", ["<div>", "<span>", "<section>"], "<nav> tells browsers and assistive tools the content is navigation."),
        ("easy", "Which attribute supplies alternative text for an image?", "alt", ["title", "src", "caption"], "alt is read by screen readers and shown if the image fails to load."),
        ("easy", "Which tag creates an ordered (numbered) list?", "<ol>", ["<ul>", "<li>", "<dl>"], "<ol> numbers its <li> items; <ul> gives bullets."),
        ("medium", "Which input type gives built-in browser validation for e-mail addresses?", "email", ["text", "mail", "address"], 'type="email" checks the value looks like an e-mail before submission.'),
        ("medium", "What does the required attribute do on a form field?", "Blocks submission while the field is empty", ["Makes the field read-only", "Hides the field", "Fills the field automatically"], "The browser stops submission and shows a message if the value is missing."),
        ("medium", "Which element links a text caption to a form control so clicking the text focuses the control?", "<label>", ["<legend>", "<caption>", "<title>"], "A <label> tied by for/id improves usability and accessibility."),
        ("hard", "Which rel value should accompany links that open in a new tab, to stop access to window.opener?", "noopener", ["nofollow", "external", "bookmark"], "noopener removes the opener reference and prevents tab-napping."),
        ("hard", "Which element should appear only once per page and wrap its dominant content?", "<main>", ["<article>", "<aside>", "<section>"], "<main> identifies the primary content of the document."),
    ],
    "CSS": [
        ("easy", "Which property changes the colour of text?", "color", ["font-color", "text-style", "foreground"], "color sets the foreground (text) colour."),
        ("easy", "Which selector targets elements with class=\"card\"?", ".card", ["#card", "card", "*card"], "A dot selects by class; # selects by id."),
        ("easy", "In the box model, which layer sits between the content and the border?", "padding", ["margin", "outline", "gap"], "Padding is inner spacing; margin is outside the border."),
        ("medium", "Which declaration turns an element into a Flexbox container?", "display: flex", ["flex: container", "position: flex", "layout: flex"], "display: flex makes the element's children flex items."),
        ("medium", "What does box-sizing: border-box do?", "Includes padding and border inside the declared width and height", ["Removes the border", "Adds margin to the width", "Hides overflow"], "Width and height then describe the whole visible box."),
        ("medium", "Which selector has the highest specificity?", "#menu", ["div", "div.menu", ".menu"], "An id selector outranks class and element selectors."),
        ("hard", "In a row Flexbox container, which property aligns items along the main axis?", "justify-content", ["align-items", "align-content", "flex-wrap"], "justify-content works on the main axis; align-items on the cross axis."),
        ("hard", "Which rule beats an id selector in a normal stylesheet without !important?", "An inline style attribute", ["A class selector", "An element selector", "The universal selector"], "Inline styles have higher specificity than any selector."),
    ],
    "JavaScript": [
        ("easy", "Which keyword declares a block-scoped variable that cannot be reassigned?", "const", ["var", "static", "final"], "const is block-scoped and cannot be reassigned."),
        ("easy", "Which array method adds an item to the end of an array?", "push()", ["pop()", "shift()", "unshift()"], "push appends; pop removes the last item."),
        ("easy", "Which call selects an element by its id?", "document.getElementById()", ["document.findId()", "window.select()", "document.idOf()"], "getElementById returns the element with that id, or null."),
        ("medium", "Which array method returns a new array with each item transformed?", "map()", ["forEach()", "push()", "splice()"], "map returns a new array; forEach returns undefined."),
        ("medium", "Which is NOT a state of a Promise?", "cancelled", ["pending", "fulfilled", "rejected"], "Promises are pending, fulfilled or rejected."),
        ("medium", "What does === check?", "Equal value and equal type", ["Value only, with coercion", "Reference only", "Type only"], "Strict equality does no type coercion."),
        ("hard", "What does typeof null return?", "object", ["null", "undefined", "number"], "This is a long-standing quirk of the language."),
        ("hard", "What does await do inside an async function?", "Pauses the function until the promise settles", ["Blocks the whole browser thread", "Cancels the promise", "Converts the promise to a callback"], "Only the async function pauses; other code keeps running."),
    ],
    "MongoDB": [
        ("easy", "What is the basic unit of data in MongoDB?", "A document", ["A row in a fixed table", "A tablespace", "A column family"], "Documents are BSON/JSON-like records."),
        ("easy", "Which method inserts a single document into a collection?", "insertOne()", ["addRow()", "push()", "createDoc()"], "insertOne adds one document; insertMany adds several."),
        ("easy", "A MongoDB collection is most similar to which relational concept?", "A table", ["A column", "A foreign key", "A transaction"], "A collection groups related documents like a table groups rows."),
        ("medium", "Which query finds documents where age is greater than 18?", "db.users.find({ age: { $gt: 18 } })", ["db.users.find({ age > 18 })", "db.users.select(age > 18)", "db.users.get({ $age: 18 })"], "$gt is the greater-than query operator."),
        ("medium", "Which update changes one field without replacing the whole document?", "updateOne(filter, { $set: { ... } })", ["insertOne(filter)", "deleteOne(filter)", "drop()"], "$set modifies only the named fields."),
        ("medium", "Which method removes every document matching a filter?", "deleteMany()", ["dropMany()", "removeAll()", "truncate()"], "deleteMany removes all matches; deleteOne removes one."),
        ("hard", "Which aggregation stage groups documents and computes totals?", "$group", ["$sort", "$skip", "$limit"], "$group accumulates values per group key."),
        ("hard", "What is the main benefit of an index on a queried field?", "Faster reads for queries on that field", ["Smaller documents", "Automatic schema validation", "Encrypted storage"], "Indexes avoid scanning the whole collection."),
    ],
    "NoSQL": [
        ("easy", "Which of these is a document database?", "MongoDB", ["MySQL", "PostgreSQL", "SQLite"], "MongoDB stores JSON-like documents."),
        ("easy", "What does NoSQL commonly stand for?", "Not only SQL", ["No SQL allowed", "Network SQL", "Normalized SQL"], "It describes non-relational data stores."),
        ("easy", "Which is a popular key-value store?", "Redis", ["MariaDB", "Oracle Database", "SQL Server"], "Redis stores values by key, mostly in memory."),
        ("medium", "What does a flexible schema mean?", "Documents in one collection can have different fields", ["Tables must never change", "Every record needs identical columns", "Data cannot be queried"], "Fields can vary between documents."),
        ("medium", "Which is a typical strength of many NoSQL systems?", "Horizontal scaling across many servers", ["Mandatory joins", "Fixed schemas", "Only vertical scaling"], "Many NoSQL systems shard data across nodes."),
        ("medium", "Compared with relational databases, document databases usually...", "store related data together in one document", ["require normalized tables", "forbid nested data", "cannot store arrays"], "Embedding related data avoids many joins."),
        ("hard", "The CAP theorem lists which three properties?", "Consistency, Availability, Partition tolerance", ["Concurrency, Atomicity, Performance", "Caching, Access, Persistence", "Consistency, Atomicity, Partitioning"], "A distributed store cannot guarantee all three during a partition."),
        ("hard", "Which NoSQL type best models highly connected data such as social networks?", "Graph database", ["Key-value store", "Wide-column store", "Flat file store"], "Graph databases store nodes and relationships directly."),
    ],
    "Django": [
        ("easy", "Which command creates a new Django project?", "django-admin startproject", ["python manage.py newproject", "django create site", "pip install project"], "startproject generates the project skeleton."),
        ("easy", "Which file maps URL paths to views?", "urls.py", ["models.py", "admin.py", "apps.py"], "urls.py holds the URL patterns."),
        ("easy", "Which file defines database tables as Python classes?", "models.py", ["views.py", "settings.py", "urls.py"], "Each model class maps to a table."),
        ("medium", "Which command applies migrations to the database?", "python manage.py migrate", ["python manage.py runserver", "python manage.py collectstatic", "python manage.py shell"], "migrate runs unapplied migrations."),
        ("medium", "Which ORM call returns all rows of a model?", "Model.objects.all()", ["Model.select_all()", "Model.fetch()", "Model.rows"], "objects is the default manager; all() returns a QuerySet."),
        ("medium", "What is the main job of a DRF serializer?", "Validate data and convert between objects and JSON", ["Render HTML templates", "Run database migrations", "Serve static files"], "Serializers validate input and shape output."),
        ("hard", "Which command creates migration files from model changes?", "python manage.py makemigrations", ["python manage.py migrate --create", "python manage.py dumpdata", "python manage.py inspectdb"], "makemigrations writes the migration; migrate applies it."),
        ("hard", "Which DRF base class is used for class-based JSON API views?", "APIView", ["TemplateView", "FormView", "HttpRenderer"], "APIView adds request parsing, renderers and error handling."),
    ],
    "Docker": [
        ("easy", "What is a running instance of a Docker image called?", "A container", ["A volume", "A registry", "A layer"], "Containers are created from images."),
        ("easy", "What is a Dockerfile used for?", "Describing the steps to build an image", ["Storing container logs", "Listing running containers", "Mapping ports at runtime"], "docker build reads the Dockerfile."),
        ("easy", "Which command lists running containers?", "docker ps", ["docker images", "docker build", "docker pull"], "docker ps shows running containers; add -a for all."),
        ("medium", "What does docker run -p 8080:80 do?", "Maps host port 8080 to container port 80", ["Maps container port 8080 to host port 80", "Runs 8080 containers", "Limits CPU to 80%"], "Format is host:container."),
        ("medium", "What is a volume mainly used for?", "Persisting data outside the container's lifecycle", ["Speeding up builds only", "Building images", "Naming networks"], "Volume data survives container removal."),
        ("medium", "Which Dockerfile instruction sets the base image?", "FROM", ["BASE", "IMAGE", "START"], "FROM must start the build stage."),
        ("hard", "How does an image differ from a container?", "An image is a read-only template; a container is a running instance", ["They are identical", "A container is a template for images", "An image always runs as root"], "Many containers can run from one image."),
        ("hard", "Which instruction sets the default command run when a container starts?", "CMD", ["COPY", "EXPOSE", "LABEL"], "CMD provides the default command."),
    ],
}


# Added in version 2: brings every topic to 7 easy, 7 medium and 7 hard questions,
# so a practice set can hold 3-7 questions. Appended after _RAW so the original
# question IDs (1-56) stay the same.
_RAW_EXTRA = {
    "HTML": [
        ("easy", "Which tag creates a hyperlink?", "<a>", ["<link>", "<href>", "<url>"], "<a href=\"...\"> creates a clickable link; <link> connects resources such as stylesheets."),
        ("easy", "Which tag holds the largest default heading?", "<h1>", ["<h6>", "<head>", "<header>"], "<h1> is the top-level heading and <h6> the smallest."),
        ("easy", "Which element embeds an image?", "<img>", ["<image>", "<src>", "<pic>"], "<img> with a src attribute embeds an image."),
        ("easy", "Which tag creates one row in a table?", "<tr>", ["<td>", "<th>", "<row>"], "<tr> is a table row; <td> and <th> are the cells inside it."),
        ("medium", "Which attribute on <a> opens the link in a new tab?", "target=\"_blank\"", ["rel=\"new\"", "href=\"_new\"", "open=\"tab\""], "target=\"_blank\" opens the link in a new browsing context."),
        ("medium", "Which element groups related form controls with a border and caption?", "<fieldset>", ["<formgroup>", "<div>", "<span>"], "<fieldset> with a <legend> groups related inputs."),
        ("medium", "Which meta tag makes a page scale properly on mobile screens?", "<meta name=\"viewport\">", ["<meta name=\"mobile\">", "<meta charset=\"utf-8\">", "<meta name=\"robots\">"], "The viewport meta tag sets width=device-width for responsive layouts."),
        ("medium", "Which attribute gives an element a unique identifier in the page?", "id", ["class", "name", "key"], "An id must be unique; a class can be shared by many elements."),
        ("hard", "Which attribute delays loading an image until it is near the viewport?", "loading=\"lazy\"", ["defer", "async", "lazy=\"true\""], "Native lazy loading saves bandwidth for images that are off screen."),
        ("hard", "Which <script> attributes stop the script from blocking HTML parsing?", "defer and async", ["lazy and eager", "nomodule and nonce", "preload and prefetch"], "Both download in parallel; defer runs after parsing, async as soon as it arrives."),
        ("hard", "Which attributes store custom data on an element for JavaScript to read?", "data-* attributes", ["custom-* attributes", "js-* attributes", "meta-* attributes"], "data-* values are available through element.dataset."),
        ("hard", "Which ARIA attribute gives an accessible name to an element with no visible text?", "aria-label", ["aria-hidden", "role", "tabindex"], "Screen readers announce aria-label as the element's name."),
        ("hard", "Which element lets the browser choose between several image sources by screen size or format?", "<picture>", ["<figure>", "<imgset>", "<gallery>"], "<picture> with <source> children lets the browser pick the best image."),
    ],
    "CSS": [
        ("easy", "Which property sets the background colour of an element?", "background-color", ["bgcolor", "color", "fill"], "background-color paints the element's background."),
        ("easy", "Which property changes the size of text?", "font-size", ["text-size", "font-weight", "size"], "font-size sets how large the text is."),
        ("easy", "Which selector targets the element with id=\"header\"?", "#header", [".header", "header", "*header"], "A hash selects by id; a dot selects by class."),
        ("easy", "Which property adds space outside an element's border?", "margin", ["padding", "border-spacing", "outline"], "Margin is outside the border; padding is inside it."),
        ("medium", "Which position value keeps an element in place while the page scrolls?", "fixed", ["relative", "static", "absolute"], "position: fixed places the element relative to the viewport."),
        ("medium", "Which pseudo-class styles an element while the mouse is over it?", ":hover", [":active", ":focus", ":visited"], ":hover applies while the pointer is over the element."),
        ("medium", "Which unit is relative to the root element's font size?", "rem", ["em", "px", "vh"], "rem uses the <html> font size; em uses the parent's."),
        ("medium", "Which property controls the stacking order of positioned elements?", "z-index", ["order", "stack", "layer"], "Higher z-index values sit on top."),
        ("hard", "Which CSS feature applies styles only when the screen matches a condition, such as a maximum width?", "Media queries (@media)", ["@import", "@font-face", "@keyframes"], "@media rules are the basis of responsive design."),
        ("hard", "Which declaration creates a grid with three equal columns?", "grid-template-columns: repeat(3, 1fr)", ["grid-columns: 3", "columns: 3fr", "display: grid-3"], "repeat(3, 1fr) makes three equal fractions of the free space."),
        ("hard", "How is a CSS custom property declared?", "--main-color: #333;", ["$main-color: #333;", "@main-color: #333;", "var-main-color: #333;"], "Custom properties start with -- and are read with var(--main-color)."),
        ("hard", "Which property lets a flex item grow to fill free space?", "flex-grow", ["flex-basis", "flex-shrink", "align-self"], "flex-grow sets how much of the free space an item takes."),
        ("hard", "Which pseudo-element inserts generated content before an element's content?", "::before", [":first-child", "::marker", "::first-line"], "::before with a content property inserts generated content."),
    ],
    "JavaScript": [
        ("easy", "Which method prints a message to the browser console?", "console.log()", ["print()", "document.log()", "window.echo()"], "console.log writes to the developer console."),
        ("easy", "Which operator joins two strings together?", "+", ["&", "*", "."], "In JavaScript, + concatenates strings."),
        ("easy", "Which value does a declared but unassigned variable hold?", "undefined", ["null", "0", "NaN"], "Variables start as undefined until a value is assigned."),
        ("easy", "Which method turns a JSON string into an object?", "JSON.parse()", ["JSON.stringify()", "JSON.toObject()", "Object.fromJSON()"], "JSON.parse reads JSON text; JSON.stringify writes it."),
        ("medium", "Which array method keeps only the items that pass a test?", "filter()", ["map()", "reduce()", "some()"], "filter returns a new array of the items whose callback returns true."),
        ("medium", "Which method attaches a click handler to an element?", "addEventListener()", ["onEvent()", "attachHandler()", "listen()"], "element.addEventListener('click', handler) registers the handler."),
        ("medium", "What does [...a, ...b] produce when a and b are arrays?", "A new array with the items of a followed by b", ["A nested array [a, b]", "The sum of a and b", "A syntax error"], "Spread syntax expands each array's items into the new array."),
        ("medium", "Which built-in function sends an HTTP request and returns a Promise?", "fetch()", ["request()", "ajax()", "http()"], "fetch is the standard browser API for HTTP requests."),
        ("hard", "What is a closure?", "A function that keeps access to variables from the scope where it was created", ["A function that closes the browser tab", "A loop that stops early", "A private class field"], "Closures let inner functions use outer variables after the outer function returns."),
        ("hard", "What does 0.1 + 0.2 === 0.3 evaluate to?", "false", ["true", "undefined", "NaN"], "Floating-point rounding makes 0.1 + 0.2 equal 0.30000000000000004."),
        ("hard", "After the current script finishes, which callbacks run first?", "Promise callbacks (microtasks)", ["setTimeout callbacks (macrotasks)", "requestAnimationFrame callbacks", "Event listeners added later"], "The microtask queue is emptied before the next macrotask runs."),
        ("hard", "What does \"use strict\" do?", "Turns on stricter parsing and error checking", ["Makes all variables constant", "Disables all warnings", "Compiles the code to bytecode"], "Strict mode turns silent mistakes into thrown errors."),
        ("hard", "Which keyword creates a variable that is hoisted with the value undefined?", "var", ["let", "const", "static"], "let and const are hoisted too but stay in the temporal dead zone until declared."),
    ],
    "MongoDB": [
        ("easy", "Which field does MongoDB add automatically as each document's unique key?", "_id", ["id", "key", "uuid"], "Every document has a unique _id, an ObjectId by default."),
        ("easy", "Which method returns documents from a collection?", "find()", ["getAll()", "select()", "list()"], "find() with an empty filter returns every document."),
        ("easy", "Which format does MongoDB use to store documents?", "BSON", ["CSV", "XML", "YAML"], "BSON is binary JSON with extra types such as dates."),
        ("easy", "Which method counts the documents matching a filter?", "countDocuments()", ["size()", "total()", "length()"], "countDocuments(filter) returns the number of matches."),
        ("medium", "Which query operator matches any value in a given list?", "$in", ["$all", "$or", "$any"], "{ status: { $in: ['a', 'b'] } } matches either value."),
        ("medium", "Which method sorts query results?", "sort()", ["order()", "orderBy()", "arrange()"], "sort({ field: 1 }) sorts ascending and -1 descending."),
        ("medium", "Which update operator appends a value to an array field?", "$push", ["$set", "$inc", "$add"], "$push adds an element to the end of an array."),
        ("medium", "What does find({}, { name: 1 }) return?", "Only the name field (plus _id) of each document", ["Documents sorted by name", "Documents without the name field", "A new index on name"], "The second argument is a projection that picks fields."),
        ("hard", "Which aggregation stage filters documents like a query?", "$match", ["$project", "$group", "$unwind"], "$match passes on only the documents that meet its condition."),
        ("hard", "Which aggregation stage joins documents from another collection?", "$lookup", ["$join", "$merge", "$unionWith"], "$lookup performs a left outer join with another collection."),
        ("hard", "Which aggregation stage outputs one document per element of an array field?", "$unwind", ["$split", "$group", "$flatten"], "$unwind deconstructs an array into separate documents."),
        ("hard", "What is a replica set?", "A group of servers that keep copies of the same data", ["A set of indexes", "A folder of backups", "A shard key"], "Replica sets give redundancy and automatic failover."),
        ("hard", "What is sharding in MongoDB?", "Splitting data across several servers by a shard key", ["Copying data to a backup server", "Compressing documents", "Encrypting a collection"], "Sharding spreads data and load horizontally."),
    ],
    "NoSQL": [
        ("easy", "What do most document databases store records as?", "JSON-like documents", ["Fixed-width text lines", "Spreadsheet cells", "Image files"], "Document stores keep each record as a JSON-like document."),
        ("easy", "Which NoSQL type stores data as key and value pairs?", "Key-value store", ["Graph database", "Relational database", "Document database"], "A key-value store looks up each value by its key."),
        ("easy", "Which of these is a wide-column store?", "Apache Cassandra", ["Redis", "Neo4j", "MongoDB"], "Cassandra groups data into column families."),
        ("easy", "Which of these is a graph database?", "Neo4j", ["Cassandra", "Redis", "DynamoDB"], "Neo4j stores nodes and the relationships between them."),
        ("medium", "What does BASE stand for in NoSQL?", "Basically Available, Soft state, Eventually consistent", ["Balanced, Atomic, Secure, Encrypted", "Binary, Async, Sharded, Embedded", "Basic Access, Simple Execution"], "BASE trades strict consistency for availability."),
        ("medium", "What is eventual consistency?", "All copies become consistent once no new updates arrive", ["Every read always sees the latest write", "Data is never copied", "Writes are rejected under load"], "Replicas may briefly disagree but converge over time."),
        ("medium", "What is denormalization?", "Storing duplicated data together to avoid joins", ["Splitting data into many tables", "Deleting duplicate records", "Encrypting data at rest"], "Denormalized data is faster to read but must be kept in sync."),
        ("medium", "Which use case suits a key-value store such as Redis best?", "Caching and session storage", ["Complex multi-table reports", "Graph traversal", "Relational joins"], "Fast lookups by key make Redis ideal for caches and sessions."),
        ("hard", "What is horizontal scaling?", "Adding more servers to share the load", ["Upgrading one server's CPU and RAM", "Adding columns to a table", "Removing indexes"], "Horizontal scaling grows capacity by adding machines."),
        ("hard", "In a wide-column store, related columns are grouped into...", "column families", ["collections", "nodes and edges", "worksheets"], "Column families hold related columns for each row key."),
        ("hard", "What is a partition (shard) key used for?", "Deciding which node stores each record", ["Encrypting each record", "Sorting query results", "Naming the database"], "The key's value maps each record to a partition."),
        ("hard", "Which read consistency does Amazon DynamoDB use by default?", "Eventually consistent reads", ["Strongly consistent reads only", "No consistency guarantee", "Serializable transactions only"], "Strongly consistent reads must be requested explicitly."),
        ("hard", "During a network partition, a CP system chooses...", "consistency over availability", ["availability over consistency", "neither", "both in full"], "CP systems refuse some requests rather than return stale data."),
    ],
    "Django": [
        ("easy", "Which command starts the development server?", "python manage.py runserver", ["python manage.py start", "django run", "python server.py"], "runserver serves the project on http://127.0.0.1:8000/ by default."),
        ("easy", "Which command creates a new app inside a project?", "python manage.py startapp", ["django-admin newapp", "python manage.py createapp", "pip install app"], "startapp generates the app's files."),
        ("easy", "Which file holds project configuration such as INSTALLED_APPS?", "settings.py", ["config.json", "urls.py", "manage.py"], "settings.py holds the project's configuration."),
        ("easy", "Which command creates an admin account?", "python manage.py createsuperuser", ["python manage.py adduser", "python manage.py admin", "django-admin login"], "createsuperuser makes a user with full admin rights."),
        ("medium", "Which ORM method returns rows matching a condition?", "Model.objects.filter()", ["Model.objects.where()", "Model.objects.find()", "Model.objects.match()"], "filter() returns a QuerySet of matching rows."),
        ("medium", "Which ORM method returns exactly one object and raises an error if none match?", "get()", ["first()", "filter()", "one()"], "get() raises DoesNotExist or MultipleObjectsReturned."),
        ("medium", "Where are a project's apps registered?", "INSTALLED_APPS in settings.py", ["apps.py of each app", "urls.py", "requirements.txt"], "Django loads models and migrations only for installed apps."),
        ("medium", "Which model field stores a date and time?", "DateTimeField", ["DateField", "TimeStampField", "DateTimeColumn"], "DateField stores only a date; DateTimeField adds the time."),
        ("hard", "What does middleware do in Django?", "Processes every request and response globally", ["Defines database tables", "Stores static files", "Writes migrations"], "Middleware hooks run around every view."),
        ("hard", "Which setting lists the host names the site may serve?", "ALLOWED_HOSTS", ["DEBUG_HOSTS", "SITE_HOSTS", "SERVER_NAMES"], "Requests for other hosts are rejected when DEBUG is False."),
        ("hard", "What does select_related() do?", "Fetches related objects in the same query with a SQL join", ["Deletes related objects", "Selects random rows", "Caches the whole table"], "It avoids one extra query per related object."),
        ("hard", "Which DRF setting controls how API errors are formatted?", "EXCEPTION_HANDLER", ["ERROR_VIEW", "DEFAULT_RENDERER_CLASSES", "DEBUG_PROPAGATE"], "A custom exception handler can reshape every error response."),
        ("hard", "Why must DEBUG be False in production?", "Error pages would otherwise expose code and settings", ["The site only runs faster", "Migrations require it", "Static files need it"], "Debug pages show tracebacks and configuration to anyone."),
    ],
    "Docker": [
        ("easy", "Which command downloads an image from a registry?", "docker pull", ["docker get", "docker fetch", "docker download"], "docker pull fetches an image, by default from Docker Hub."),
        ("easy", "Which command builds an image from a Dockerfile?", "docker build", ["docker make", "docker compile", "docker image"], "docker build -t name . builds and tags an image."),
        ("easy", "Which command stops a running container?", "docker stop", ["docker end", "docker quit", "docker halt"], "docker stop sends SIGTERM, then SIGKILL after a timeout."),
        ("easy", "What is Docker Hub?", "A public registry for sharing images", ["A container runtime", "A Dockerfile editor", "A load balancer"], "Docker Hub hosts official and community images."),
        ("medium", "Which Dockerfile instruction copies files from the build context into the image?", "COPY", ["MOVE", "ADDFILE", "IMPORT"], "COPY src dest copies files into the image."),
        ("medium", "Which Dockerfile instruction sets the working directory for later instructions?", "WORKDIR", ["CD", "DIR", "PATH"], "WORKDIR also creates the directory if it is missing."),
        ("medium", "Which tool runs a multi-container app defined in a YAML file?", "Docker Compose", ["Docker Hub", "docker inspect", "Docker Machine"], "docker compose up starts every service in compose.yaml."),
        ("medium", "Which command shows a container's output logs?", "docker logs", ["docker output", "docker print", "docker tail"], "docker logs -f follows the output live."),
        ("hard", "What is the main benefit of a multi-stage build?", "Smaller final images without the build tools", ["Faster container start-up only", "Running several containers at once", "Automatic scaling"], "Only the artefacts copied into the last stage end up in the image."),
        ("hard", "How do CMD and ENTRYPOINT differ?", "ENTRYPOINT sets the executable; CMD gives default arguments that can be overridden", ["They are identical", "CMD runs at build time and ENTRYPOINT at run time", "ENTRYPOINT is only for Windows images"], "docker run arguments replace CMD but are passed to ENTRYPOINT."),
        ("hard", "Why is a .dockerignore file useful?", "It keeps unneeded files out of the build context", ["It hides containers from docker ps", "It ignores failed builds", "It turns off logging"], "A smaller context builds faster and avoids leaking files."),
        ("hard", "Why does the order of Dockerfile instructions affect build speed?", "Docker caches layers, so unchanged early steps are reused", ["Docker sorts instructions alphabetically", "Later instructions run in parallel", "Order only changes the image name"], "Put rarely changing steps, such as installing dependencies, first."),
        ("hard", "Which network lets containers on one host reach each other by container name?", "A user-defined bridge network", ["The none network", "The host network only", "A volume"], "User-defined bridges provide built-in DNS by container name."),
    ],
}


def _build():
    questions, qid = [], 1
    for raw in (_RAW, _RAW_EXTRA):
        for topic in TOPICS:
            for difficulty, text, correct, wrong, why in raw[topic]:
                pos = qid % 4
                options = list(wrong)
                options.insert(pos, correct)
                questions.append(
                    {
                        "id": qid,
                        "topic": topic,
                        "difficulty": difficulty,
                        "question": text,
                        "options": dict(zip(LETTERS, options)),
                        "correct_answer": LETTERS[pos],
                        "explanation": why,
                    }
                )
                qid += 1
    return questions


QUESTIONS = _build()
_BY_ID = {q["id"]: q for q in QUESTIONS}


def get_question(question_id):
    return _BY_ID.get(question_id)
