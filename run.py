import sys
from src.pipeline import run_pipeline_multi

if __name__ == "__main__":
    provider = None
    input_file = None
    use_references = True

    if len(sys.argv) > 1:
        provider = sys.argv[1].lower()
        if provider == "all":
            provider = None

    if len(sys.argv) > 2:
        input_file = sys.argv[2]

    if len(sys.argv) > 3:
        mode = sys.argv[3].lower()
        if mode == "noref":
            use_references = False
        elif mode == "ref":
            use_references = True
        else:
            raise ValueError("Third argument must be 'ref' or 'noref'")

    run_pipeline_multi(
        provider_name=provider,
        input_override=input_file,
        use_references=use_references
    )