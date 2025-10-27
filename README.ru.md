[![en_readme](https://img.shields.io/badge/Readme-in_English-darkblue)](https://github.com/Tarasyonok/pet-project-forum/blob/main/README.md)

# 🌙 Night Coder

> **Место, где разработчики кодят и развиваются вместе**  
> *Потому что код не спит, и мы тоже* 🚀

![CI/CD](https://github.com/Tarasyonok/pet-project-forum/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![Gunicorn](https://img.shields.io/badge/Gunicorn-23.0-green?logo=gunicorn)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.2-purple?logo=bootstrap)
![Ruff](https://img.shields.io/badge/Ruff-14-lightgreen?logo=ruff)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Что такое Night Coder?

**Night Coder** — это полнофункциональная платформа для сообщества разработчиков, созданная для тех волшебных часов,
когда можно заняться своими идеями. Это место, где студенты и увлечённые разработчики собираются вместе, чтобы задавать
вопросы, делиться знаниями и прокачивать навыки.

### ✨ Почему существует Night Coder

- 🕒 **Сообщество** - Всегда есть тот, не спит и готов пообщаться
- 🏆 **Геймификация** - Зарабатывай репутацию и поднимайся в рейтинге
- 🌐 **Два языка** - Поддержка английского и русского
- 🎨 **Красивый интерфейс** - Тёмная тема для ночного программирования
- 🤝 **Настоящие связи** - Прокачай свою карму разработчика

## 🚀 Night Coder Live

### 👉 **[Попробуй Night Coder](https://your-night-coder-app.onrender.com)** 👈

**Демо-доступ (если не хочешь создавать аккаунт):**

- Ник: `DemoUser`
- Email: `demo@nightcoder.com`
- Пароль: `DemoPass123`

## 📸 Скриншоты

<details>
    <summary>🏠 Главная страница</summary><br>
    <img src="/readme_screenshots/home_ru.png" alt="Главная страница" width="100%">
</details>
<details>
    <summary>👤 Профиль пользователя</summary>
    <br> <img src="/readme_screenshots/profile_ru.png" alt="Профиль пользователя" width="100%">
</details>
<details>
    <summary>💬 Форум</summary><br>
    <img src="/readme_screenshots/forum_ru.png" alt="Форум" width="100%">
</details>
<details>
    <summary>📚 Отзывы</summary><br>
    <img src="/readme_screenshots/reviews_ru.png" alt="Отзывы" width="100%">
</details>
<details>
    <summary>🏆 Рейтинги</summary><br>
    <img src="/readme_screenshots/leaderboards_ru.png" alt="Рейтинг" width="100%">
</details>

## 🛠️ Технологии

### **Бэкенд**

- **Python 3.13** - Основной язык программирования
- **Django 5.2** - Веб-фреймворк
- **PostgreSQL 17** - Продакшен база данных

### **Фронтенд**

- **Bootstrap 5** - Адаптивный CSS-фреймворк
- **JavaScript** - Интерактивные функции
- **HTML5 & CSS3** - Современные веб-стандарты

### **DevOps и инструменты**

- **Poetry** - Управление зависимостями и пакетирование
- **Ruff** - Супербыстрый линтер и форматтер для Python
- **Тесты** - Юнит-тесты и интеграционные тесты
- **Git** - Контроль версий с чистой историей коммитов
- **CI/CD** - Автоматические линтинг и тестирование
- **Gunicorn** - WSGI HTTP сервер для продакшена
- **Docker** - Контейнеризация
- **Render** - Платформа для деплоя

## 🎨 Ключевые возможности

### 💬 **Q&A форум**

- Задавай вопросы по программированию и получай ответы
- Система голосования с наградой в виде репутации
- Отмечай ответы как верные
- Полнотекстовый поиск по вопросам и ответам

### ⭐ **Отзывы о курсах**

- Делись впечатлениями о курсах по программированию
- 5-звёздочная система оценок с детальными отзывами
- Голосуй за полезные отзывы
- Поиск по названию курса или технологии

### 🏆 **Система геймификации**

- **Очки репутации** - Зарабатывай за полезный вклад
- **Рейтинги** - Соревнуйся с другими разработчиками
- **Лучшие участники месяца** - Признание для активных членов
- **Статистика в футере** - Контекстный процессор для статистики сообщества на каждой странице

### 👤 **Профили пользователей**

- Загрузка аватара и личное описание
- История активности (вопросы, ответы, отзывы)
- Детализация репутации и статистика
- Небольшая аналитика данных сайта

### 🌐 **Интернационализация**

- Полная поддержка английского и русского языков
- Переключатель языка
- SEO-дружелюбная структура URL

### 🎯 **UX/UI**

- Тёмная тема, оптимизированная для программирования
- Адаптивный дизайн для мобильных устройств
- Доступность и удобная навигация с клавиатуры

## 📁 Структура проекта

```
night-coder/
├── 🔧 core/                # Общие утилиты и миксины
├── 💬 forum/               # Функционал вопросов и ответов
├── 🏠 home/                # Приложение главной страницы
├── 🏆 leaderboards/        # Система геймификации
├── 🌐 locale/              # Файлы переводов
├── ⭐ reviews/             # Отзывы о курсах
├── 🗿 static/              # CSS, JS, изображения
├── 💄 templates/           # Шаблоны Django
├── 👤 users/               # Аутентификация и профили
└── 👍 votes/               # Голосование за контент
```

## 🚀 Быстрый старт

1. **Клонируй репозиторий**
   ```bash
   git clone https://github.com/Tarasyonok/pet-project-forum
   cd pet-project-forum
   ```

2. **Настрой окружение**
   ```bash
   cp .env.example .env
   # Отредактируй .env со своими хостами и секретным ключом
   ```

### Вариант 1: Docker (Рекомендуется)

1. Запусти через Docker
    ```bash
   docker-compose up --build
   ```

### Вариант 2: Традиционная разработка

1. **Настрой виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

2. **Установи зависимости**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Запусти миграции**
   ```bash
   python manage.py migrate
   ```

4. **Создай суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

5. **Запусти сервер для разработки**
   ```bash
   python manage.py runserver
   ```

Перейди на [localhost:8000](http://localhost:8000) и создай свой первый вопрос! 🌙

## 🧪 Тестирование

```bash
python manage.py test
```

## 🔧 Качество кода

```bash
# Линтинг и форматирование кода
ruff check .          # Линтинг
ruff format .         # Форматирование
```

## 🌐 Деплой

Night Coder развёрнут на **Render** с автоматическим CI/CD:

1. **Пуш в main ветку** → Автоматический деплой
2. **build.sh и start.sh** → Скрипты сборки и запуска
3. **Окружение** → Конфигурация для продакшена

## 🤝 Участие в разработке

Мы рады заинтересованными программистами! Вот как ты можешь помочь:

1. **Сделай форк** репозитория
2. **Создай** feature ветку (`git checkout -b feature/amazing-feature`)
3. **Закоммить** изменения (`git commit -m 'Add amazing feature'`)
4. **Запуш** в ветку (`git push origin feature/amazing-feature`)
5. **Открой** Pull Request

### Рекомендации по разработке

- Следуй стилю PEP 8 (используй ruff)
- Пиши тесты для новых функций
- Обновляй документацию
- Используй осмысленные сообщения коммитов с эмодзи

### Если есть какие то замечания/предложения по улучшению, то смело открывай Issue

## 🏆 Достижения

Этот проект демонстрирует мастерство в:

- ✅ **Full-Stack разработке** - Полноценное веб-приложение
- ✅ **Дизайне баз данных** - Сложные связи и оптимизация
- ✅ **Пользовательском опыте** - Интуитивно понятный и приятный интерфейс
- ✅ **DevOps** - CI/CD и облачный деплой
- ✅ **Контейнеризации** - Docker и Docker Compose
- ✅ **Продакшен развертывании** - PostgreSQL, Gunicorn и управление окружением
- ✅ **Интернационализации** - Поддержка нескольких языков
- ✅ **Тестировании и качестве** - Полное покрытие тестами
- ✅ **Производительности** - Быстрая загрузка и эффективные запросы

## 👨‍💻 О разработчике

**Кирилл Тарасов**  
*Full-Stack разработчик*

- ✈️ **Telegram**: [@bravekirty](https://t.me/bravekirty)
- 🐙 **GitHub**: [@Tarasyonok](https://github.com/Tarasyonok)
- 📧 **Email**: bravekirty@gmail.com

[//]: # (- 🌳 **Linktree**: [@bravekirty]&#40;https://linktr.ee/bravekirty&#41;)

[//]: # (- 💼 **LinkedIn**: [Your LinkedIn]&#40;https://linkedin.com/in/your-profile&#41;)

## 📄 Лицензия

Этот проект лицензирован под MIT License - смотри файл [LICENSE](LICENSE) для деталей.

---

<div align="center">

### **Готов присоединиться к нашему ночному сообществу?** 🌙

[![Попробовать Night Coder](https://img.shields.io/badge/Попробовать_Night_Coder-Live-orange?style=for-the-badge)](https://your-night-coder-app.onrender.com)

*⭐ Не забудь поставить звёздочку репозиторию, если он тебе понравился!*

</div>
