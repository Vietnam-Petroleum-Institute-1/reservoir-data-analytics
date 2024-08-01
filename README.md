data_analyst_base
==============================

A short description of the project.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │   ├───1.0_Old             the creator's initials, and a short `-` delimited description, e.g.
    │   │   ├───catboost_info   `1.0-jqp-initial-data-exploration`.
    │   │   │   ├───learn
    │   │   │   └───tmp
    │   │   └───petro
    │   │       └───__pycache__
    │   ├───catboost_info
    │   │   ├───learn
    │   │   └───tmp
    │   ├───CORE
    │   │   ├───PERM
    │   │   ├───PHI
    │   │   ├───SW
    │   │   └───VCL
    │   │       └───catboost_info
    │   │           ├───learn
    │   │           └───tmp
    │   └───EXPLAIN
    │       ├───PERM
    │       ├───PHI
    │       ├───SW
    │       └───VCL                      
    │                         
    │   
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

--------

Base dự án
------------

    ├── LICENSE
    ├── Makefile           <- Makefile với các lệnh như `make data` hoặc `make train`
    ├── README.md          <- File README cấp cao nhất cho các nhà phát triển sử dụng dự án này.
    ├── data
    │   ├── external       <- Dữ liệu từ nguồn bên thứ ba.
    │   ├── interim        <- Dữ liệu trung gian đã được chuyển đổi.
    │   ├── processed      <- Bộ dữ liệu cuối cùng và chuẩn cho mô hình.
    │   └── raw            <- Dữ liệu gốc, không thể thay đổi.
    │
    ├── docs               <- Một dự án Sphinx mặc định; xem sphinx-doc.org để biết chi tiết.
    │
    ├── models             <- Các mô hình được huấn luyện và được serialize, các dự đoán của mô hình hoặc tóm tắt mô hình.
    │
    ├── notebooks          <- Jupyter notebooks. Quy ước đặt tên là số (để sắp xếp), tên viết tắt của người tạo và mô tả ngắn được phân tách bằng dấu `-`, ví dụ: `1.0-jqp-initial-data-exploration`.
    │   ├───1.0_Old
    │   │   ├───catboost_info
    │   │   │   ├───learn
    │   │   │   └───tmp
    │   │   └───petro
    │   │       └───__pycache__
    │   ├───catboost_info
    │   │   ├───learn
    │   │   └───tmp
    │   ├───CORE
    │   │   ├───PERM
    │   │   ├───PHI
    │   │   ├───SW
    │   │   └───VCL
    │   │       └───catboost_info
    │   │           ├───learn
    │   │           └───tmp
    │   └───EXPLAIN
    │       ├───PERM
    │       ├───PHI
    │       ├───SW
    │       └───VCL
    ├── references         <- Từ điển dữ liệu, hướng dẫn và tất cả các tài liệu giải thích khác.
    │
    ├── reports            <- Phân tích được tạo ra dưới dạng HTML, PDF, LaTeX, v.v.
    │   └── figures        <- Đồ họa và hình ảnh được tạo ra để sử dụng trong báo cáo.
    │
    ├── requirements.txt   <- Tệp yêu cầu để sao chép môi trường phân tích, ví dụ: được tạo ra với `pip freeze> requirements.txt`
    │
    ├── setup.py           <- làm cho dự án có thể cài đặt được pip (pip install -e .) để src có thể được nhập vào.
    ├── src                <- Mã nguồn được sử dụng trong dự án này.
    │   ├── __init__.py    <- Làm cho src trở thành một module Python.
    │   │
    │   ├── data           <- Kịch bản để tải xuống hoặc tạo ra dữ liệu.
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Kịch bản để chuyển đổi dữ liệu gốc thành các tính năng để mô hình hóa.
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Kịch bản để huấn luyện mô hình và sau đó sử dụng các mô hình đã huấn luyện để đưa ra dự đoán.
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- là thư mục chứa các script để tạo các trực quan hóa cho mục đích khám phá và hiển thị kết qu
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
