# Электронная система контроля отсутствующих в Лицее  
Запущена на http://92.53.124.98:8000  
Приложение https://github.com/thecattest/lyceum-reports-android
## Идея  
В нашем лицее ежедневно отслеживаются отсутствующие ученики. Для этого два дежурных ученика ходят по школе и собирают списки отсутствующих, после чего записывают результаты в бумажную таблицу.  
Идея этого проекта заключается в полной оцифровке процесса. Я написал WEB-систему, в которой можно отмечать отсутствующих и просматривать актуальную информацию в разных представлениях. Доступ к ней осуществляется по интернету. На данный момент она запущена на моем VDS сервере. В случае, если всё сложится, впереди этап тестирования в школе, а также доработки, диктуемые реальными практическими условиями. В данный момент готово MVP. Открывать систему можно как с компьютера, так и с телефонов, верстка адаптивная.

## Реализация  
### Главная страница  
На главной странице - сводка, в виде карточек представлена краткая актуальная информация. Одна карточка - один класс. На карточке цифра и буква класса, отсутствующие за сегодня и за вчера, кнопка `дополнить` и кнопка `подробнее`.  
![](https://user-images.githubusercontent.com/57992909/117179991-64c56300-addc-11eb-9f03-7b7ca29f95ca.png)
### Таблицы
Два вида таблиц на отдельных страницах - за класс и за день. В таблице за класс отображаются отсутствующие в каждый конкретный день в выбранном классе, в таблице за день - отсутствующие в каждом классе за выбранный день.  
#### Таблица за класс 
Показывает список отсутствующих в классе за последние 50 дней  
Открывается при нажатии кнопки `подробнее` на карточке класса на главной странице
![](https://user-images.githubusercontent.com/57992909/117180127-84f52200-addc-11eb-926d-f855a2680dd0.png)
#### Таблица за день
Показывает сводку отсутствующих во всех классах за день  
Ссылка находится в шапке главной страницы  
![](https://user-images.githubusercontent.com/57992909/117180417-d69dac80-addc-11eb-9d7d-421f8be549cf.png)
### Страница отсутствующих  
На странице заполнения отсутствующих - буква и номер класса, дата, список учеников. При нажатии на строчку с учеником он отмечается как отсутствующий, после выбора всех необходимо подтвердить отправку зеленой кнопкой внизу.  
Кнопка `Очистить` просто снимает весь выбор на клиенте, никаких изменений в базе не происходит.  
При смене даты автоматически отмечаются выбранные ранее ученики, если информация уже вносилась.  
Страница открывается при нажатии кнопки `дополнить`/`заполнить` на карточке класса на главной.  
Кстати, при переходе по ссылке `заполнить` сразу открывается вчерашний или сегодняшний день, в зависимости от местонахождения кнопки.
![](https://user-images.githubusercontent.com/57992909/117180606-0351c400-addd-11eb-8b65-7b0c77182e1e.png)
![](https://user-images.githubusercontent.com/57992909/117180661-15cbfd80-addd-11eb-92f9-30a6b354e1b0.png)
### Аккаунты  
Доступ к системе только с аккаунтами, так что существует ещё и страница авторизации.  
![](https://user-images.githubusercontent.com/57992909/117181027-7bb88500-addd-11eb-8a41-af98f6b362b3.png)
Существует 3 типа аккаунтов:  
#### Админ - может смотреть все классы, таблицы и всё редактировать `thecattest` / `superpass`  
![](https://user-images.githubusercontent.com/57992909/117179991-64c56300-addc-11eb-9f03-7b7ca29f95ca.png)
#### Редактор - может смотреть и редактировать только один класс, который ему открыт `editor` / `editor`  
![](https://user-images.githubusercontent.com/57992909/117181246-b0c4d780-addd-11eb-9b5c-46467839fb06.png)
#### Руководитель - смотрит всё, трогать ничего нельзя `viewer` / `viewer`  
![](https://user-images.githubusercontent.com/57992909/117181147-98ed5380-addd-11eb-9e15-7333134327e7.png)

## Технологии
### Серверная часть написана на Python3.6 с использованием следующих библиотек:
* `Flask` + `Flask_RESTful`
* `SQLAlchemy`
* `PyMySQL` для подключения к базе данных MySQL
### База данных  
`MySQL` на отдельном сервере, в проекте используется `ORM SQLAlchemy`. 
### Фронт 
* `HTML5`
* `CSS3` + `Bootstrap`
* `Vue.js` + `Axios`  
  
Сервер одновременно отвечает на запросы к api, обработчики которых вынесены в отдельный blueprint, и сервит html страницы.  
На страницах динамически подгружается актуальная информация посредством Axios, за отрисовку элементов и взаимодействие отвечает Vue.js.
