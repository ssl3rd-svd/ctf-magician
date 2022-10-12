from .project_impl import CMagProjectImpl

class CMagProject(CMagProjectImpl):
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        loaded, total = self.plugin_manager.load_all(True)
        if total:
            self.log.info(f"{loaded} of {total} plugins loaded.")
        else:
            self.log.warn(f"no plugins loaded.")

    def __repr__(self) -> str:
        return f"<CMagProject path={self.dir}>"