CREATE TABLE oauth_users (
    id SERIAL PRIMARY KEY,                       -- Внутренний уникальный идентификатор пользователя
    oauth_provider_user_id TEXT NOT NULL,       -- ID пользователя из OAuth провайдера
    oauth_provider TEXT NOT NULL,              -- Название провайдера (facebook, twitter, tiktok)
    created_at TIMESTAMP DEFAULT NOW()         -- Время создания записи
);

-- Индекс для быстрого поиска по паре oauth_provider_user_id + oauth_provider
CREATE UNIQUE INDEX idx_oauth_user_provider ON oauth_users(oauth_provider_user_id, oauth_provider);

-- Таблица для хранения жалоб
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,                   -- Уникальный идентификатор жалобы
    user_first_name TEXT NOT NULL,           -- Имя пользователя
    user_last_name TEXT NOT NULL,            -- Фамилия пользователя
    complaint_description TEXT NOT NULL,               -- Описание жалобы
    location_coords GEOGRAPHY(POINT),        -- Координаты местоположения (геометрия)
    severity TEXT NOT NULL,                  -- Уровень серьезности (Low, Medium, High, Critical)
    impact_estimation TEXT NOT NULL,         -- Масштаб проблемы (Personal, City/Town, State, Country, Earth)
    problem_status TEXT NOT NULL,            -- Статус проблемы (Ongoing, Resolved, Worsened, Pending Review)
    created_at TIMESTAMP DEFAULT NOW(),      -- Дата создания жалобы
    updated_at TIMESTAMP DEFAULT NOW(),      -- Дата последнего обновления
    metadata JSONB                           -- Дополнительные метаданные (например, "source", "tokenized")
);

-- Индексы для ускорения запросов
CREATE INDEX idx_complaints_severity ON complaints(severity);
CREATE INDEX idx_complaints_impact_estimation ON complaints(impact_estimation);
CREATE INDEX idx_complaints_problem_status ON complaints(problem_status);
CREATE INDEX idx_complaints_location_id ON complaints(location_id);

CREATE TABLE session_complaints (
    id SERIAL PRIMARY KEY,                   -- Уникальный идентификатор записи
    session_id TEXT NOT NULL,                -- ID сессии GPT
    user_id INT REFERENCES oauth_users(id) ON DELETE CASCADE,
    complaint_id INT NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()       -- Время создания записи
);

-- Индексы для оптимизации
CREATE INDEX idx_session_id ON session_complaints(session_id);
CREATE INDEX idx_user_id ON session_complaints(user_id);
CREATE INDEX idx_complaint_id ON session_complaints(complaint_id);

-- Таблица для хранения гибких данных о времени
CREATE TABLE complaint_time (
    id SERIAL PRIMARY KEY,                        -- Уникальный идентификатор записи
    complaint_id INT NOT NULL REFERENCES complaints(id) ON DELETE CASCADE, -- Связь с жалобой
    type TEXT NOT NULL,                           -- Тип времени (exact, date, date_range, и т.д.)
    exact_timestamp TIMESTAMP,                    -- Для "exact" типа: точное время
    date DATE,                                    -- Для "date" типа: конкретная дата
    start_date DATE,                              -- Для "date_range" и "datetime_range": начальная дата
    end_date DATE,                                -- Для "date_range" и "datetime_range": конечная дата
    start_datetime TIMESTAMP,                     -- Для "datetime_range": начальное время с датой
    end_datetime TIMESTAMP,                       -- Для "datetime_range": конечное время с датой
    time_interval TEXT,                           -- Для "time_interval": часть дня (morning, evening)
    approx_period TEXT,                           -- Для "approx_period": текстовое представление периода (e.g., "January 2025")
    created_at TIMESTAMP DEFAULT NOW()            -- Дата и время создания записи
);

-- Индексы для ускорения запросов
CREATE INDEX idx_complaint_time_complaint_id ON complaint_time(complaint_id);
CREATE INDEX idx_complaint_time_type ON complaint_time(type);


-- Создаем таблицу location_directory
CREATE TABLE location_directory (
    id SERIAL PRIMARY KEY,          -- Уникальный идентификатор
    location_details TEXT NOT NULL, -- Детали локации (город, район, ориентир и т.д.)
    latitude FLOAT8,                -- Широта
    longitude FLOAT8,               -- Долгота
    city TEXT,                      -- Город
    region TEXT,                    -- Регион
    country TEXT,                   -- Страна
    created_at TIMESTAMP DEFAULT NOW() -- Дата и время создания записи
);

-- Создаем индекс для быстрого поиска по полю location_details
CREATE UNIQUE INDEX idx_location_details ON location_directory(location_details);


-- Создаем таблицу dictionary_problem_categories для категорий проблем
CREATE TABLE dictionary_problem_categories (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL UNIQUE,      -- Название категории
    created_at TIMESTAMP DEFAULT NOW()  -- Дата создания записи
);

-- Создаем таблицу complaint_problem_categories для связи жалоб с категориями
CREATE TABLE complaint_problem_categories (
    id SERIAL PRIMARY KEY,
    complaint_id INT NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,  -- Связь с жалобой
    category_id INT NOT NULL REFERENCES dictionary_problem_categories(id) ON DELETE CASCADE, -- Связь с категорией
    created_at TIMESTAMP DEFAULT NOW()                                      -- Дата создания записи
);

-- Создаем таблицу dictionary_related_events для связанных событий
CREATE TABLE dictionary_related_events (
    id SERIAL PRIMARY KEY,
    event_name TEXT NOT NULL UNIQUE,    -- Название связанного события
    created_at TIMESTAMP DEFAULT NOW()  -- Дата создания записи
);

-- Создаем таблицу complaint_related_events для связи жалоб с событиями
CREATE TABLE complaint_related_events (
    id SERIAL PRIMARY KEY,
    complaint_id INT NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,  -- Связь с жалобой
    event_id INT NOT NULL REFERENCES dictionary_related_events(id) ON DELETE CASCADE, -- Связь с событием
    created_at TIMESTAMP DEFAULT NOW()                                      -- Дата создания записи
);

-- Эмбеддинги для категорий проблем
CREATE TABLE problem_category_embeddings (
    id SERIAL PRIMARY KEY,
    category_id INT NOT NULL REFERENCES dictionary_problem_categories(id) ON DELETE CASCADE, -- Ссылка на словарь категорий
    embedding VECTOR(384) NOT NULL, -- Эмбеддинг категории
    created_at TIMESTAMP DEFAULT NOW() -- Дата создания записи
);

-- Эмбеддинги для связанных событий
CREATE TABLE related_event_embeddings (
    id SERIAL PRIMARY KEY,
    event_id INT NOT NULL REFERENCES dictionary_related_events(id) ON DELETE CASCADE, -- Ссылка на словарь событий
    embedding VECTOR(384) NOT NULL, -- Эмбеддинг события
    created_at TIMESTAMP DEFAULT NOW() -- Дата создания записи
);

-- Создаем индексы для ускорения поиска
CREATE INDEX idx_complaint_problem_categories_complaint_id ON complaint_problem_categories(complaint_id);
CREATE INDEX idx_complaint_problem_categories_category_id ON complaint_problem_categories(category_id);

CREATE INDEX idx_complaint_related_events_complaint_id ON complaint_related_events(complaint_id);
CREATE INDEX idx_complaint_related_events_event_id ON complaint_related_events(event_id);
