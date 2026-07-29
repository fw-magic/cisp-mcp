# CISP MCP CentOS 7 离线部署手册

适用环境：联网构建机和离线生产机均为 CentOS 7、`x86_64`、glibc 2.17；运行用户为 `app`；固定目录为 `/ztsoft/usr/wasadm/mcp`。

构建机和生产机必须使用相同绝对路径，因为 Python 虚拟环境会记录解释器路径。

## 1. 运行方式

```text
客户 Agent
  │ HTTPS + Authorization: Bearer <客户CISP_API_KEY>
  ▼
Nginx / API Gateway
  ▼
cisp-mcp
  │ X-API-Key: <客户CISP_API_KEY>
  ▼
CISP API（按客户Key计费）
```

- 生产服务器不保存统一的 `CISP_API_KEY`。
- HTTP 模式从每次请求的 Bearer Token取得客户 Key。
- 本地 stdio 模式才从 `.env` 或环境变量读取 `CISP_API_KEY`。
- 缺少或格式错误的 Bearer Key返回 `401`。
- 客户之间不能复用 MCP Session。

## 2. 首次准备联网构建机

以下命令以 `root` 执行。

### 2.1 基础工具和目录

```bash
yum install -y curl git tar gzip ca-certificates
update-ca-trust

MCP_BASE=/ztsoft/usr/wasadm/mcp

install -d -o app -g "$(id -gn app)" \
  "$MCP_BASE/bin" \
  "$MCP_BASE/cache" \
  "$MCP_BASE/python" \
  "$MCP_BASE/src" \
  "$MCP_BASE/package"
```

### 2.2 安装 uv

```bash
MCP_BASE=/ztsoft/usr/wasadm/mcp
UV_VERSION=0.11.32

curl -LsSf \
  "https://astral.sh/uv/${UV_VERSION}/install.sh" \
  -o /tmp/uv-install.sh

sudo -u app env \
  UV_INSTALL_DIR="$MCP_BASE/bin" \
  UV_NO_MODIFY_PATH=1 \
  sh /tmp/uv-install.sh

"$MCP_BASE/bin/uv" --version
```

`UV_NO_MODIFY_PATH=1` 可避免安装器修改 app 用户不可写的 `/ztapp/.profile`。

### 2.3 安装 Python 3.11

```bash
sudo -u app env \
  UV_CACHE_DIR="$MCP_BASE/cache" \
  UV_PYTHON_INSTALL_DIR="$MCP_BASE/python" \
  UV_PYTHON_INSTALL_BIN=0 \
  "$MCP_BASE/bin/uv" \
  python install 3.11 --no-bin
```

### 2.4 克隆项目

```bash
MCP_PROJECT="$MCP_BASE/src/cisp-mcp"

sudo -u app git clone \
  https://github.com/fw-magic/cisp-mcp.git \
  "$MCP_PROJECT"
```

## 3. 联网构建、验证和打包

每次发布都执行本章。必须使用已提交的 tag 或 commit，不要打包未提交代码。

### 3.1 切换发布版本

```bash
set -euo pipefail

MCP_BASE=/ztsoft/usr/wasadm/mcp
MCP_PROJECT="$MCP_BASE/src/cisp-mcp"
MCP_PACKAGE="$MCP_BASE/package"

sudo -u app git -C "$MCP_PROJECT" fetch --tags --prune origin
sudo -u app git -C "$MCP_PROJECT" checkout <tag-or-commit>

git -C "$MCP_PROJECT" status --short
git -C "$MCP_PROJECT" rev-parse HEAD
```

`git status --short` 必须为空。

### 3.2 按锁文件构建

```bash
cd "$MCP_PROJECT"

sudo -u app env \
  UV_CACHE_DIR="$MCP_BASE/cache" \
  UV_PYTHON_INSTALL_DIR="$MCP_BASE/python" \
  UV_PYTHON_INSTALL_BIN=0 \
  "$MCP_BASE/bin/uv" \
  sync \
  --frozen \
  --python 3.11 \
  --no-editable \
  --reinstall-package cisp-mcp
```

不要在生产机运行 `uv add`、`uv lock` 或 `pip install`。

### 3.3 验证

