FROM python:3.11.9


WORKDIR /tools


COPY ./requirements.txt /tools/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /tools/requirements.txt


COPY ./crawling /tools/crawling

CMD ["fastapi", "run", "crawling/app/crawl_api.py", "--port", "80"]