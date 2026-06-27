from pathlib import Path

def read_prompt_block(full_text: str, name: str, prompts_file: Path) -> str:
    marker = f"==={name}==="
    start = full_text.find(marker)
    if start == -1:
        raise ValueError(f"Prompt block '{name}' not found in {prompts_file}")

    start = full_text.find("\n", start)
    if start == -1:
        raise ValueError(f"Prompt block '{name}' is flawed (no newline).")
    start += 1

    end = full_text.find("===", start)
    if end == -1:
        end = len(full_text)

    return full_text[start:end].strip()

def load_prompts(prompts_file: Path) -> tuple[str, str, str]:
    text = prompts_file.read_text(encoding="utf-8")
    induce = read_prompt_block(text, "INDUCE_RULES", prompts_file)
    apply_ = read_prompt_block(text, "APPLY_RULES", prompts_file)
    infer_noref = read_prompt_block(text, "INFER_RULES_NOREF", prompts_file)
    return induce, apply_, infer_noref