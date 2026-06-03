import gradio as gr
from app.api_client import get_all_todos, add_todo, toggle_todo, delete_todo

def format_todo_html():
    todos = get_all_todos()
    if not todos:
        return "<p style='color: gray; padding: 12px;'>할 일이 없습니다.</p>"

    rows = ""
    for t in todos:
        status = "✅" if t["is_completed"] else "⬜"
        title_style = "text-decoration: line-through; color: gray;" if t["is_completed"] else ""
        rows += f"""
        <tr style='border-bottom: 1px solid #e0e0e0;'>
            <td style='padding: 8px 12px; color: gray; font-size: 13px;'>{t['id']}</td>
            <td style='padding: 8px 12px; font-size: 16px;'>{status}</td>
            <td style='padding: 8px 12px; {title_style}'>{t['title']}</td>
            <td style='padding: 8px 12px; color: gray; font-size: 12px;'>{t['created_at'][:10]}</td>
        </tr>"""

    return f"""
    <table style='width: 100%; border-collapse: collapse;'>
        <thead>
            <tr style='background: #f5f5f5; text-align: left;'>
                <th style='padding: 8px 12px; font-size: 13px;'>ID</th>
                <th style='padding: 8px 12px; font-size: 13px;'>상태</th>
                <th style='padding: 8px 12px; font-size: 13px;'>할 일</th>
                <th style='padding: 8px 12px; font-size: 13px;'>생성일</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>"""

def create_todo_ui():
    gr.Markdown("## 📝 Todo List")

    with gr.Row():
        title_input = gr.Textbox(label="할 일", placeholder="할 일을 입력하세요", scale=4)
        add_btn = gr.Button("추가", variant="primary", scale=1)

    todo_display = gr.HTML(value=format_todo_html)

    with gr.Row():
        todo_id_input = gr.Number(label="ID", precision=0, scale=2)
        toggle_btn = gr.Button("완료 토글", scale=2)
        delete_btn = gr.Button("삭제", variant="stop", scale=2)

    msg = gr.Markdown("")

    def handle_add(title):
        if not title or not title.strip():
            return format_todo_html(), gr.update(value=""), "제목을 입력해주세요."
        add_todo(title.strip())
        return format_todo_html(), gr.update(value=""), ""

    def handle_toggle(todo_id):
        if todo_id is None:
            return format_todo_html(), "ID를 입력해주세요."
        toggle_todo(int(todo_id))
        return format_todo_html(), ""

    def handle_delete(todo_id):
        if todo_id is None:
            return format_todo_html(), "ID를 입력해주세요."
        delete_todo(int(todo_id))
        return format_todo_html(), ""

    add_btn.click(handle_add, [title_input], [todo_display, title_input, msg])
    toggle_btn.click(handle_toggle, [todo_id_input], [todo_display, msg])
    delete_btn.click(handle_delete, [todo_id_input], [todo_display, msg])
