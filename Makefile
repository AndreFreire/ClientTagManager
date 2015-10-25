app:
	cd django/ClientTagManager/ && cookiecutter https://github.com/rpedigoni/cookiecutter-django-app

test:
	coverage run --branch --source=django/ClientTagManager  django/ClientTagManager/./manage.py test django/ClientTagManager/ -v 2 --failfast --settings=settings.test
	coverage report --omit=django/ClientTagManager/*/migrations*,django/ClientTagManager/settings/*,django/ClientTagManager/urls.py,django/ClientTagManager/wsgi.py,django/ClientTagManager/manage.py,django/ClientTagManager/*/tests/*,django/ClientTagManager/__init__.py

html:
	coverage html --omit=django/ClientTagManager/*/migrations*,django/ClientTagManager/settings/*,django/ClientTagManager/urls.py,django/ClientTagManager/wsgi.py,django/ClientTagManager/manage.py,django/ClientTagManager/*/tests/*,django/ClientTagManager/__init__.py
	open htmlcov/index.html

doc:
	$(MAKE) -C docs/ html
	open docs/build/html/index.html

deploy:
	fab -f django/fabfile.py deploy

clean:
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf docs/build/