```bash
sudo -u app \
  "$MCP_PROJECT/.venv/bin/python" \
  -m unittest discover -s tests -v

sudo -u app \
  "$MCP_PROJECT/.venv/bin/python" \
  scripts/smoke_test_mcp.py
```

预期：

```text
Ran 58 tests
OK
Total: 25
Smoke test passed.
```

smoke test 不调用真实 CISP，不产生查询费用。

### 3.4 制作离线包

```bash
COMMIT_SHORT="$(git -C "$MCP_PROJECT" rev-parse --short=12 HEAD)"
BUILD_TIME="$(date +%Y%m%d%H%M%S)"
RELEASE_ID="${BUILD_TIME}-${COMMIT_SHORT}"
ARTIFACT="cisp-mcp-centos7-x86_64-${RELEASE_ID}.tar.gz"

tar \
  --exclude='mcp/src/cisp-mcp/.git' \
  --exclude='.env*' \
  --exclude='*.pem' \
  --exclude='*.key' \
  --exclude='.pytest_cache' \
  --exclude='.mypy_cache' \
  --exclude='.ruff_cache' \
  --exclude='*/__pycache__' \
  --exclude='*.pyc' \
  -C /ztsoft/usr/wasadm \
  -czf "$MCP_PACKAGE/$ARTIFACT" \
  mcp/bin \
  mcp/python \
  mcp/src/cisp-mcp
```

生成清单和校验文件：

```bash
{
  echo "release_id=$RELEASE_ID"
  echo "commit=$(git -C "$MCP_PROJECT" rev-parse HEAD)"
  echo "git_ref=$(git -C "$MCP_PROJECT" describe --tags --always --dirty)"
  echo "build_time=$(date --iso-8601=seconds)"
  echo "builder=$(hostname)"
  echo "os=$(cat /etc/redhat-release)"
  echo "arch=$(uname -m)"
  echo "glibc=$(ldd --version | head -1)"
  echo "uv=$("$MCP_BASE/bin/uv" --version)"
  echo "python=$("$MCP_PROJECT/.venv/bin/python" --version 2>&1)"
} > "$MCP_PACKAGE/${ARTIFACT}.manifest"

cd "$MCP_PACKAGE"
sha256sum "$ARTIFACT" > "${ARTIFACT}.sha256"
sha256sum -c "${ARTIFACT}.sha256"
ls -lh "$ARTIFACT" "${ARTIFACT}.sha256" "${ARTIFACT}.manifest"
```

上传三个文件到生产机的 `/ztsoft/usr/wasadm/mcp-deploy/`：

```text
<artifact>.tar.gz
<artifact>.tar.gz.sha256
<artifact>.tar.gz.manifest
```

## 4. 首次配置生产机

### 4.1 目录

```bash
install -d -o root -g root -m 0750 \
  /ztsoft/usr/wasadm/mcp-deploy \
  /ztsoft/usr/wasadm/mcp-backups

install -d -o app -g "$(id -gn app)" \
  /ztsoft/usr/wasadm/mcp
```

### 4.2 运行配置

```bash
APP_GROUP="$(id -gn app)"

install -d -o root -g "$APP_GROUP" -m 0750 /etc/cisp-mcp
install -o root -g "$APP_GROUP" -m 0640 /dev/null \
  /etc/cisp-mcp/cisp-mcp.env
```

编辑 `/etc/cisp-mcp/cisp-mcp.env`：

```ini
CISP_ENDPOINT=https://cisp.zenitera.com
CISP_REQUEST_URI=/ectcispserver/api/entcreditapi/query
CISP_ENDPOINT_PROXY=http://proxy.example.internal:8080
CISP_TIMEOUT_SECONDS=30
CISP_VERIFY_SSL=true

MCP_HOST=127.0.0.1
MCP_PORT=8000
```

- 不使用代理时删除 `CISP_ENDPOINT_PROXY` 或设置为空。
- 支持 `http://` 和 `socks5://` 代理。
- 不要配置生产统一 `CISP_API_KEY`。
- 如果代理 URL含账号密码，环境文件必须保持 `0640`。

测试代理：

```bash
curl -Iv \
  --connect-timeout 10 \
  --proxy http://proxy.example.internal:8080 \
  https://cisp.zenitera.com
```

### 4.3 systemd

创建 `/etc/systemd/system/cisp-mcp.service`：

