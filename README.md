# API Gateway Real

聚合 Pump.fun、Dexscreener、Axiom.trade、GAGN 四个平台数据，
提供统一接口：GET /api/feeds

## 部署

1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

2. 运行
   ```bash
   python main.py
   ```

## 扩展

- 在 `feeds.py` 中完善 fetch_axiom()、fetch_gagn() 的真实抓取逻辑
- 调整合并与去重策略
