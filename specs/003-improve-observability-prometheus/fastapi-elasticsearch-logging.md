# 將 FastAPI 日誌傳送到 Elasticsearch 的設置指南

本文檔描述如何將 FastAPI 應用程序的日誌傳送到 Elasticsearch，以便通過 Kibana 進行可視化和分析。

## 架構概述

我們使用以下組件來實現日誌收集和分析：

1. **FastAPI 應用程序**：生成結構化 JSON 日誌
2. **Docker JSON 日誌驅動**：收集容器的 stdout/stderr 輸出
3. **Filebeat**：從 Docker 日誌文件收集日誌並轉發到 Elasticsearch
4. **Elasticsearch**：存儲和索引日誌數據
5. **Kibana**：可視化和分析日誌數據

## 設置步驟

### 1. FastAPI 日誌配置

FastAPI 應用程序已配置為使用結構化 JSON 日誌格式。關鍵實現在 `logging_config.py` 中：

- `JSONLogFormatter` 類將日誌記錄格式化為結構化 JSON
- 日誌包含請求 ID、項目 ID、方法、路徑、狀態碼和響應時間等元數據
- 所有日誌都輸出到標準輸出 (stdout)

### 2. Docker 配置

在 `docker-compose.observability.yml` 中，我們配置 backend 服務使用 JSON 日誌驅動：

```yaml
backend:
  # ... 其他配置 ...
  logging:
    driver: "json-file"
    options:
      tag: "{{.Name}}"
```

### 3. Filebeat 配置

Filebeat 設置為從 Docker 容器日誌文件收集日誌：

```yaml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    json.keys_under_root: true
    json.add_error_key: true
    processors:
      # ... 處理器配置 ...

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  indices:
    - index: "alertingscout-%{+yyyy.MM.dd}"
      when.contains:
        service.name: "alertingscout"
```

## 使用方法

### 在代碼中記錄日誌

在 FastAPI 應用程序的任何部分使用標準 Python 日誌記錄：

```python
import logging
logger = logging.getLogger(__name__)

# 記錄不同級別的日誌
logger.debug("調試信息")
logger.info("信息性消息")
logger.warning("警告消息")
logger.error("錯誤消息")
logger.exception("帶有堆棧跟蹤的錯誤")
```

### 查看日誌

1. 訪問 Kibana 界面：<http://localhost:5601>
2. 創建索引模式：
   - 在側邊欄中點擊 "Stack Management"
   - 選擇 "Index Patterns"
   - 點擊 "Create index pattern"
   - 輸入 `alertingscout-*` 作為模式
   - 選擇 `@timestamp` 作為時間字段
   - 點擊 "Create index pattern"

3. 查看日誌：
   - 在側邊欄中點擊 "Discover"
   - 從下拉菜單中選擇 `alertingscout-*` 索引模式
   - 使用時間過濾器和搜索欄來過濾日誌

### 常用搜索查詢

在 Kibana 的搜索欄中，您可以使用以下查詢：

- 查詢錯誤日誌：`level:ERROR`
- 查詢特定端點：`path:"/todos"`
- 查詢特定請求 ID：`request_id:"abc123"`
- 查詢慢響應：`duration_ms:>500`

## 定制和擴展

### 添加更多日誌字段

在 `logging_config.py` 的 `JSONLogFormatter` 類中添加更多字段：

```python
log_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "service": getattr(record, "service", "alertingscout"),
    "level": record.levelname,
    "message": record.getMessage(),
    "logger": record.name,
    "host": socket.gethostname(),
    # 添加新字段
    "environment": os.environ.get("ENVIRONMENT", "development"),
}
```

### 創建 Kibana 儀表板

1. 在 Kibana 中點擊 "Dashboard"
2. 點擊 "Create dashboard"
3. 添加可視化組件來展示：
   - 按日誌級別的日誌計數
   - 按端點的請求計數
   - 按時間的請求響應時間
   - 錯誤率趨勢

## 故障排除

### 無法看到日誌

- 確認 FastAPI 應用程序正在產生日誌
- 檢查 Filebeat 配置是否正確
- 檢查 Elasticsearch 索引是否存在：`curl http://localhost:9200/_cat/indices`
- 檢查 Filebeat 日誌：`docker logs alertingscout-filebeat-1`

### Filebeat 失敗

- 確保 Filebeat 有權限讀取 Docker 日誌文件
- 檢查 Filebeat 配置是否有語法錯誤
- 確保 Elasticsearch 可訪問
