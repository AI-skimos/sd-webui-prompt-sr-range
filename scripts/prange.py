from modules import scripts, script_callbacks

def make_axis_options():
    xyz_grid = [x for x in scripts.scripts_data if x.script_class.__module__ == "xyz_grid.py"][0].module
    def apply_mimic_scale(p, x, xs):
        if x != 0:
            setattr(p, "dynthres_enabled", True)
            setattr(p, "dynthres_mimic_scale", x)
        else:
            setattr(p, "dynthres_enabled", False)
    def confirm_scheduler(p, xs):
        for x in xs:
            if x not in VALID_MODES:
                raise RuntimeError(f"Unknown Scheduler: {x}")
    
    def float_to_str(value):
        return str(int(value)) if value.is_integer() else '{:.{prec}f}'.format(value, prec=len(str(value).split('.')[1]))

    def apply_prompt_range(p, x, xs):
        print(f"DEBUG: xs: {xs}, x:{x}")
        old, new = float_to_str(xs[0]), float_to_str(x)
        if old not in p.prompt and old not in p.negative_prompt:
            raise RuntimeError(f"Prompt S/R did not find {xs[0]} in prompt or negative prompt.")
        p.prompt = p.prompt.replace(old, new)
        p.negative_prompt = p.negative_prompt.replace(old, new)
        print(f"DEBUG: propmt: {p.prompt}")

    extra_axis_options = [
        xyz_grid.AxisOption("Prompt S/R Range", float, apply_prompt_range)
    ]
    if not any("Prompt S/R Range" in x.label for x in xyz_grid.axis_options):
        xyz_grid.axis_options.extend(extra_axis_options)

def callbackBeforeUi():
    try:
        make_axis_options()
    except Exception as e:
        traceback.print_exc()
        print(f"Failed to add support for X/Y/Z Plot Script because: {e}")

script_callbacks.on_before_ui(callbackBeforeUi)