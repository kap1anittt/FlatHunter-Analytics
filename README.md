# FlatHunter-Analytics
CIAN Flat Prices: Parsing, ETL, EDA, A/B Tests, ml

**FlatHunter-Analytics** — аналитический проект по анализу цен на квартиры на платформе CIAN. В проекте реализованы этапы ETL, EDA, A/B тестирования и машинное обучение.

## 📁 Структура проекта

FlatHunter-Analytics/
├── AB test/
│   ├── Product-Market_Fit.ipynb
│   └── data.csv
├── analysis/
│   ├── eda.ipynb
│   └── cleaned_data.csv
├── Analyze_core/
│   ├── Core_Metric.ipynb
│   └── data.csv
├── data/
│   └── data.csv
├── data_cleaning/
│   ├── cleaning_data.ipynb
│   └── cian_rent.csv
├── ml/
│   ├── model.ipynb
│   └── data.csv
├── parsing/
│   └── cian_parser.py
├── dashboard/
├── LICENSE
└── README.md


## 🔄 Описание этапов

### 1. Сбор и парсинг данных
- Используется скрипт `parsing/cian_parser.py` для сбора данных с сайта CIAN.

### 2. Очистка и подготовка данных
- Очистка и предобработка — в `data_cleaning/`.

### 3. Анализ данных (EDA)
- Разведочный анализ и визуализации находятся в `analysis/`.

### 4. A/B тестирование
- Результаты экспериментов анализируются в `AB test/`.

A/B тест выявил:

значимую и существенную разницу между двумя локациями,

что позволяет сегментировать рынок и по-разному таргетировать маркетинг, продукт и стратегию ценообразования.

### 5. Ключевые метрики
- Расчёт и анализ метрик — в `Analyze_core/`.

### 6. Машинное обучение
- Модели для предсказания цен за м^2 квартир — в `ml/`.

## Начать работу

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/FlatHunter-Analytics.git
   cd FlatHunter-Analytics