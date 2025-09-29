#!/usr/bin/env python3

import requests
import json
import time
import random
import datetime
import concurrent.futures
import logging
import argparse
import sys
from typing import Dict, List, Optional, Any

# 設定日誌格式，方便 ELK 堆疊分析
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s"}',
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(__name__)


class ApiLoadTest:
    def __init__(self, base_url: str = "http://localhost:8000", request_interval: float = 0.5):
        """
        初始化負載測試
        :param base_url: API 的基礎 URL
        :param request_interval: 每次請求之間的間隔時間 (秒)
        """
        self.base_url = base_url
        self.request_interval = request_interval
        self.session = requests.Session()
        self.todo_ids = []
        self.project_ids = []

    def run_test(self, duration_minutes: int = 5):
        """
        運行負載測試
        :param duration_minutes: 測試持續時間 (分鐘)
        """
        logger.info(f"Starting load test for {duration_minutes} minutes with request interval {self.request_interval}s")

        end_time = time.time() + (duration_minutes * 60)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while time.time() < end_time:
                futures = []

                # 測試根端點
                futures.append(executor.submit(self.test_root_endpoint))

                # 測試專案端點
                futures.append(executor.submit(self.test_projects_endpoints))

                # 測試待辦事項端點
                futures.append(executor.submit(self.test_todos_endpoints))

                # 測試錯誤案例
                if random.random() < 0.2:  # 20% 機率測試錯誤案例
                    futures.append(executor.submit(self.test_error_cases))

                # 等待所有請求完成
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as exc:
                        logger.error(f"Generated an exception: {exc}")

                # 等待指定間隔
                time.sleep(self.request_interval)

        logger.info("Load test completed")

    def test_root_endpoint(self):
        """測試根端點"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/")
            elapsed = time.time() - start_time
            self._log_request("GET", "/", response.status_code, elapsed)
            return response.json()
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("GET", "/", str(e), elapsed)
            return None

    def test_projects_endpoints(self):
        """測試專案相關端點"""
        # 50% 機率創建新專案
        if random.random() < 0.5 or not self.project_ids:
            self._create_project()

        # 獲取專案列表
        self._get_projects()

        # 如果有專案，50% 機率獲取單個專案
        if self.project_ids and random.random() < 0.5:
            project_id = random.choice(self.project_ids)
            self._get_project(project_id)

            # 30% 機率更新專案
            if random.random() < 0.3:
                self._update_project(project_id)

    def test_todos_endpoints(self):
        """測試待辦事項相關端點"""
        # 40% 機率創建新待辦事項
        if random.random() < 0.4 or not self.todo_ids:
            self._create_todo()

        # 獲取待辦事項列表
        self._get_todos()

        # 如果有待辦事項，40% 機率獲取單個待辦事項
        if self.todo_ids and random.random() < 0.4:
            todo_id = random.choice(self.todo_ids)
            self._get_todo(todo_id)

            # 30% 機率更新待辦事項
            if random.random() < 0.3:
                self._update_todo(todo_id)

            # 10% 機率刪除待辦事項
            elif random.random() < 0.1:
                self._delete_todo(todo_id)

    def test_error_cases(self):
        """測試錯誤案例"""
        error_tests = [
            lambda: self._get_project("nonexistent"),
            lambda: self._get_todo("nonexistent"),
            lambda: self._create_project(invalid=True),
            lambda: self._create_todo(invalid=True),
        ]

        # 隨機選擇一個錯誤測試
        random.choice(error_tests)()

    def _create_project(self, invalid: bool = False):
        """創建專案"""
        if invalid:
            data = {"wrong_field": "Invalid Project"}
        else:
            data = {
                "name": f"Project {random.randint(1000, 9999)}",
                "description": f"Test project created at {datetime.datetime.now().isoformat()}",
            }

        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/projects", json=data, headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start_time
            self._log_request("POST", "/projects", response.status_code, elapsed)

            if response.status_code == 200:
                project = response.json()
                self.project_ids.append(project.get("id"))
                return project
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("POST", "/projects", str(e), elapsed)

        return None

    def _get_projects(self):
        """獲取專案列表"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/projects")
            elapsed = time.time() - start_time
            self._log_request("GET", "/projects", response.status_code, elapsed)

            if response.status_code == 200:
                projects = response.json()
                # 更新專案 ID 列表，但保留已有的 ID
                for project in projects:
                    if project.get("id") not in self.project_ids:
                        self.project_ids.append(project.get("id"))
                return projects
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("GET", "/projects", str(e), elapsed)

        return None

    def _get_project(self, project_id: str):
        """獲取單個專案"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/projects/{project_id}")
            elapsed = time.time() - start_time
            self._log_request("GET", f"/projects/{project_id}", response.status_code, elapsed)

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("GET", f"/projects/{project_id}", str(e), elapsed)

        return None

    def _update_project(self, project_id: str):
        """更新專案"""
        data = {
            "name": f"Updated Project {random.randint(1000, 9999)}",
            "description": f"Updated at {datetime.datetime.now().isoformat()}",
        }

        start_time = time.time()
        try:
            response = self.session.put(
                f"{self.base_url}/projects/{project_id}", json=data, headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start_time
            self._log_request("PUT", f"/projects/{project_id}", response.status_code, elapsed)

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("PUT", f"/projects/{project_id}", str(e), elapsed)

        return None

    def _create_todo(self, invalid: bool = False):
        """創建待辦事項"""
        if invalid:
            data = {"wrong_field": "Invalid Todo"}
        else:
            # 如果有專案，50% 機率將待辦事項與專案關聯
            project_id = random.choice(self.project_ids) if self.project_ids and random.random() < 0.5 else None

            data = {
                "title": f"Todo {random.randint(1000, 9999)}",
                "description": f"Test todo created at {datetime.datetime.now().isoformat()}",
                "priority": random.choice(["low", "medium", "high"]),
                "status": random.choice(["pending", "in_progress", "completed"]),
                "due_date": (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).isoformat(),
            }

            if project_id:
                data["project_id"] = project_id

        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/todos", json=data, headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start_time
            self._log_request("POST", "/todos", response.status_code, elapsed)

            if response.status_code == 200:
                todo = response.json()
                self.todo_ids.append(todo.get("id"))
                return todo
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("POST", "/todos", str(e), elapsed)

        return None

    def _get_todos(self):
        """獲取待辦事項列表"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/todos")
            elapsed = time.time() - start_time
            self._log_request("GET", "/todos", response.status_code, elapsed)

            if response.status_code == 200:
                todos = response.json()
                # 更新待辦事項 ID 列表，但保留已有的 ID
                for todo in todos:
                    if todo.get("id") not in self.todo_ids:
                        self.todo_ids.append(todo.get("id"))
                return todos
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("GET", "/todos", str(e), elapsed)

        return None

    def _get_todo(self, todo_id: str):
        """獲取單個待辦事項"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/todos/{todo_id}")
            elapsed = time.time() - start_time
            self._log_request("GET", f"/todos/{todo_id}", response.status_code, elapsed)

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("GET", f"/todos/{todo_id}", str(e), elapsed)

        return None

    def _update_todo(self, todo_id: str):
        """更新待辦事項"""
        data = {
            "title": f"Updated Todo {random.randint(1000, 9999)}",
            "description": f"Updated at {datetime.datetime.now().isoformat()}",
            "priority": random.choice(["low", "medium", "high"]),
            "status": random.choice(["pending", "in_progress", "completed"]),
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).isoformat(),
        }

        start_time = time.time()
        try:
            response = self.session.put(
                f"{self.base_url}/todos/{todo_id}", json=data, headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start_time
            self._log_request("PUT", f"/todos/{todo_id}", response.status_code, elapsed)

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("PUT", f"/todos/{todo_id}", str(e), elapsed)

        return None

    def _delete_todo(self, todo_id: str):
        """刪除待辦事項"""
        start_time = time.time()
        try:
            response = self.session.delete(f"{self.base_url}/todos/{todo_id}")
            elapsed = time.time() - start_time
            self._log_request("DELETE", f"/todos/{todo_id}", response.status_code, elapsed)

            if response.status_code == 200:
                # 從列表中移除已刪除的待辦事項 ID
                if todo_id in self.todo_ids:
                    self.todo_ids.remove(todo_id)
                return {"success": True}
        except Exception as e:
            elapsed = time.time() - start_time
            self._log_error("DELETE", f"/todos/{todo_id}", str(e), elapsed)

        return None

    def _log_request(self, method: str, endpoint: str, status_code: int, elapsed: float):
        """記錄 API 請求"""
        logger.info(
            json.dumps(
                {
                    "type": "API request",
                    "method": method,
                    "endpoint": endpoint,
                    "status_code": status_code,
                    "response_time": round(elapsed, 4),
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            )
        )

    def _log_error(self, method: str, endpoint: str, error: str, elapsed: float):
        """記錄 API 錯誤"""
        logger.error(
            json.dumps(
                {
                    "type": "API error",
                    "method": method,
                    "endpoint": endpoint,
                    "error": error,
                    "response_time": round(elapsed, 4),
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load testing tool for AlertingScout API")
    parser.add_argument("duration", nargs="?", type=int, default=5, help="Test duration in minutes (default: 5)")
    parser.add_argument(
        "interval", nargs="?", type=float, default=0.5, help="Request interval in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--url", type=str, default="http://localhost:8000", help="API base URL (default: http://localhost:8000)"
    )

    args = parser.parse_args()

    print(f"Starting load test for {args.duration} minutes with request interval {args.interval}s")

    load_tester = ApiLoadTest(base_url=args.url, request_interval=args.interval)
    load_tester.run_test(duration_minutes=args.duration)
