Date: 2016-03-07
Title: django源码阅读笔记
Slug: django-source-code-explore-note
Tags: django


Open edX的后端采用Django来写，Django是一个大而全的web框架，许多地方和Rails相似

Open edX对Django框架做了大量的改造，对其特性的应用也是十分全面。由于时常需要去hack Open edX，以至于不得不深入到Django源码本身，读别人的源码，和大多事情一样，都符合万事开头难的规律，深入之后，其乐无穷.

>初极狭，才通人，复行数十步，豁然开朗

Open edX的最新稳定版所依赖的Django版本为1.8.7，所以我主要阅读的也是这个版本的源码:[Django 1.8.7](https://github.com/django/django/tree/1.8.7)

下面下阅读过程一些值得记录的地方记下来

#django-admin
安装django后，我们会获得一个命令行工具`django-admin`，用于创建django项目和djangoapp

这主要是通过[entry_points](https://github.com/django/django/blob/1.8.7/setup.py#L47)实现

```
:::text
entry_points={'console_scripts': [
        'django-admin = django.core.management:execute_from_command_line',
    ]},
```

通过entry_points,我们可以将python函数注册到系统，这对于用python写系统应用十分有用

#request
首先来看看[HttpRequest](https://github.com/django/django/blob/1.8.7/django%2Fhttp%2Frequest.py#L42)

```python
        self.GET = QueryDict(mutable=True)
        self.POST = QueryDict(mutable=True)
```

###QueryDict
request的两个GET和POST属性是[QueryDict](https://github.com/django/django/blob/1.8.7/django%2Fhttp%2Frequest.py#L316).
QueryDict集成自[MultiValueDict](https://github.com/django/django/blob/1.8.7/django%2Futils%2Fdatastructures.py#L285)

MultiValueDict来自[django/django/utils/datastructures.py](https://github.com/django/django/blob/1.8.7/django%2Futils%2Fdatastructures.py),是django为自身打造的一种抽象数据结构，这个抽象数据结构主要是为了解决这个问题

>    This class exists to solve the irritating problem raised by cgi.parse_qs,which returns a list for every key, even though most Web forms submitsingle name-value pairs.


###MultiPartParser
[MultiPartParser](https://github.com/django/django/blob/1.8.7/django/http/multipartparser.py#L45)类的主要作用是：

>  Multi-part parsing for file uploads.

---

更多的可用属性和方法参考:[Request and response objects](https://docs.djangoproject.com/en/1.8/ref/request-response/)


#response
[HttpResponse](https://github.com/django/django/blob/1.8.7/django/http/response.py#L330)

>    An HTTP response class with a string as content.
     This content that can be read, appended to or replaced.

###JsonResponse
[django/django/http/response.py JsonResponse](https://github.com/django/django/blob/1.8.7/django/http/response.py#L517)

```
:::text
class JsonResponse(HttpResponse):
		...
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder)
        super(JsonResponse, self).__init__(content=data, **kwargs)
```

#middleware
>  Middleware is a framework of hooks into Django’s request/response processing. It’s a light, low-level “plugin” system for globally altering Django’s input or output.

我们关注一下几个middleware

```python
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
```

###[SessionMiddleware](https://github.com/django/django/blob/1.8.7/django/contrib/sessions/middleware.py#L9)

#####process_request



```python
	
    def __init__(self):
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(session_key)
```

#####process_response

>process_response() is called on all responses before they’re returned to the browser.  


```python
                        response.set_cookie(settings.SESSION_COOKIE_NAME,
                                request.session.session_key, max_age=max_age,
                                expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                path=settings.SESSION_COOKIE_PATH,
                                secure=settings.SESSION_COOKIE_SECURE or None,
                                httponly=settings.SESSION_COOKIE_HTTPONLY or None)
```

###[CommonMiddleware](https://github.com/django/django/blob/1.8.7/django%2Fmiddleware%2Fcommon.py#L16)
使用条件分支来过滤非法客户端

```python
        if 'HTTP_USER_AGENT' in request.META:
            for user_agent_regex in settings.DISALLOWED_USER_AGENTS:
                if user_agent_regex.search(request.META['HTTP_USER_AGENT']):
                    logger.warning('Forbidden (User agent): %s', request.path,
                        extra={
                            'status_code': 403,
                            'request': request
                        }
                    )
                    return http.HttpResponseForbidden('<h1>Forbidden</h1>')
```

ETag header的处理也在CommonMiddleware

###[CsrfViewMiddleware](https://github.com/django/django/blob/1.8.7/django/middleware/csrf.py#L76)
#####process_view
```python
        if getattr(callback, 'csrf_exempt', False):
            return None
```

callback come from `def process_view(self, request, callback, callback_args, callback_kwargs):`,callback是装饰器？

###[AuthenticationMiddleware](https://github.com/django/django/blob/master/django%2Fcontrib%2Fauth%2Fmiddleware.py#L14)
#####process_request
```python
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: get_user(request))
```

注意断言（assert）的使用，这里设置了request.user,并且

>The Django authentication middleware requires session middleware


###get_user
[get_user](https://github.com/django/django/blob/1.8.7/django%2Fcontrib%2Fauth%2F__init__.py#L159)


#backends
###[ModelBackend](https://github.com/django/django/blob/1.8.7/django%2Fcontrib%2Fauth%2Fbackends.py#L7)
By default, AUTHENTICATION_BACKENDS is set to:	`['django.contrib.auth.backends.ModelBackend']`

###CASBackend
look at [CASBackend](https://github.com/wwj718/django-cas/blob/wwj/1.2.0/cas/backends.py#L218)

#storage system

###qiniu

#参考
*  [django/django](https://github.com/django/django/tree/1.8.7)
*  [Django documentation 1.8](https://docs.djangoproject.com/en/1.8/)
*  [djangobook](http://www.djangobook.com/en/2.0/index.html)
	*  [中文版](http://djangobook.py3k.cn/2.0/)
*  [Appendix G: Request and Response Objects](http://www.djangobook.com/en/2.0/appendixG.html)
	*  [中文版](http://djangobook.py3k.cn/appendixH/)
*  [Django documentation Middleware](https://docs.djangoproject.com/en/1.8/topics/http/middleware/)
*  [Customizing authentication in Django](https://docs.djangoproject.com/en/1.9/topics/auth/customizing/)
*  [Writing a custom storage system](https://docs.djangoproject.com/en/1.9/howto/custom-file-storage/)
