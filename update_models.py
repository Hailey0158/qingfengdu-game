import json, os, sys

# 用户提供的新配置（Buddy 自定义模型集合）
new_config = {
    "models": [
        {"id": "Auto", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "GLM-5.2", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "GLM-5V", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "MiniMax-M3", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "Kimi-K2.7", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "Kimi-K3", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "DeepSeek-V4-Pro", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
        {"id": "DeepSeek-V4-Flash", "name": "AG", "vendor": "apiget",
         "apiKey": "sk-OypvSNfyDKrmsewb6hMn9yCOgEbPVISKBcR4shIDbWORNaYB",
         "url": "https://api.apiget.store/v1/chat/completions",
         "maxInputTokens": 360000, "maxOutputTokens": 8192,
         "supportsToolCall": True, "supportsImages": True, "supportsReasoning": True},
    ]
}

targets = [
    os.path.expanduser(r"~\workbuddy\models.json"),
    os.path.expanduser(r"~\codebuddy\models.json"),
]

def load_existing(path):
    if not os.path.exists(path):
        return {"models": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 解析现有文件失败 {path}: {e}")
        sys.exit(1)

for path in targets:
    existing = load_existing(path)
    if not isinstance(existing, dict) or "models" not in existing or not isinstance(existing["models"], list):
        print(f"[ERROR] 现有文件结构无效: {path}")
        sys.exit(1)

    # 按 id 建立索引：保留非 Buddy(本批) 自定义模型，本批按 id 覆盖，缺失 id 才追加
    new_by_id = {m["id"]: m for m in new_config["models"]}
    merged = []
    seen = set()
    for m in existing["models"]:
        mid = m.get("id")
        if mid in new_by_id:
            merged.append(new_by_id[mid])  # 覆盖
            seen.add(mid)
        else:
            merged.append(m)  # 保留其他模型
    # 追加本批中现有文件没有的 id
    for mid, m in new_by_id.items():
        if mid not in seen:
            merged.append(m)

    # 校验：每个 id 只保留一条
    ids = [m.get("id") for m in merged]
    if len(ids) != len(set(ids)):
        print(f"[ERROR] 合并后出现重复 id: {path}")
        sys.exit(1)
    # 校验：不得把 id 改成 AG:*
    for m in merged:
        if str(m.get("id", "")).startswith("AG:"):
            print(f"[ERROR] 发现非法 id 前缀 AG: -> {m.get('id')}")
            sys.exit(1)

    result = {"models": merged}
    # 再次解析验证
    try:
        json.dumps(result, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] 结果序列化失败: {e}")
        sys.exit(1)

    # 写临时文件，再原子替换
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    # 验证临时文件可解析
    with open(tmp, "r", encoding="utf-8") as f:
        json.load(f)
    os.replace(tmp, path)
    print(f"[OK] 已更新: {path} (模型数={len(merged)})")

print("全部完成")
