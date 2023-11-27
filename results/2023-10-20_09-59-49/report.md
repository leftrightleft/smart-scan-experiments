# Smart-scan Analysis Results

![Plot](plot.png)

[Link to full CSV export](export.csv)
## Test Parameters
#### Models:
['gpt-35-turbo-16k']
#### Temperatures:
[0.0]
#### Prompt:

        You are a decision tool responsible for determining whether a static analysis using CodeQL should be performed on a given code diff from a GitHub pull request. Your decisions are based on identifying changes in the source code that could pose security concerns.

        Your criteria for triggering a 'yes' decision are as follows:

        Any addition, removal, or modification of source code should result in a 'yes.'
        Examples of changes that warrant a 'yes' include adding new variables, modifying existing code, or deleting code snippets.
        On the other hand, a 'no' decision should be made if:

        The application's source code remains unaltered.
        Changes only involve non-code elements, such as markdown files or comments.
        Format your response in JSON with the following structure:
        {
          "decision": "yes/no",
          "reason": "Brief explanation for the decision. Keep it to two or three sentences."
        }
        For instance:
        {
          "decision": "no",
          "reason": "The changes involve only modifications to markdown files, which do not impact the operation of the application."
        }
        Ensure that your decision and reason keys are consistently named as 'decision' and 'reason' respectively. Provide clear, concise justifications for your decisions.

        #### START EXAMPLES

        ------ Example Input ------
        diff --git a/index.js b/index.js
        new file mode 100644
        index 0000000..e69de29
        diff --git a/src/main/java/com/github/demo/servlet/BookServlet.java b/src/main/java/com/github/demo/servlet/BookServlet.java
        index 626765c..6dace96 100644
        --- a/src/main/java/com/github/demo/servlet/BookServlet.java
        +++ b/src/main/java/com/github/demo/servlet/BookServlet.java
        @@ -65,7 +65,15 @@ protected void doGet(HttpServletRequest req, HttpServletResponse resp)
                resp.setContentType("text/html; charset=UTF-8");
        
                try {
        -            List<Book> books = bookService.getBooks();
        +            List<Book> books;
        +
        +            String searchTerm = req.getParameter("title");
        +            if (searchTerm != null) {
        +                books = bookService.searchBooks(searchTerm);
        +            } else {
        +                books = bookService.getBooks();
        +            }
        +
                    ctx.setVariable("books", books);
                    engine.process("books", ctx, resp.getWriter());
                } catch (BookServiceException e) {
                
        ------ Example Output ------
        {
          "decision": "yes",
          "reason": "The changes involve new data flows, which could pose security concerns."
        }

        ------ Example Input ------
        diff --git a/README.md b/README.md
        index 828b255..fa0cf3f 100644
        --- a/README.md
        +++ b/README.md
        @@ -1 +1,2 @@
        -# test-python
        \ No newline at end of file
        +# test-python
        +This is just a readme. 

        ------ Example Output ------
        {
          "decision": "no",
          "reason": "The changes involve only modifications to markdown files, which do not impact the operation of the application."
        }

        ------ Example Input ------
        diff --git a/server/routes.py b/server/routes.py
        index d6087dc..97b433a 100644
        --- a/server/routes.py
        +++ b/server/routes.py
        @@ -10,7 +10,7 @@ def index():
            name = request.args.get('name')
            author = request.args.get('author')
            read = bool(request.args.get('read'))
        -
        +    # Check if name exists.  If it does, make a query
            if name:
                cursor.execute(
                    "SELECT * FROM books WHERE name LIKE '%" + name + "%'"
        @@ -27,4 +27,4 @@ def index():
                cursor.execute("SELECT name, author, read FROM books")
                books = [Book(*row) for row in cursor]
        
        -    return render_template('books.html', books=books)
        \ No newline at end of file
        +    return render_template('books.html', books=books)

        ------ Example Output ------
        {
          "decision": "no",
          "reason": "This change only introduces a new comment, which does not impact the operation of the application."
        }
        
        #### END EXAMPLES        
        

## "No" Decision

| directory                   | file                               | model            | decision   | reason                                                                                                                                                                      |
|:----------------------------|:-----------------------------------|:-----------------|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| test-data/diffs_with_alerts | octodemo-ghas-policy-as-code-19    | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files (package-lock.json), which do not impact the operation of the application.                                         |
| test-data/diffs_with_alerts | octodemo-ghas-policy-as-code-17    | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files, such as package-lock.json, which do not impact the operation of the application.                                  |
| test-data/diffs_with_alerts | octodemo-NodeGoat-14               | gpt-35-turbo-16k | no         | The changes involve only modifications to the package-lock.json file, which do not impact the operation of the application.                                                 |
| test-data/diffs_with_alerts | octodemo-demo-ghas-aegilops-14     | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files (package-lock.json), which do not impact the operation of the application.                                         |
| test-data/diffs_with_alerts | octodemo-dependency-review-demo-13 | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files (package-lock.json), which do not impact the operation of the application.                                         |
| test-data/diffs_with_alerts | octodemo-beergoat-16               | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files, such as package-lock.json, which do not impact the operation of the application.                                  |
| test-data/diffs_with_alerts | octodemo-beergoat-20               | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files (package-lock.json), which do not impact the operation of the application.                                         |
| test-data/diffs_with_alerts | octodemo-beergoat-18               | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files (package-lock.json), which do not impact the operation of the application.                                         |
| test-data/diffs_with_alerts | octodemo-demo-ghas-geekmasher-41   | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files, such as package-lock.json, which do not impact the operation of the application.                                  |
| test-data/diffs_with_alerts | octodemo-ghas-policy-as-code-22    | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code files, such as package-lock.json, which do not impact the operation of the application.                                  |
| test-data/diffs_with_alerts | octodemo-forrester-webgoat-2       | gpt-35-turbo-16k | no         | The changes involve only modifications to the GitHub workflow file, which do not impact the operation of the application.                                                   |
| test-data/diffs_with_alerts | octodemo-rails-goat-20             | gpt-35-turbo-16k | no         | The changes involve only modifications to non-code elements, such as the addition of a Rubocop workflow file. These changes do not impact the operation of the application. |
| test-data/diffs_with_alerts | octodemo-NodeGoat-19               | gpt-35-turbo-16k | no         | The changes involve only modifications to the package-lock.json file, which does not impact the operation of the application.                                               |
## Top 10 Token Usage

|   tokens | directory                   | file                                 | model            | decision   | reason                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|---------:|:----------------------------|:-------------------------------------|:-----------------|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    15049 | test-data/diffs_with_alerts | octodemo-Infocus-2022-19             | gpt-35-turbo-16k | yes        | The changes involve updates to package dependencies, which could introduce security vulnerabilities or compatibility issues.                                                                                                                                                                                                                                                                                                                                            |
|    14957 | test-data/diffs_with_alerts | octodemo-NodeGoat-17                 | gpt-35-turbo-16k | yes        | The changes involve modifications to the package.json file, which could impact the dependencies and behavior of the application.                                                                                                                                                                                                                                                                                                                                        |
|    14222 | test-data/diffs             | elastic-logstash-13026               | gpt-35-turbo-16k | yes        | The changes involve modifications to several dependencies, including aws-eventstream, aws-sdk-core, aws-sdk-resources, aws-sdk, aws-sigv4, bindata, concurrent-ruby, dalli, dotenv, ffi, http-cookie, jar-dependencies, jruby-openssl, manticore, march_hare, msgpack, multi_json, nokogiri, pleaserun, racc, sequel, tzinfo-data, and xml-simple. These changes could introduce security vulnerabilities or compatibility issues that should be analyzed using CodeQL. |
|    13728 | test-data/diffs_with_alerts | octodemo-haikus-for-mona-18          | gpt-35-turbo-16k | yes        | The changes involve updates to package dependencies, including the 'mocha' package, which could introduce security vulnerabilities or compatibility issues.                                                                                                                                                                                                                                                                                                             |
|    13279 | test-data/diffs_with_alerts | octodemo-Infocus-2022-20             | gpt-35-turbo-16k | yes        | The changes involve updates to package dependencies, which could introduce security vulnerabilities or compatibility issues.                                                                                                                                                                                                                                                                                                                                            |
|    13174 | test-data/diffs             | elastic-logstash-2751                | gpt-35-turbo-16k | yes        | The changes involve adding new gems to the Gemfile, which could introduce new functionality and potential security vulnerabilities.                                                                                                                                                                                                                                                                                                                                     |
|    13001 | test-data/diffs_with_alerts | octodemo-haikus-for-mona-20          | gpt-35-turbo-16k | yes        | The changes involve updates to package dependencies, including express. It is important to perform a static analysis to ensure that the updated dependencies do not introduce any security vulnerabilities.                                                                                                                                                                                                                                                             |
|    12127 | test-data/diffs             | elastic-logstash-4895                | gpt-35-turbo-16k | yes        | The changes involve modifications to the Gemfile, which could introduce new dependencies or update existing ones. This could potentially impact the security of the application.                                                                                                                                                                                                                                                                                        |
|    11840 | test-data/diffs_with_alerts | octodemo-brokencrystals-48           | gpt-35-turbo-16k | yes        | The changes involve modifications to package-lock.json, which could indicate updates to dependencies that may introduce security vulnerabilities.                                                                                                                                                                                                                                                                                                                       |
|    11219 | test-data/diffs_with_alerts | octodemo-himadri518-code-scanning-41 | gpt-35-turbo-16k | yes        | The changes involve modifications to the go.mod file, which could impact the dependencies and introduce security vulnerabilities.                                                                                                                                                                                                                                                                                                                                       |