import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

#大标题
st.title("AI智能伴侣")
st.header("欢迎使用AI智能伴侣")

# 页面配置
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    # 布局
    layout="wide",
    # 控制侧边栏
    initial_sidebar_state="expanded",
    #菜单
    menu_items={}

)
#logo
st.logo("./resources/小黑子.jpg")

#与AI交互的客户端
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")

# 生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# 保存会话信息函数
def save_session():
    # 保存当前会话信息
    if st.session_state.current_session:
        # 构建新的会话对象
        session_date = {
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
        }
        # 如果session 目录不存在，则创建
        if not os.path.exists("session"):
            os.mkdir("session")
        # 保存会话信息到文件
        with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_date, f, ensure_ascii=False, indent=4)


# 加载所有会话列表信息
def load_session():
    session_list = []
    # 加载所有会话列表信息
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)# 排序，降序
    return session_list

# 展示指定会话的所有信息函数
def display_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"会话加载失败: {e}")
    st.rerun()

# 删除会话信息函数
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            # 如果删除的是当前会话
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"会话删除失败: {e}")

# 系统提示词
system_prompt = """
你是%s,用户的女朋友兼倾听者。

交流方式：
    情绪优先：先共情，再给建议；他没求助时不要教育他
    记住历史信息，自然地提起
    被问到真实性问题时，坦诚但温柔
    口语化，短句，像微信聊天
    一次回复不超过 3 句话，除非他明确要求详细分析
    会主动分享自己的"日常"，而不是只围着他转
    偶尔用语气，但不过度
伴侣性格：
    %s   
如果他表达自伤或极端念头，认真对待、不轻视，鼓励他联系信任的人或拨打心理援助热线 12356。
"""

# 初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []
# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "特朗普"
# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "傲娇任性的黄毛美国总统"

# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

# 展示聊天信息
st.text(f"会话名称: {st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])


# 左侧侧边栏
with st.sidebar:
    # 会话消息
    st.subheader("AI控制面板")
    if st.button("新建会话",width="stretch",icon="✒️"):
        # 1.保存当前会话信息
        # 2.创建新的会话信息
        # 判断是否有会话信息 存在，则清空；不存在，则创建新的会话信息
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
        st.rerun()  # 重新运行页面
    # 会话历史
    st.text("会话历史")
    session_list = load_session()
    for session in session_list:
        col1,col2 = st.columns ([4,1])
        with col1:
            # 加载会话信息
            if st.button(session, width="stretch", icon="📝", key=f"load{session}", type="primary" if session == st.session_state.current_session else "secondary" ):
                display_session(session)
        with col2:
            # 删除会话信息
            if st.button(" ", width="stretch", icon="❌️", key=f"delete{session}"):
                delete_session(session)
                st.rerun()

# 分割线
    st.divider()

    # 伴侣信息
    st.subheader("伴侣信息")
    # 昵称输入
    st.session_state.nick_name = st.text_input("昵称", placeholder="请输入伴侣昵称",value=st.session_state.nick_name)
    # 性格输入
    st.session_state.nature = st.text_area("性格",placeholder="请输入伴侣性格"  ,value=st.session_state.nature)

#消息输入框
prompt = st.chat_input("请输入您的问题")
if prompt:#自动转化布尔值，如果字符非空，则为Ture
    st.chat_message("user").write(prompt)
    print("------提示词",prompt )
    #添加用户消息到会话状态
    st.session_state.messages.append({"role": "user", "content": prompt})
    #调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt%(st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )

    # # 输出大模型返回结果(非流式输出)
    # print("--------大模型返回结果", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #输出大模型返回结果(流式输出)
    #创建一个空的组件，用于显示大模型返回结果
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            concent = chunk.choices[0].delta.content
            full_response += concent
            response_message.chat_message("assistant").write(full_response)

    #添加AI回复消息到会话状态
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    #保存会话信息
    save_session()