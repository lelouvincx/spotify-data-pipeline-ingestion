# Project: Xây dựng data pipeline ELT đơn giản

## 1. Introduction

Trong project này mình sẽ hướng dẫn xây dựng một data pipeline cơ bản theo mô hình ELT (extract - load - transform), sử dụng bộ dữ liệu từ spotify để phân tích xu hướng nghe nhạc và đưa ra một Flask API cho mục đích sau này.

Project này hoàn thành dựa trên kiến thức đã học được từ khóa Fundamental Data Engineering của AIDE. Xin gửi lời cảm ơn đặc biệt tới thầy Nguyễn Thanh Bình, anh Ông Xuân Hồng và anh Hùng Lê.

## 2. Objective

Mục tiêu của project này là xây dựng một data pipeline để đưa dữ liệu của bảng `spotify_tracks` từ mySQL và `my_tracks` từ API của Spotify thành dashboard để phân tích. Các bảng được hỗ trợ bởi `spotify_albums` và `spotify_artists` như mô tả dưới đây:

1. `spotify_tracks`: OLTP table chứa thông tin bài hát từ spotify
2. `my_tracks`: lịch sử stream nhạc của bản thân, lấy schema giống `spotify_tracks`
3. `spotify_albums`: chứa thông tin albums từ dataset
4. `spotify_artists`: thông tin nghệ sĩ từ dataset

