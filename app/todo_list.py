import gradio as gr
import json
from datetime import date
from html import escape
from app.api_client import get_all_todos, add_todo, toggle_todo, delete_todo, update_todo_title, ask_question

# Runs once on page load — defines global JS helpers used by inline HTML handlers
PAGE_JS = """
() => {
    window._todoDispatch = function(data) {
        const el = document.querySelector('#_todo_action textarea');
        if (!el) return;
        el.value = JSON.stringify(data);
        el.dispatchEvent(new Event('input', {bubbles: true}));
        setTimeout(() => {
            const btn = document.querySelector('#_todo_action_btn button');
            if (btn) btn.click();
        }, 60);
    };
    window.todoToggle = function(el) {
        window._todoDispatch({action: 'toggle', id: parseInt(el.dataset.id)});
    };
    window.todoDelete = function(el) {
        window._todoDispatch({action: 'delete', id: parseInt(el.dataset.id)});
    };
    window.todoEdit = function(el) {
        window._todoDispatch({action: 'edit', id: parseInt(el.dataset.id), title: el.dataset.title});
    };
}
"""

def _dday_label(due: str | None) -> str:
    """due_date 문자열(YYYY-MM-DD)을 받아 D-day 뱃지 HTML 반환."""
    if not due:
        return ""
    try:
        delta = (date.fromisoformat(due) - date.today()).days
        if delta > 0:
            text, color = f"D-{delta}", "#6366f1"
        elif delta == 0:
            text, color = "D-Day", "#f59e0b"
        else:
            text, color = f"D+{abs(delta)}", "#ef4444"
        return (
            f"<span style='font-size:11px;padding:2px 7px;border-radius:10px;"
            f"background:{color};color:#fff;margin-left:4px;'>{text}</span>"
        )
    except ValueError:
        return ""


def format_todo_html():
    todos = get_all_todos()
    if not todos:
        return "<p style='color:#9ca3af;padding:20px;text-align:center;'>할 일이 없습니다.</p>"

    items = ""
    for t in todos:
        checked = "checked" if t["is_completed"] else ""
        text_style = "color:#9ca3af;text-decoration:line-through;" if t["is_completed"] else "color:#1f2937;"
        title_safe = escape(t['title'])
        title_attr = escape(t['title'], quote=True)
        due = t.get("due_date") or ""
        due_display = (
            f"<span style='color:#9ca3af;font-size:11px;white-space:nowrap;'>{due}</span>"
            + _dday_label(due)
            if due else ""
        )

        items += f"""
<div style='display:flex;align-items:center;padding:12px 16px;gap:12px;border-bottom:1px solid #f3f4f6;'>
  <input type='checkbox' {checked} data-id='{t["id"]}'
         onchange='window.todoToggle(this)'
         style='width:17px;height:17px;cursor:pointer;accent-color:#6366f1;flex-shrink:0;'>
  <span style='flex:1;font-size:14px;{text_style}'>{title_safe}</span>
  {due_display}
  <span style='color:#d1d5db;font-size:11px;white-space:nowrap;'>{t['created_at'][:10]}</span>
  <button data-id='{t["id"]}' data-title='{title_attr}' onclick='window.todoEdit(this)'
          style='padding:4px 10px;border:1px solid #e5e7eb;border-radius:5px;background:#fff;color:#6b7280;cursor:pointer;font-size:12px;'>수정</button>
  <button data-id='{t["id"]}' onclick='window.todoDelete(this)'
          style='padding:4px 10px;border:1px solid #fecaca;border-radius:5px;background:#fef2f2;color:#ef4444;cursor:pointer;font-size:12px;'>삭제</button>
</div>"""

    return f"<div style='border:1px solid #f3f4f6;border-radius:8px;overflow:hidden;'>{items}</div>"


def create_todo_ui():
    with gr.Tabs():
        # ── Tab 1: Todo 목록 ──────────────────────────────────────
        with gr.TabItem("📝 Todo"):
            with gr.Row():
                title_input = gr.Textbox(label="할 일", placeholder="할 일을 입력하세요", scale=4)
                due_input = gr.DateTime(
                    label="마감일",
                    include_time=False,
                    type="string",
                    value=None,
                    scale=2,
                )
                add_btn = gr.Button("추가", variant="primary", scale=1)

            with gr.Row(visible=False) as edit_row:
                edit_input = gr.Textbox(label="수정할 내용", scale=4)
                save_btn = gr.Button("저장", variant="primary", scale=1)
                cancel_btn = gr.Button("취소", scale=1)

            edit_id_state = gr.State(None)
            todo_display = gr.HTML(value=format_todo_html)
            msg = gr.Markdown("")

            # Hidden JS → Python bridge
            hidden_action = gr.Textbox(visible=False, elem_id="_todo_action")
            hidden_action_btn = gr.Button(visible=False, elem_id="_todo_action_btn")

            def handle_add(title, due_date):
                if not title or not title.strip():
                    return format_todo_html(), gr.update(value=""), gr.update(value=None), "제목을 입력해주세요."
                # gr.DateTime(type="string") returns "YYYY-MM-DD" or None
                add_todo(title.strip(), due_date)
                return format_todo_html(), gr.update(value=""), gr.update(value=None), ""

            def handle_action(action_str):
                if not action_str:
                    return format_todo_html(), gr.update(), gr.update(), None
                try:
                    data = json.loads(action_str)
                except Exception:
                    return format_todo_html(), gr.update(), gr.update(), None

                action = data.get('action')
                todo_id = int(data.get('id', 0))

                if action == 'toggle':
                    toggle_todo(todo_id)
                    return format_todo_html(), gr.update(visible=False), gr.update(value=""), None
                elif action == 'delete':
                    delete_todo(todo_id)
                    return format_todo_html(), gr.update(visible=False), gr.update(value=""), None
                elif action == 'edit':
                    return gr.update(), gr.update(visible=True), gr.update(value=data.get('title', '')), todo_id

                return format_todo_html(), gr.update(), gr.update(), None

            def handle_save(edit_id, new_title):
                if edit_id is not None and new_title and new_title.strip():
                    update_todo_title(int(edit_id), new_title.strip())
                return format_todo_html(), gr.update(visible=False), gr.update(value=""), None

            def handle_cancel():
                return gr.update(visible=False), gr.update(value=""), None

            add_btn.click(handle_add, [title_input, due_input], [todo_display, title_input, due_input, msg])
            title_input.submit(handle_add, [title_input, due_input], [todo_display, title_input, due_input, msg])

            hidden_action_btn.click(
                handle_action,
                [hidden_action],
                [todo_display, edit_row, edit_input, edit_id_state]
            )
            save_btn.click(
                handle_save,
                [edit_id_state, edit_input],
                [todo_display, edit_row, edit_input, edit_id_state]
            )
            cancel_btn.click(handle_cancel, [], [edit_row, edit_input, edit_id_state])

        # ── Tab 2: AI 질의응답 ────────────────────────────────────
        with gr.TabItem("🤖 AI 질의응답"):
            gr.Markdown("저장된 Todo 목록을 바탕으로 질문하세요.")

            question_input = gr.Textbox(
                label="질문",
                placeholder="예: 오늘 마감인 일이 있어? / 아직 못 끝낸 일 요약해줘",
                lines=2,
            )
            ask_btn = gr.Button("질문하기", variant="primary")
            answer_output = gr.Markdown("")

            def handle_ask(question):
                if not question or not question.strip():
                    return "질문을 입력해주세요."
                return ask_question(question.strip())

            ask_btn.click(handle_ask, [question_input], [answer_output])
            question_input.submit(handle_ask, [question_input], [answer_output])
