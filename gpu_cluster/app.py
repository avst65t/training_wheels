import gradio as gr
import httpx  # instead of requests

API_URL = "http://10.8.10.91:5000/ask"

async def ask_stream(user_input):
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", API_URL, json={"text": user_input}) as response:
                partial = ""
                async for chunk in response.aiter_text():
                    partial += chunk
                    yield partial
    except Exception as e:
        yield f"[Error] {e}"

with gr.Blocks(title=" 🧠 Assistant") as demo:
    gr.Markdown("##🧠 Distributed LLM Inference - Streaming Q&A")

    output_display = gr.Markdown(value="Ask something below...", elem_id="output")

    with gr.Row(elem_id="input-row"):
        question_input = gr.Textbox(
            placeholder="Type your question...",
            lines=1,
            scale=10,
            elem_id="question-box",
            show_label=False
        )
        submit_btn = gr.Button("Submit", scale=1, elem_id="submit-btn")

    submit_btn.click(fn=ask_stream, inputs=question_input, outputs=output_display)
    question_input.submit(fn=ask_stream, inputs=question_input, outputs=output_display)

    demo.css = """
    body{
        color:#000;
    }

    #output {
        height: 500px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 1em;
        border-radius: 10px;
        background-color: #27272a;
        font-size: 1.1em;
        white-space: pre-wrap;
        color: #f4f4f5;
    }

    #input-row {
        position: sticky;
        bottom: 0;
        background: rgb(82, 82, 91);
        padding-top: 10px;
        padding-bottom: 10px;
    }

    #question-box textarea {
        font-size: 1em;
        padding: 10px;
        border-radius: 8px;
    }

    #submit-btn {
        height: 48px;
        margin-left: 10px;
        padding: 0 16px;
        font-size: 1em;
        background: #27272a !important;
        color: white;
    }
    """

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
