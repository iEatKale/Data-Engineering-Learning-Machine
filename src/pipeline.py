import json
from pathlib import Path
from dotenv import load_dotenv
import time

from .paths import (
    DIRTY_TRAIN_CSV, CLEAN_TRAIN_CSV,
    INPUTS_DIR, DATA_DIR, PROMPTS_FILE
)
from .prompts import load_prompts
from .io_csv import read_csv, df_to_csv_text

from .providers.openai_provider import OpenAIProvider
from .providers.mistral_provider import MistralProvider
from .providers.claude_provider import ClaudeProvider


def resolve_input_path(input_override: str | None = None) -> Path:
    if not input_override:
        raise ValueError(
            "No input file provided."
        )

    candidate = Path(input_override)

    if candidate.exists():
        return candidate

    candidate_in_inputs = INPUTS_DIR / input_override
    if candidate_in_inputs.exists():
        return candidate_in_inputs

    raise FileNotFoundError(
        f"Could not find input file: {input_override}\n"
        f"Tried:\n"
        f" - {candidate}\n"
        f" - {candidate_in_inputs}"
    )


def run_pipeline_multi(
    provider_name: str | None = None,
    input_override: str | None = None,
    use_references: bool = True
):
    load_dotenv()

    induce_tmpl, apply_tmpl, infer_noref_tmpl = load_prompts(PROMPTS_FILE)

    if use_references:
        dirty_train_df = read_csv(DIRTY_TRAIN_CSV)
        clean_train_df = read_csv(CLEAN_TRAIN_CSV)

    input_path = resolve_input_path(input_override)
    input_df = read_csv(input_path)

    if use_references:
        induce_prompt = induce_tmpl.format(
            DIRTY_CSV=df_to_csv_text(dirty_train_df),
            CLEAN_CSV=df_to_csv_text(clean_train_df),
        )

    all_providers = {
        "openai": OpenAIProvider(),
        "claude": ClaudeProvider(),
        "mistral": MistralProvider(),
    }

    if provider_name:
        if provider_name not in all_providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        providers = [all_providers[provider_name]]
    else:
        providers = list(all_providers.values())

    outputs_root = DATA_DIR / "outputs"
    outputs_root.mkdir(parents=True, exist_ok=True)

    input_stem = input_path.stem
    mode = "ref" if use_references else "noref"

    for p in providers:
        out_dir = outputs_root / p.name / mode / input_stem
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=== Running provider: {p.name} on {input_path.name} ===")

        start_time = time.time()

        if use_references:
            rules = p.generate_json(induce_prompt)
            (out_dir / "rules.json").write_text(
                json.dumps(rules, indent=2), encoding="utf-8"
            )

            apply_prompt = apply_tmpl.format(
                RULES_JSON=json.dumps(rules, indent=2),
                DIRTY_CSV=df_to_csv_text(input_df),
            )
            cleaned_csv = p.generate_text(apply_prompt).strip()

        else:
            noref_rules_prompt = infer_noref_tmpl.format(
                DIRTY_CSV=df_to_csv_text(input_df)
            )

            rules = p.generate_json(noref_rules_prompt)
            (out_dir / "rules.json").write_text(
                json.dumps(rules, indent=2), encoding="utf-8"
            )

            apply_prompt = apply_tmpl.format(
                RULES_JSON=json.dumps(rules, indent=2),
                DIRTY_CSV=df_to_csv_text(input_df),
            )
            cleaned_csv = p.generate_text(apply_prompt).strip()

        end_time = time.time()
        duration = end_time - start_time

        (out_dir / "cleaned.csv").write_text(cleaned_csv + "\n", encoding="utf-8")
        print(f"[OK] {p.name}: wrote rules.json + cleaned.csv")
        print(f"[TIME] {p.name}: {duration:.2f} seconds")