### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
  A relational database management system.

- What is the difference between SQL and PostgreSQL?
  PostgreSQL offers more language support than SQL, such as Python.

- In `psql`, how do you connect to a database?
  \c 'database name'

- What is the difference between `HAVING` and `WHERE`?
  `HAVING` checks conditions after the aggregation takes place.
  `WHERE` checks conditions before the aggregation takes place.

- What is the difference between an `INNER` and `OUTER` join?
  `INNER` join only consider the attributes from tables that we want to match and ignores the rest.
  `OUTER` join will consider the whole table and all of its attributes, join them, and leave unmatched fields from both tables null.

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
  `LEFT OUTER` join considers the whole left table. The unmatched attributes of the left table will be null in the right table fields.

  `RIGHT OUTER` join considers the whole right table. The unmatched attributes of the right table will be null in the left table fields.

- What is an ORM? What do they do?
  Object Relational Mapping. It allows you to manipulate data with code instead of using SQL.

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?
  AJAX does not make the page reload when a response is receive, an HTTP request does.

- What is CSRF? What is the purpose of the CSRF token?
  Cross-Site Request Forgery: Malicious sites that mimic legitimate sites collect cookie information from a user's browser. A randomly generated cookie that can only be authenticated be the owner and the site it was requested from to keep sensitive data safe.

- What is the purpose of `form.hidden_tag()`?
  This keeps sensitive data fields hidden when typing information.