# Global AI Jobs 2026 数据分析项目

对 Kaggle 数据集 [Global AI Jobs Report 2026](https://www.kaggle.com/datasets/datascikhan/global-ai-jobs-2026)（5000 条全球 AI 岗位记录 × 37 字段）完成的完整分析：探索性数据分析 → 专题可视化 → 机器学习建模。

## 项目结构

```
├── main.ipynb                     # 数据下载与初步查看
├── data/raw/global_ai_jobs_2026.csv
├── notebooks/
│   ├── 01_eda.ipynb               # 探索性数据分析（8 项）
│   ├── 02_visualization.ipynb     # 专题可视化（9 项）
│   └── 03_machine_learning.ipynb  # 机器学习项目（8 项）
└── scripts/common.py              # 公共模块：数据加载/列名规范化/绘图样式
```

## 运行方式

```bash
pip install -r requirements.txt
jupyter lab   # 依次打开 notebooks/ 下三个 notebook 运行
```

所有聚合均使用 pandas 管道式操作（`groupby / agg / query / assign / sort_values`）完成；绘图使用 seaborn/matplotlib（已配置中文字体）。

## 分析内容

- **EDA**：岗位构成、薪资分布、经验分布、地理趋势、行业模式、远程办公、自动化风险、满意度
- **可视化**：薪资分布、高薪岗位 Top12、行业需求、地理分布、远程对比、经验-薪资、岗位风险、行业 AI 成熟度、职级增长曲线
- **机器学习**：薪资预测（R²≈0.68）、技能文本→岗位分类（Top-3 准确率 100%）、职业人群细分（KMeans）、岗位聚类（Ward 层次聚类）、自动化风险/满意度预测、置换重要性、IsolationForest 异常检测

## 核心发现

- 岗位覆盖 36 类 × 8 大专业方向，数量高度均衡；欧洲（45%）+ 亚洲（29%）为主要聚集地
- 年薪中位数约 $142K，右偏长尾（最高 $718K）；Entry→Executive 中位数从 $73K 升至 $340K
- 64% 岗位支持 WFH、平均远程比例 58%，行业间远程友好度差异平缓
- 技能组合对岗位有极强辨识度，可用于简历匹配与岗位推荐
- 自动化风险、满意度在本数据集中接近随机生成，特征无显著预测力（负结果）

## 数据质量提示

该数据集为模拟/合成数据：`Posted_Date` 含 2026~2039 未来日期、经验等级与实际年限一致性弱、多数数值特征间相关性≈0。分析结论侧重方法论演示，不宜直接用于真实市场决策。
