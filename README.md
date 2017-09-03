# translation-app
This is a translation app built with Django and AngularJS.

The name of this app is **Salvē** (from the Latin word for *hello*). You can view the live project [here][1]. I implemented it with the following technologies:


- Backend/Rest Framework: Django (Django Rest Framework)
- Frontend Framework: AngularJS
- Language detection and translation: Yandex
- Hosting: ElasticBeanstalk (AWS)
- Database: Postgres
- Version control: Github

## How It Works

Using this app is simple. Just type a text value into the input box on the homepage, select a target language, and submit.

The translation request is sent as a POST to the backend. The server then constructs and issues a URL request to the Yandex API. The Yandex API takes the text and automatically detects the originating language. It then translates to the desired language based on the user input. Django takes the result from this request, constructs a new translation and saves it to the database. 

Finally, the response is serialized and sent back to the client. If there is no error, the client is automatically redicted to another page, where she can view the input, the detected language, the target language and the resulting translation.

Lastly, the user can view all previous translations via the History page, accessiable from the link in the header.

[1]: http://translator.us-west-2.elasticbeanstalk.com


