# 실행 방법: uvicorn fastapi_calc:app --reload
from fastapi1 import FastAPI
import gradio as gr
import requests

app = FastAPI()

# 1. FastAPI API: 수식을 계산하는 엔드포인트
@app.get("/api/calc")
def calculate(formula: str):
    try:
        result = eval(formula) # eval 함수를 통한 연산 
        return {"result": str(result)}
    except Exception as e:
        return {"result": f"오류: {str(e)}"}


# 2. Gradio에서 API를 호출하는 함수
def call_calc_api(formula):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/api/calc",
            params={"formula": formula}
        )
        return res.json()["result"]
    except Exception as e:
        return f"연결 오류: {str(e)}"


# 3. Gradio UI 구성
with gr.Blocks() as demo:
    gr.Markdown("## FastAPI 계산기")
    
    # 옆으로 배치
    with gr.Row():
        input_formula = gr.Textbox(
            label="수식 입력", 
            placeholder="예: (10 + 20) * 3 / 2",
            scale=4
        )
        calc_btn = gr.Button("계산", variant="primary", scale=1)
    
    output_result = gr.Textbox(label="계산 결과", interactive=False)
    
    gr.Markdown("""
    ### 사용 가능한 연산자
    - 더하기(+), 빼기(-), 곱하기(*), 나누기(/)
    - 괄호 ( ), 거듭제곱 (**)
    """)

    # 버튼 클릭 시 API 호출
    calc_btn.click(
        fn=call_calc_api,
        inputs=input_formula,
        outputs=output_result
    )


# 4. FastAPI에 Gradio 앱 마운트
app = gr.mount_gradio_app(app, demo, path="/")