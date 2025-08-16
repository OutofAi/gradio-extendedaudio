![addition](https://github.com/user-attachments/assets/c6615c87-336b-4a0c-b0bb-7173378b1405)


An extended tab/option to the standard gradio.Audio to dispatch a generate event, useful for hooking up text-to-speech foundation models

## Wheel Generation:
```python
git clone https://github.com/OutofAi/gradio-extendedaudio
```

```python
cd extendedaudio/frontend
```

```python
npm install
```

```python
cd ..
```

```python
gradio cc install 
```

```python
gradio cc build 
```

## Example Usage

```python

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

```
