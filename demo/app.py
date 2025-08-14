
import gradio as gr
from gradio_extendedaudio import ExtendedAudio


def internal_fn(evt: gr.EventData):
    # You Text-to-Speech inference code should be done here
    detail = getattr(evt, "data", None) or getattr(evt, "_data", {}) or {}
    text   = detail.get("text")
    voice  = detail.get("choice")
    return f"voice={voice!r}, text={text!r}"

with gr.Blocks() as demo:
    src = ExtendedAudio()
    out = gr.Text()
    src.generate(fn=internal_fn, outputs=[out])

if __name__ == "__main__":
    demo.launch()
