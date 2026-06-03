import gradio as gr
from app.api_client import chat_message


def _respond(message: str, history: list[dict]) -> str:
    return chat_message(message, history)


with gr.Blocks(title="AI Todo 채팅") as chat_demo:
    gr.HTML(
        '<div style="padding:10px 0 4px;">'
        '<a href="/" style="padding:5px 12px;background:#f3f4f6;color:#374151;'
        'border-radius:6px;text-decoration:none;font-size:13px;">← Todo 목록</a></div>'
    )
    gr.ChatInterface(
        fn=_respond,
        description="저장된 Todo 목록을 바탕으로 AI와 자유롭게 대화하세요.",
        examples=[
            "오늘 마감인 할 일이 있어?",
            "아직 완료하지 못한 일들을 요약해줘",
            "가장 최근에 추가한 할 일이 뭐야?",
        ],
    )
