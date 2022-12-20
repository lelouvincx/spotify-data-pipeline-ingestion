# Project: Xây dựng data pipeline ELT đơn giản

Trong project này mình sẽ hướng dẫn xây dựng một data pipeline cơ bản theo mô hình ELT (extract - load - transform), sử dụng bộ dữ liệu từ spotify để phân tích xu hướng nghe nhạc.

Project này hoàn thành dựa trên kiến thức đã học được từ khóa Fundamental Data Engineering của AIDE. Xin gửi lời cảm ơn đặc biệt tới thầy Nguyễn Thanh Bình, anh Ông Xuân Hồng và anh Hùng Lê.

Chi tiết nội dung project xem [ở đây](https://lelouvincx.github.io/projects/fde_project/)

## Pipeline design

Chúng ta sử dụng máy ảo EC2 để tính toán và [dagster](https://dagster.io/) để orchestrate tasks.

1. Dữ liệu spotify được download từ kaggle dưới dạng csv, sau đó import vào mySQL mô phỏng làm dữ liệu doanh nghiệp
2. Dữ liệu streaming history của bản thân được extract từ spotify API
3. Extract 2 nguồn dữ liệu trên bằng pandas để preprocessing (optimize size consumed)
4. Load vào Amazon S3, từ đó load tiếp vào data warehouse (PostgreSQL) để làm analytics
5. Transform dữ liệu bằng dbt trên nền PostgreSQL
6. Trực quan hóa dữ liệu bằng Metabase

![](https://i.imgur.com/GmFNVht.jpg)

## Setup

### 1. Prequisites

Để sử dụng pipeline này, download những phần mềm sau:

1. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Tài khoản gitlab](https://gitlab.com/)
3. [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
4. [Tài khoản AWS](https://aws.amazon.com/)
5. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) và [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
6. [Docker](https://docs.docker.com/engine/install/) ít nhất 4GB RAM và [Docker Compose](https://docs.docker.com/compose/install/) ít nhất v1.29.2

Nếu dùng Windows, setup thêm WSL và một máy ảo local Ubuntu, cài đặt những thứ trên cho ubuntu.

### 2. Setup data infrastructure local

Clone repository:

```bash
git clone https://gitlab.com/lelouvincx/fde01_project_fde220103_dinhminhchinh.git
mv fde01_project_fde220103_dinhminhchinh project
cd project

# Create env file
touch env
cp env.template env
```

Điền các biến môi trường vào file env.

Chạy các lệnh sau để setup infra dưới local:

```bash
# Setup python packages
make install

# Build docker images
make build

# Run locally
make up

# Check running containers
docker ps

# Check code quality
make check
make lint

# Use black to reformat if any tests failed, then try again
black ./elt_pipeline

# Test coverage
make test
```

Lúc này sẽ có 7 services sau đang chạy:

![](https://i.imgur.com/5XuJ4o2.png)

Bây giờ chúng ta import dataset spotify (dạng csv) vào mySQL:

```bash
# Enter mysql cli
make to_mysql
```

```sql
SET GLOBAL local_infile=true;
-- Check if local_infile is turned on
SHOW VARIABLES LIKE "local_infile";
exit
```

Source từng file theo thứ tự:

```bash
# Create tables with schema
make mysql_create
# Load csv into created tables
make mysql_load
# Set their foreign keys
make mysql_set_foreign_key
```

Khởi tạo schema và table trong psql:

```bash
# Enter psql cli
make psql_create
```

Testing:

```bash
# Test utils
python -m pytest -vv --cov=utils elt_pipeline/tests/utils
# Test ops
python -m pytest -vv --cov=ops elt_pipeline/tests/ops
```

Truy cập giao diện của pipeline bằng dagit: https://localhost:3001/

### 3. Setup data infrastructure on AWS

1. Chúng ta dùng terraform làm IaC (Infrastructure as Code) để setup hạ tầng trên AWS (nhớ [cấp credential key cho AWS](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build) nhé)

```bash
cd terraform

# Initialize infra
make tf-init

# Checkout planned infra
make tf-plan

# Build up infra
make tf-up
```

Đợi một chút để setup xong. Chúng ta lên [Amazon Web Services](aws.amazon.com)

- Trong EC2 sẽ thấy 1 máy ảo tên project-spotify-EC2
  ![](https://i.imgur.com/M514qT5.png)
- Trong S3 thấy 1 bucket tên project-spotify-bucket
  ![](https://i.imgur.com/0vxMqf0.png)

Sau khi project-spotify-EC2 hiện đã pass hết status thì chúng ta đã setup thành công.

2. Bây giờ chúng ta truy cập vào EC2 để hoàn tất setup

```bash
# Connect to EC2 from local terminal
make ssh-ec2
# Generate new ssh key for gitlab
ssh-keygen
# Then press Enter until done
cat ~/.ssh/id_rsa.pub
```

- Copy đoạn mã SSH
- Vào gitlab, phía trên góc phải có hình avatar -> Preferences -> SSH Keys -> paste key vừa copy vào -> đặt tên là 'project-spotify-vm' -> Add key
- Vào terminal của EC2 (vừa connect lúc nãy), clone về bằng SSH
- Lặp lại bước setup infra local đã trình bày ở phần trên

3. Cấp access point cho S3 bucket

## Tear down infrastructure

Dỡ bỏ infra sau khi xong việc (_thực hiện dưới máy local_):

```bash
# Tear down containers
make down

# Tear down AWS
cd terraform
make tf-down
```

**Note:** Lên AWS kiểm tra lại các services sau đã dừng và bị xóa chưa (nếu không muốn mất tiền oan như mình): EC2, S3.

## Design considerations

Sau khi deploy thành công pipeline, giờ là lúc đánh giá project.

1. **Tốc độ**: Tốc độ extract data khá chậm (vì load vào `pandas.DataFrame` 2 lần). Một số giải pháp thay thế: [polars](https://pola-rs.github.io/polars-book/user-guide/introduction.html?fbclid=IwAR0ERGiDoExMbnvby9_HprvCFGAA1AMrDvrtghJ5Ql88pYXONA5rZ902bD4), json, ...
2. **Kích thước**: Chuyện gì sẽ xảy ra khi data lớn lên gấp 10x, 100x, 1000x? Lúc đấy ta cần xem xét các giải pháp giúp lưu trữ big data, thay đổi data warehouse thành Amazon RDS, Google BigQuery, ...
3. **Môi trường phát triển**: Khi project có thêm nhiều người cùng sử dụng là cũng là lúc phân chia môi trường thành testing, staging, production.

## Further actions

1. **Tăng lượng data**: Tích hợp nhiều data hơn từ Spotify API: Khi ingest bài hát mới, ingest luôn thông tin về artist, album, tạo thành hệ sinh thái bài hát đầy đủ.
2. **Stream ingestion**: Dùng một tech stack khác cho job API theo hướng streaming. Hệ thống sẽ listen mỗi lần nghe xong bài hát là tự động cập nhật vào pipeline.
3. **My wrap-up**: Tự thực hành phân tích dữ liệu như tính năng wrap-up của spotify.
4. **Recommender system**: Thực hành làm một hệ thống gợi ý dựa trên những bài đã nghe.
