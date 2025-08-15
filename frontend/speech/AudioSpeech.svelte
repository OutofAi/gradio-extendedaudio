<!-- SimpleGenerateBox.svelte -->
<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let text_value = "";
  export let placeholder = "Type your text here…";
  export let buttonLabel = "Text to Speech";
  export let rows = 8;
  export let disabled = false;

  export let options: string[] = ["Option1", "Option2"];
  type Choice = string | null;

  export let defaultChoice: Choice = options[0] ?? null;
  let selected: Choice = defaultChoice;

  const dispatch = createEventDispatcher<{
    generate: { text: string; choice: Exclude<Choice, null> };
  }>();

  function submit() {
    const text = text_value.trim();
    if (!text || !selected) return;
    dispatch("generate", { text, choice: selected });
  }

  // if options change at runtime, keep selection valid
  $: if (selected && !options.includes(selected)) {
    selected = options[0] ?? null;
  }

  function onKeydown(e: KeyboardEvent) {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      submit();
    }
  }

  function onRadioKeydown(e: KeyboardEvent) {
    if (!["ArrowRight", "ArrowLeft"].includes(e.key)) return;
    e.preventDefault();
    const idx = options.indexOf(selected ?? options[0]);
    const next = e.key === "ArrowRight"
      ? (idx + 1) % options.length
      : (idx - 1 + options.length) % options.length;
    selected = options[next];
  }
</script>

<div class="wrapper">
  <div class="box" aria-labelledby="sgb-title">
    <label class="sr-only" for="gen-input">Text input</label>
    <textarea
      id="gen-input"
      class="input"
      {rows}
      bind:value={text_value}
      placeholder={placeholder}
      on:keydown={onKeydown}
    />

    <div class="controls">
      {#if options.length > 1}
        <div class="radios" role="radiogroup" aria-label="Choose one" tabindex="0" on:keydown={onRadioKeydown}>
          {#each options as opt, i}
            <button
              type="button"
              class="radio {selected === opt ? 'selected' : ''}"
              role="radio"
              aria-checked={selected === opt}
              tabindex={selected === opt ? 0 : -1}
              on:click={() => (selected = opt)}
            >
              {opt}
            </button>
          {/each}
        </div>
      {/if}

      <button
        class="generate"
        type="button"
        on:click={submit}
        disabled={disabled || !text_value.trim() || !selected}
        aria-disabled={disabled || !text_value.trim() || !selected}
      >
        {buttonLabel}
      </button>
    </div>
  </div>
</div>

<style>
/* ---- Theme bridge: reuse the same tokens your other component uses ---- */
/* If your app already defines --neutral-*, --spacing-*, --color-accent, etc.
   these will be used. Otherwise the fallbacks on the right kick in. */

:global(:root) {
  --bg: var(--panel-background, #ffffff);
  --fg: var(--neutral-900, #111827);
  --muted: var(--neutral-500, #6b7280);
  --border: var(--neutral-200, #e5e7eb);
  --seg-bg: var(--neutral-100, #f3f4f6);

  --accent: var(--color-accent, #3b82f6);
  --accent-foreground: var(--button-primary-text, #ffffff);
  --focus: var(--focus-color, var(--color-accent, #3b82f6));
  --ring-alpha: var(--focus-ring-alpha, 0.18);

  --radius-lg: var(--radius-lg, 12px);
  --radius-pill: 999px;

  --space-1: var(--size-1, 4px);
  --space-2: var(--size-2, 8px);
  --space-3: var(--size-3, 12px);
  --space-4: var(--size-4, 16px);
}

@media (prefers-color-scheme: dark) {
  :global(:root) {
    --bg: var(--panel-background, #0b1220);
    --fg: var(--neutral-200, #e5e7eb);
    --muted: var(--neutral-400, #9ca3af);
    --border: var(--neutral-700, #25304a);
    --seg-bg: var(--neutral-900, #111827);

    --accent: var(--color-accent, #3b82f6);
    --accent-foreground: var(--button-primary-text, #0b1220);
    --focus: var(--focus-color, #60a5fa);
    --ring-alpha: var(--focus-ring-alpha, 0.28);
  }
}

/* Also support explicit dark theme containers if your app uses them */
:global(.dark), :global([data-theme="dark"]) {
  --bg: var(--panel-background, #0b1220);
  --fg: var(--neutral-200, #e5e7eb);
  --muted: var(--neutral-400, #9ca3af);
  --border: var(--neutral-700, #25304a);
  --seg-bg: var(--neutral-900, #111827);

  --accent: var(--color-accent, #3b82f6);
  --accent-foreground: var(--button-primary-text, #0b1220);
  --focus: var(--focus-color, #60a5fa);
  --ring-alpha: var(--focus-ring-alpha, 0.28);
}

/* ---- Your component styles (now using the bridged tokens) ---- */

.wrapper { width: 100%; }

.box {
  position: relative;
  width: 100%;
  color-scheme: light dark;
  padding-top: 0.1rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  color: var(--fg);
}

/* Textarea matches neutral panel look */
.input {
  box-sizing: border-box;
  width: 100%;
  height: 150px;
  padding: var(--space-3) var(--space-3) calc(64px + var(--space-3)) var(--space-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  font: inherit;
  outline: none;
  background: var(--seg-bg);
  color: var(--fg);
}
.input::placeholder { color: var(--muted); }
.input:focus {
  border-color: var(--focus);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, var(--ring-alpha));
}

/* Controls bar */
.controls {
  position: absolute;
  right: var(--space-3);
  bottom: var(--space-3);
  padding-right: 0.5rem;
  padding-bottom: 0.1rem;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Segmented radio matches the second component’s subtle group */
.radios {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 3px;
  background: var(--seg-bg);
}

/* Radio “pills” */
.radio {
  border: 1px solid transparent;
  background: transparent;
  padding: 3px 12px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  font-weight: 600;
  color: var(--fg);
  transition: background 120ms ease, border-color 120ms ease, color 120ms ease, box-shadow 120ms ease;
}
.radio:hover {
  color: var(--accent);
}
.radio.selected {
  background: var(--accent);
  color: var(--accent-foreground);
  border-color: var(--accent);
}
.radio:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, var(--ring-alpha));
}

/* Primary action button, aligned with the “accent” look */
.generate {
  height: 32px;
  padding: 0 14px;
  border: 1px solid var(--accent);
  border-radius: var(--radius-pill);
  font-weight: 600;
  cursor: pointer;
  background: var(--accent);
  color: var(--accent-foreground);
  transition: filter 120ms ease, box-shadow 120ms ease, opacity 120ms ease;
}
.generate:hover { filter: brightness(0.97); }
.generate:active { filter: brightness(0.94); }
.generate:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, var(--ring-alpha));
}
.generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Accessibility helper */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

</style>
