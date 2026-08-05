from pathlib import Path

import duckdb


PROJECT_DIR = Path.cwd()
WORK_DIR = PROJECT_DIR / "work"
PIPELINE_DB = WORK_DIR / "bottleneck.duckdb"


con = duckdb.connect(str(PIPELINE_DB))
cnt_erp = con.execute("SELECT COUNT(*), COUNT(DISTINCT product_id) FROM erp_clean").fetchone()
cnt_web = con.execute("SELECT COUNT(*), COUNT(DISTINCT id_web) FROM web_clean").fetchone()

if cnt_erp[0] != cnt_erp[1]:
	raise ValueError(f"ERREUR TEST: Doublons dans erp_clean ({cnt_erp[0]} != {cnt_erp[1]})")

if cnt_web[0] != cnt_web[1]:
	raise ValueError(f"ERREUR TEST: Doublons dans web_clean ({cnt_web[0]} != {cnt_web[1]})")

if cnt_erp[0] != 825:
	raise ValueError(f"ERREUR TEST: Volume erp_clean ({cnt_erp[0]}) != 825")

if cnt_web[0] != 714:
	raise ValueError(f"ERREUR TEST: Volume web_clean ({cnt_web[0]}) != 714")

con.close()