```ini
[Unit]
Description=CISP MCP Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=app
WorkingDirectory=/ztsoft/usr/wasadm/mcp/src/cisp-mcp
EnvironmentFile=/etc/cisp-mcp/cisp-mcp.env
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONDONTWRITEBYTECODE=1
ExecStart=/ztsoft/usr/wasadm/mcp/src/cisp-mcp/.venv/bin/cisp-mcp --transport streamable-http
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=full
ProtectHome=true
CapabilityBoundingSet=

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable cisp-mcp
```

## 5. 生产发布或升级

将 `ARTIFACT` 替换成实际文件名。

### 5.1 校验

```bash
set -euo pipefail

MCP_BASE=/ztsoft/usr/wasadm/mcp
DEPLOY_DIR=/ztsoft/usr/wasadm/mcp-deploy
BACKUP_ROOT=/ztsoft/usr/wasadm/mcp-backups
ARTIFACT='cisp-mcp-centos7-x86_64-实际版本.tar.gz'

cd "$DEPLOY_DIR"
sha256sum -c "${ARTIFACT}.sha256"
cat "${ARTIFACT}.manifest"
tar -tzf "$ARTIFACT" | sed -n '1,30p'
```

只有校验结果为 `OK` 才能继续。

### 5.2 停止并备份

```bash
systemctl stop cisp-mcp

DEPLOY_TIME="$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$DEPLOY_TIME"
install -d -o root -g root -m 0750 "$BACKUP_DIR"

for NAME in bin python src; do
  if [ -e "$MCP_BASE/$NAME" ]; then
    mv "$MCP_BASE/$NAME" "$BACKUP_DIR/$NAME"
  fi
done

echo "BACKUP_DIR=$BACKUP_DIR"
```

记录输出的 `BACKUP_DIR`，回滚时需要。

### 5.3 解压并离线验证

```bash
tar \
  --no-same-owner \
  -xzf "$DEPLOY_DIR/$ARTIFACT" \
  -C /ztsoft/usr/wasadm

chown -R app:"$(id -gn app)" \
  "$MCP_BASE/bin" \
  "$MCP_BASE/python" \
  "$MCP_BASE/src"

MCP_PROJECT="$MCP_BASE/src/cisp-mcp"

"$MCP_PROJECT/.venv/bin/python" --version
"$MCP_PROJECT/.venv/bin/cisp-mcp" --help

sudo -u app \
  "$MCP_PROJECT/.venv/bin/python" \
  -m unittest discover -s tests -v

sudo -u app \
  "$MCP_PROJECT/.venv/bin/python" \
  scripts/smoke_test_mcp.py
```

### 5.4 启动

```bash
systemctl start cisp-mcp
systemctl status cisp-mcp --no-pager
journalctl -u cisp-mcp -n 100 --no-pager
```

无 Key请求必须返回 `401`：

```bash
curl -s \
  -o /dev/null \
  -w '%{http_code}\n' \
  http://127.0.0.1:8000/mcp
```

最后通过测试客户 Key执行一次真实低成本查询，确认代理、鉴权和计费正常。

## 6. Nginx/API Gateway

生产入口必须使用 HTTPS。Nginx 不保存客户 Key，只原样转发 Authorization。

```nginx
location /mcp {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;

    proxy_set_header Host 127.0.0.1:8000;
    proxy_set_header Authorization $http_authorization;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Connection "";

    proxy_buffering off;
    proxy_request_buffering off;
    proxy_cache off;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
}
```

```bash
nginx -t
systemctl reload nginx
```

要求：

- 不记录 `Authorization`、`X-API-Key` 或查询敏感参数。
- 对来源 IP配置连接数和请求频率限制。
- 不要直接向公网开放 `8000`。

## 7. 客户端配置

### Claude Code

```bash
export CISP_API_KEY='<客户自己的CISP_API_KEY>'
```

项目 `.mcp.json`：

```json
{
  "mcpServers": {
    "cisp-mcp": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${CISP_API_KEY}"
      }
    }
  }
}
```

### Codex

`~/.codex/config.toml`：

```toml
[mcp_servers.cisp-mcp]
url = "https://mcp.example.com/mcp"
bearer_token_env_var = "CISP_API_KEY"
startup_timeout_sec = 20
tool_timeout_sec = 120
enabled = true
```

