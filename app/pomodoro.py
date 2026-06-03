import gradio as gr
from app.ui.api_client import complete_pomodoro

def create_pomodoro_ui():
    with gr.Column(elem_classes="glass-card"):
        gr.Markdown("## ⏳ Focus Timer")
        
        # 타이머 표시용 HTML
        timer_display = gr.HTML(
            "<div style='font-size: 48px; text-align: center; margin: 20px 0; font-family: monospace;'>25:00</div>"
        )
        
        with gr.Row():
            start_btn = gr.Button("Start Focus", variant="primary")
            stop_btn = gr.Button("Reset")
        
        # 상태 관리 변수
        timer_state = gr.State(value=1500) # 25분 (초 단위)
        is_running = gr.State(value=False)
        
        def format_time(seconds):
            mins = seconds // 60
            secs = seconds % 60
            return f"<div style='font-size: 48px; text-align: center; margin: 20px 0; font-family: monospace;'>{mins:02d}:{secs:02d}</div>"

        def tick(seconds, running):
            if not running or seconds <= 0:
                return seconds, format_time(seconds), running, gr.update(active=running and seconds > 0)
            
            new_seconds = seconds - 1
            if new_seconds == 0:
                complete_pomodoro(duration=25)
                return 1500, format_time(1500), False, gr.update(active=False)
                
            return new_seconds, format_time(new_seconds), True, gr.update(active=True)

        # 1초마다 실행되는 타이머 컴포넌트
        timer = gr.Timer(1, active=False)
        timer.tick(tick, [timer_state, is_running], [timer_state, timer_display, is_running, timer])
        
        start_btn.click(lambda: (True, True), None, [is_running, timer.active])
        stop_btn.click(lambda: (1500, format_time(1500), False, False), None, [timer_state, timer_display, is_running, timer.active])

    return timer_display