![](https://i.imgur.com/Hj9mnFH.png)

Chi tiết hơn xem ở: [Exploratory Data Analysis](./EDA.ipynb)

## 3. Design

### 3.1 Pipeline design

Chúng ta sử dụng máy ảo EC2 để tính toán và [dagster](https://dagster.io/) để orchestrate tasks.

1. Dữ liệu spotify được download từ kaggle dưới dạng csv, sau đó import vào mySQL mô phỏng làm dữ liệu doanh nghiệp
2. Dữ liệu streaming history của bản thân được extract từ spotify API
3. Extract 2 nguồn dữ liệu trên bằng pandas để preprocessing (drop duplicates, fill missing values, optimize for analysis (OLAP))
4. Load vào Amazon S3, từ đó load tiếp vào data warehouse (Amazon Redshift) để làm analytics và postgreSQL để làm API
5. Transform dữ liệu bằng dbt trên nền Redshift
6. Trực quan hóa dữ liệu bằng Metabase và làm API bằng Python Flask

![](https://i.imgur.com/vPPWLXr.png)

### 3.2 Data lake structure

Chúng ta sử dụng AWS S3 làm data lake. Mọi dữ liệu trước hết sẽ được chứa ở đây. Trong project này, ta chỉ cần 1 bucket với nhiều thư mục.

![](https://i.imgur.com/G03b0Go.png)

1. **Bronze**: Lưu dữ liệu thô mới lấy về. Chúng là step 1, 2, 3 trong pipeline design
2. **Silver**: Lưu dữ liệu được tiền xử lý. Chúng là step 4 trong pipeline design
3. **Gold**: Lưu dữ liệu sạch khi transform bằng dbt (step 5)

![](https://i.imgur.com/c72VWTu.png)

### 3.3 Directory tree

![](https://i.imgur.com/uQsfWBv.png)

- **docker-compose**: compose các container chạy trong docker
- **EDA**: khám phá dataset và profiling
- **.gitignore**: giúp git không track file (như env, cache, ...)
- **.gitlab-ci**: config quá trình CI trên gitlab
- **Makefile**: thu gọn câu lệnh
- **requirements.txt**: packages python cần thiết và thiết lập virtualenv
- Folder **dagser_home** chứa dagster.yaml để config thành phần dagster còn workspace.yaml để chỉ định dagster chạy host elt_pipeline
- Folder **dockers** chứa file config các container: dagster và jupyter
- Folder **load_dataset** chứa các file dùng để load dữ liệu ban đầu vào mySQL
- Folder **terraform** để khởi tạo và config server trên AWS

Chi tiết cây thư mục xem ở: [tree](./tree.txt).

## 4. Setup

### 4.1 Prequisites

Để sử dụng pipeline này, download những phần mềm sau:

1. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Tài khoản gitlab](https://gitlab.com/)
3. [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
4. [Tài khoản AWS](https://aws.amazon.com/)
5. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) và [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
6. [Docker](https://docs.docker.com/engine/install/) ít nhất 4GB RAM và [Docker Compose](https://docs.docker.com/compose/install/) ít nhất v1.29.2

Nếu dùng Windows, setup thêm WSL và một máy ảo local Ubuntu, cài đặt những thứ trên cho ubuntu.

### 4.2 Setup data infrastructure local

Chạy các lệnh sau để setup infra dưới local:

```bash=
# Clone the repository
git clone https://gitlab.com/lelouvincx/fde01_project_fde220103_dinhminhchinh.git
mv fde01_project_fde220103_dinhminhchinh project
cd project

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

Lúc này sẽ có các container sau đang chạy: mysql, psql, elt_pipeline, dagster_daemon và dagster_dagit.

Bây giờ chúng ta import dataset spotify (dạng csv) vào mySQL:

```bash=
# Enter mysql cli
make to_mysql
```

```sql=
SET GLOBAL local_infile=true;
-- Check if local_infile is turned on
SHOW VARIABLES LIKE "local_infile";
exit
```

Source từng file theo thứ tự:

```bash=
# Create tables with schema
make mysql_create
# Load csv into created tables
make mysql_load
# Set their foreign keys
make mysql_set_foreign_key
```

Testing:

```bash=

```

Truy cập UI của pipeline bằng dagit: https://localhost:3001/

### 4.3 Setup data infrastructure on AWS

1. Chúng ta dùng terraform làm IaC (Infrastructure as Code) để setup hạ tầng trên AWS (nhớ [cấp credential key cho AWS](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build) nhé):

```bash=
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

2. Bây giờ chúng ta truy cập vào EC2 để hoàn tất setup:

```bash=
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

3. Khởi tạo Redshift Serverless

- Truy cập AWS -> Redshift serverless -> Create workgroup
- Nhập các thông tin như trong hình
  ![](https://i.imgur.com/ViwAe5F.png)
  ![](https://i.imgur.com/bQrPMT6.png)
- **Lưu ý:** Chỗ VPC security groups chọn cái có description là "Security group to allow inbound SCP & outbound 8080 (Airflow) connections"
  ![](https://i.imgur.com/0IrR4Vw.png)
  ![](https://i.imgur.com/srXUyaB.png)
  ![](https://i.imgur.com/J8PDlzj.png)
- Giữ nguyên các ô khác rồi chọn **Create**

Sau khi đợi khoảng 5 phút, Redshift sẽ sẵn sàng:
![](https://i.imgur.com/JgGZLbF.png)

Sau đó ta config workgroup để nó có thể truy cập vào database:

- Vào Amazon Redshift Serverless -> Workgroup configuration -> project-spotify-dwh
  ![](https://i.imgur.com/9mpXaUL.png)

- Trong phần Data access, chuyển **publicly accessible** thành on
  ![](https://i.imgur.com/3eBRswv.png)

Sau đó truy cập vào EC2 -> Security Groups -> project-spotify-security-group, thêm Redshift như hình:

![](https://i.imgur.com/t48qVAS.png)

Xong! Chúng ta có thể truy cập Redshift bằng query editor v2.

## 5. Detailed code walkthrough

### 5.1 Extract

### 5.2 Load

### 5.3 Transform

### 5.4 Check results

## 6. Tear down infrastructure

Dỡ bỏ infra sau khi xong việc (_thực hiện dưới máy local_):

```bash=
# Tear down containers
make down

# Tear down AWS
cd terraform
make tf-down
```

**Note:** Lên AWS kiểm tra lại các services sau đã dừng và bị xóa chưa (nếu không muốn mất tiền oan như mình): EC2, S3, Redshift.
