# AI 智能伴侣

用 Streamlit + DeepSeek 写的网页聊天应用，AI 扮演一个性格可自定义的伴侣，聊天记录了保存在本地。

## 功能

- 流式逐字回复，带上下文，能接住上文
- 侧边栏修改伴侣的**昵称**和**性格**，实时生效
- 多会话管理：新建、切换、删除，当前会话高亮
- 每轮对话自动存成 `session/<时间戳>.json`，关掉页面还能翻回来

## 环境准备

```powershell
pip install streamlit openai
$env:DEEPSEEK_API_KEY = "你的 DeepSeek 密钥"
```

在脚本同级目录建一个 `resources` 文件夹，里面放一张 `小黑子.jpg` 作为应用 logo（不需要 logo 就把 `st.logo(...)` 那行删掉）。

## 运行

```powershell
cd 存放 ai_partner.py 的目录
streamlit run ai_partner.py
```

浏览器打开 http://localhost:8501

> 必须在 `ai_partner.py` 所在目录启动：logo 和 `session/` 用的都是相对路径，从别的目录启动 `st.logo()` 会报错导致页面白屏。

## 会话文件格式

```json
{
    "current_session": "2026-10-28-23-49-19",
    "messages": [
        { "role": "user", "content": "那你好" },
        { "role": "assistant", "content": "哟，就一句“你好”打发本总统啊？" }
    ],
    "nick_name": "特朗普",
    "nature": "傲娇任性的黄毛美国总统"
}
```

## 说明

- 模型：`deepseek-flash`，通过 OpenAI 兼容 SDK 调用，开启了深度思考模式
- 系统提示词约束了说话方式：先共情再建议、口语化短句、单次回复不超过 3 句
