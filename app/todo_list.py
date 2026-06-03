import gradio as gr
from app.ui.api_client import get_all_todos, add_todo

def format_todo_html():
    todos = get_all_todos()
    html = "<div style='display: flex; flex-direction: column; gap: 10px;'>"
    for t in todos:
        status = "✅" if t['is_completed'] else "⏳"
        html += f"""
        <div class="glass-card">
            <h3 style='margin:0;'>{status} {t['title']} <span style='font-size: 0.8em; color: gray;'>[{t['priority']}]</span></h3>
            <p style='margin: 5px 0;'>{t['content'] or ''}</p>
            <small>{t['category']} | {t['created_at'][:10]}</small>
        </div>
        """
    html += "</div>"
    return html

def create_todo_ui():
    with gr.Column():
        gr.Markdown("## 📝 New Task")
        with gr.Row():
            title = gr.Textbox(label="Title", placeholder="What needs to be done?")
            priority = gr.Dropdown(choices=["High", "Medium", "Low"], value="Medium", label="Priority")
        
        content = gr.Textbox(label="Content", lines=2)
        category = gr.Textbox(label="Category", value="General")
        
        add_btn = gr.Button("Add Task", variant="primary")
        
        gr.Markdown("---")
        gr.Markdown("## 📋 My Todo List")
        todo_display = gr.HTML(value=format_todo_html)
        
        def handle_add(t, c, p, cat):
            add_todo(t, c, p, cat)
            return format_todo_html()

        add_btn.click(handle_add, [title, content, priority, category], [todo_display])