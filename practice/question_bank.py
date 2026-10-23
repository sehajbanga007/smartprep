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


def _build():
    questions, qid = [], 1
    for topic in TOPICS:
        for difficulty, text, correct, wrong, why in _RAW[topic]:
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
