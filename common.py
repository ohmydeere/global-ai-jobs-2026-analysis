# -*- coding: utf-8 -*-
"""公共模块：数据加载、清洗、派生特征与绘图样式配置。"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------- 路径
def _find_root() -> Path:
    """定位项目根目录（向上查找直到找到数据文件所在位置）。"""
    here = Path(__file__).resolve().parent.parent
    if (here / "data" / "raw" / "global_ai_jobs_2026.csv").exists():
        return here
    for p in here.parents:
        if (p / "data" / "raw" / "global_ai_jobs_2026.csv").exists():
            return p
    raise FileNotFoundError("未找到 data/raw/global_ai_jobs_2026.csv")


ROOT = _find_root()
DATA_PATH = ROOT / "data" / "raw" / "global_ai_jobs_2026.csv"

# ---------------------------------------------------------------- 列名映射
# 原始列名包含 % 等特殊字符，统一重命名为简洁的 snake_case，便于管道操作
RENAME_MAP = {
    "Job_ID": "job_id",
    "Job_Title": "job_title",
    "AI_Specialization": "ai_specialization",
    "Industry": "industry",
    "Company": "company",
    "Company_Size": "company_size",
    "Country": "country",
    "Continent": "continent",
    "Education_Required": "education",
    "Experience_Level": "experience_level",
    "Years_of_Experience": "years_experience",
    "Salary_USD": "salary_usd",
    "Salary_Min": "salary_min",
    "Salary_Max": "salary_max",
    "Salary_Category": "salary_category",
    "Bonus_%": "bonus_pct",
    "Equity_Offered": "equity_offered",
    "Benefits_Value_USD": "benefits_usd",
    "Skills_Required": "skills",
    "Required_Certifications": "certifications",
    "Job_Openings": "job_openings",
    "Competition_Level_Applicants": "applicants",
    "Hiring_Difficulty_1_10": "hiring_difficulty",
    "Job_Type": "job_type",
    "Remote_Work_%": "remote_pct",
    "Work_From_Home_Available": "wfh",
    "Job_Satisfaction_1_10": "satisfaction",
    "Work_Life_Balance_1_10": "wlb",
    "AI_Investment_Company_Millions": "ai_investment_m",
    "Company_AI_Maturity_1_10": "ai_maturity",
    "Job_Growth_Projection_%": "growth_pct",
    "Automation_Risk_%": "automation_risk_pct",
    "Gender_Diversity_%_Female": "female_pct",
    "Posted_Date": "posted_date",
    "Application_Deadline": "deadline",
    "Record_Created": "record_created",
    "Data_Source": "source",
}

# 有序类别（用于排序与绘图）
EDU_ORDER = ["Bachelor's", "Master's", "PhD", "Postdoctoral"]
EXP_ORDER = ["Entry Level", "Mid Level", "Senior Level", "Lead Level", "Executive"]
SALARY_CAT_ORDER = ["Low", "Lower-Mid", "Mid", "Upper-Mid", "High", "Very High"]


# ---------------------------------------------------------------- 数据加载
def load_data() -> pd.DataFrame:
    """读取原始数据：重命名列、解析日期、构造派生特征。"""
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    df = df.rename(columns=RENAME_MAP)

    # 日期解析
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    df["deadline"] = pd.to_datetime(df["deadline"], errors="coerce")

    # 派生特征
    df["skill_count"] = df["skills"].str.split(",").str.len()          # 技能数量
    df["salary_range"] = df["salary_max"] - df["salary_min"]           # 薪资区间宽度
    df["is_remote_friendly"] = (df["wfh"] == "Yes").astype(int)        # 是否支持居家
    return df


# ---------------------------------------------------------------- 绘图样式
def setup_style() -> None:
    """统一 seaborn/matplotlib 样式，支持中文显示。"""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "font.sans-serif": ["Microsoft YaHei", "SimHei", "Noto Sans SC", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "figure.dpi": 110,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "legend.frameon": False,
        }
    )


# ---------------------------------------------------------------- 工具函数
def fmt_usd(x, pos=None):
    """金额格式化：$128K / $1.2M（可直接用作 matplotlib Formatter）。"""
    if x >= 1_000_000:
        return f"${x / 1e6:.1f}M"
    if x >= 1_000:
        return f"${x / 1e3:.0f}K"
    return f"${x:.0f}"


def insights(*lines: str) -> None:
    """打印结论要点。"""
    for line in lines:
        print("·", line)
