# STREAMLIT/core/db.py
import sqlite3
from pathlib import Path
from contextlib import contextmanager

from core.auth import hash_password

DB_PATH = Path("groupware.db")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        schema_path = Path("sql/schema.sql")
        if not schema_path.exists():
            raise FileNotFoundError("sql/schema.sql 파일이 없습니다.")

        # 1) 스키마 생성/갱신
        conn.executescript(schema_path.read_text(encoding="utf-8"))

        # 2) employees 더미 데이터 (비어있을 때만)
        cur = conn.execute("SELECT COUNT(1) AS cnt FROM employees")
        cnt_emp = int(cur.fetchone()["cnt"])
        if cnt_emp == 0:
            conn.execute(
                "INSERT INTO employees(employee_id, name, department, team, ignore_remaining) VALUES (?,?,?,?,?)",
                ("HS001", "김산", "경영관리본부", "재경팀", 3),
            )
            conn.execute(
                "INSERT INTO employees(employee_id, name, department, team, ignore_remaining) VALUES (?,?,?,?,?)",
                ("HS002", "이하나", "연구개발본부", "연구1팀", 3),
            )
            conn.execute(
                "INSERT INTO employees(employee_id, name, department, team, ignore_remaining) VALUES (?,?,?,?,?)",
                ("HS003", "홍길동", "연구개발본부", "연구2팀", 3),
            )

        # 3) accounts 더미 계정 (비어있을 때만)
        cur = conn.execute("SELECT COUNT(1) AS cnt FROM accounts")
        cnt_acc = int(cur.fetchone()["cnt"])
        if cnt_acc == 0:
            # 관리자 계정
            conn.execute(
                """
                INSERT INTO accounts(login_id, password_hash, role, employee_id, created_at)
                VALUES (?,?,?,?,?)
                """,
                ("admin", hash_password("1234"), "ADMIN", None, 0),
            )

            # 직원 계정(아이디=사번)
            conn.execute(
                """
                INSERT INTO accounts(login_id, password_hash, role, employee_id, created_at)
                VALUES (?,?,?,?,?)
                """,
                ("HS001", hash_password("1234"), "EMPLOYEE", "HS001", 0),
            )
            conn.execute(
                """
                INSERT INTO accounts(login_id, password_hash, role, employee_id, created_at)
                VALUES (?,?,?,?,?)
                """,
                ("HS002", hash_password("1234"), "EMPLOYEE", "HS002", 0),
            )
            conn.execute(
                """
                INSERT INTO accounts(login_id, password_hash, role, employee_id, created_at)
                VALUES (?,?,?,?,?)
                """,
                ("HS003", hash_password("1234"), "EMPLOYEE", "HS003", 0),
            )

        # 4) popups 테이블 컬럼 보완 (expected_send_time)
        #    - DB가 이미 만들어진 상태에서도 컬럼이 없으면 추가
        cur = conn.execute("PRAGMA table_info(popups)")
        cols = [row["name"] for row in cur.fetchall()]
        if "expected_send_time" not in cols:
            conn.execute(
                "ALTER TABLE popups ADD COLUMN expected_send_time TEXT NOT NULL DEFAULT '오전 10시'"
            )

        conn.commit()

    finally:
        conn.close()


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