```bash
export CISP_API_KEY='<客户自己的CISP_API_KEY>'
```

### WorkBuddy

```json
{
  "mcpServers": {
    "cisp-mcp": {
      "type": "streamable-http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <客户自己的CISP_API_KEY>"
      },
      "disabled": false
    }
  }
}
```

WorkBuddy 未确认支持环境变量展开时，使用凭据输入框或直接填写 Key。

## 8. 回滚

将 `BACKUP_DIR` 替换为发布时记录的目录。

```bash
set -euo pipefail

MCP_BASE=/ztsoft/usr/wasadm/mcp
BACKUP_DIR=/ztsoft/usr/wasadm/mcp-backups/<备份时间>
FAILED_DIR=/ztsoft/usr/wasadm/mcp-backups/failed-$(date +%Y%m%d%H%M%S)

systemctl stop cisp-mcp
install -d -o root -g root -m 0750 "$FAILED_DIR"

for NAME in bin python src; do
  if [ -e "$MCP_BASE/$NAME" ]; then
    mv "$MCP_BASE/$NAME" "$FAILED_DIR/$NAME"
  fi
  mv "$BACKUP_DIR/$NAME" "$MCP_BASE/$NAME"
done

chown -R app:"$(id -gn app)" \
  "$MCP_BASE/bin" \
  "$MCP_BASE/python" \
  "$MCP_BASE/src"

systemctl start cisp-mcp
systemctl status cisp-mcp --no-pager
journalctl -u cisp-mcp -n 100 --no-pager
```

## 9. 后续代码和依赖更新

只修改代码：提交后在联网构建机切换到新 tag/commit，重新执行第 3、5 章。

新增依赖只能在开发机或联网构建机执行：

```bash
MCP_BASE=/ztsoft/usr/wasadm/mcp
MCP_PROJECT="$MCP_BASE/src/cisp-mcp"

cd "$MCP_PROJECT"

sudo -u app env \
  UV_CACHE_DIR="$MCP_BASE/cache" \
  UV_PYTHON_INSTALL_DIR="$MCP_BASE/python" \
  UV_PYTHON_INSTALL_BIN=0 \
  "$MCP_BASE/bin/uv" \
  add '<package-name>>=<min-version>,<max-version>'

git diff -- pyproject.toml uv.lock

sudo -u app env \
  UV_CACHE_DIR="$MCP_BASE/cache" \
  UV_PYTHON_INSTALL_DIR="$MCP_BASE/python" \
  UV_PYTHON_INSTALL_BIN=0 \
  "$MCP_BASE/bin/uv" \
  sync --frozen --python 3.11 --no-editable

sudo -u app \
  "$MCP_PROJECT/.venv/bin/python" \
  -m unittest discover -s tests -v

sudo -u app \
  "$MCP_PROJECT/.venv/bin/python" \
  scripts/smoke_test_mcp.py
```

提交 `pyproject.toml` 和 `uv.lock`。MCP SDK约束必须保持：

```toml
mcp[cli]>=1.27.2,<2
```

当前项目不使用 Pillow，不要为了重建环境临时加入 Pillow。新增二进制依赖时，必须确认支持 `manylinux2014_x86_64` 或 `manylinux_2_17_x86_64`。

## 10. 常用排查

```bash
systemctl status cisp-mcp --no-pager
journalctl -u cisp-mcp -n 200 --no-pager
ss -lntp | grep ':8000'
free -h
df -h /ztsoft/usr/wasadm
```

| 现象 | 检查 |
| --- | --- |
| `.profile: Permission denied` | uv 已安装成功时可忽略；以后使用 `UV_NO_MODIFY_PATH=1` |
| `401` | 客户端是否发送 `Authorization: Bearer <CISP_API_KEY>` |
| 工具可列出但真实调用失败 | 客户 Key、`CISP_ENDPOINT_PROXY`、DNS、防火墙 |
| `421 Invalid Host header` | Nginx设置 `Host 127.0.0.1:8000` |
| `Address already in use` | 停止现有服务后再运行 smoke test |
| `bad interpreter` | 构建机和生产机绝对路径必须相同 |

CentOS 7 已停止安全维护。本方案适合作为过渡部署，公网 TLS入口应放在仍受支持的网关系统上。
