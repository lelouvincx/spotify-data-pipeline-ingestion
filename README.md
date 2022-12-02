# Project: Xây dựng data pipeline ELT đơn giản

## 1\. Introduction

Trong project này mình sẽ hướng dẫn xây dựng một data pipeline cơ bản theo mô hình ELT (extract - load - transform), sử dụng bộ dữ liệu từ spotify để phân tích xu hướng nghe nhạc và đưa ra một Flask API cho mục đích sau này.

Project này hoàn thành dựa trên kiến thức đã học được từ khóa Fundamental Data Engineering của AIDE. Xin gửi lời cảm ơn đặc biệt tới thầy Nguyễn Thanh Bình, anh Ông Xuân Hồng và anh Hùng Lê.

## 2\. Objective

Mục tiêu của project này là xây dựng một data pipeline để đưa dữ liệu của bảng `spotify_tracks` từ mySQL và `my_tracks` từ API của Spotify thành dashboard để phân tích. Các bảng được hỗ trợ bởi `spotify_albums` và `spotify_artists` như mô tả dưới đây:

1. `spotify_tracks`: OLTP table chứa thông tin bài hát từ spotify
2. `my_tracks`: lịch sử stream nhạc của bản thân, lấy schema giống `spotify_tracks`
3. `spotify_albums`: chứa thông tin albums từ dataset
4. `spotify_artists`: thông tin nghệ sĩ từ dataset

![](https://i.imgur.com/Hj9mnFH.png)

Chi tiết hơn xem ở: [Exploratory Data Analysis](./EDA.ipynb)

## 3\. Design

Chúng ta sử dụng [dagster](https://dagster.io/) để orchestrate tasks.

1. Dữ liệu spotify được download từ kaggle dưới dạng csv, sau đó import vào mySQL mô phỏng làm dữ liệu doanh nghiệp
2. Dữ liệu streaming history của bản thân được extract từ spotify API
3. Extract 2 nguồn dữ liệu trên bằng pandas để preprocessing (drop duplicates, fill missing values, optimize for analysis (OLAP))
4. Load vào Amazon S3, từ đó load tiếp vào data warehouse (Amazon Redshift) để làm analytics và postgreSQL để làm API
5. Trực quan hóa dữ liệu bằng Metabase và làm API bằng Python Flask

![](https://i.imgur.com/UY2BdAb.png)

## 4\. Setup

### 4.1 Prequisites

Để sử dụng pipeline này, download những phần mềm sau:

1. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Tài khoản gitlab](https://gitlab.com/)
3. [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
4. [Tài khoản AWS](https://aws.amazon.com/)
5. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) và [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
6. [Docker](https://docs.docker.com/engine/install/) ít nhất 4GB RAM và [Docker Compose](https://docs.docker.com/compose/install/) ít nhất v1.29.2

Nếu dùng Windows, setup thêm WSL và một máy ảo local Ubuntu, cài đặt những thứ trên cho ubuntu.

Clone repository

```bash=
git clone https://gitlab.com/lelouvincx/fde01_project_fde220103_dinhminhchinh.git
cd fde01_project_fde220103_dinhminhchinh
```
