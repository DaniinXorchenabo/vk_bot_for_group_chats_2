FROM python:3.8
LABEL maintainer="rkbcu@mail.ru"
RUN pip install --upgrade pip && pip install pymorphy2 && pip install vk_api && pip install regex && pip install --user -U nltk && pip install pony
COPY . /.
EXPOSE 80
CMD ["python", "./main.py"]