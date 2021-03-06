import ConfigParser
import os
from cbinder.generator import CBindings
from build_openni import predefs, prelude, INCLUDES as ONI_INCLUDES

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'sources.ini'))


class Nite2Builder(CBindings):
    @classmethod
    def build(cls):
        builder = cls([os.path.join(config.get("headers", "nite_include_dir"), "NiteCAPI.h")],
            includes = ["NiteCEnums.h", "NiteCTypes.h", "NiteVersion.h"] + ONI_INCLUDES,
            include_dirs = [config.get("headers", "openni_include_dir")], 
            predefs = predefs, 
            prelude = prelude)
        builder.export("../primesense/_nite2.py")

    def filter_type(self, tp):
        return tp.name not in ["bool", "int8_t", "int16_t", "int32_t", "int64_t", "uint8_t", 
            "uint16_t", "uint32_t", "uint64_t"]
    
    def filter_func(self, func):
        return not func.name.startswith("oni")

    def emit_prelude(self, m):
        #copy("../cbinder/lib.py", "../primesense/cbinder_lib.py")
        m.from_("primesense.utils", "CEnum", "UnloadedDLL")
    
    def emit_struct_decl(self, m, tp):
        if tp.name.lower().startswith("oni"):
            m.from_("_openni2", tp.name)
        else:
            CBindings.emit_struct_decl(self, m, tp)
    
    def emit_struct_fields(self, m, tp):
        if not tp.name.lower().startswith("oni"):
            CBindings.emit_struct_fields(self, m, tp)

    def emit_union_decl(self, m, tp):
        if tp.name.lower().startswith("oni"):
            m.from_("_openni2", tp.name)
        else:
            CBindings.emit_union_decl(self, m, tp)
    
    def emit_union_fields(self, m, tp):
        if not tp.name.startswith("Oni"):
            CBindings.emit_union_fields(self, m, tp)

    def emit_enum(self, m, tp):
        if tp.name.lower().startswith("oni"):
            m.from_("_openni2", tp.name)
        else:
            CBindings.emit_enum(self, m, tp)
    
    def before_funcs_hook(self, m):
        m.import_("functools")
        m.from_("primesense.utils", "NiteError")
        m.sep()
        with m.def_("nite_call", "func"):
            m.stmt("@functools.wraps(func)")
            with m.def_("wrapper", "*args"):
                m.stmt("res = func(*args)")
                with m.if_("res != NiteStatus.NITE_STATUS_OK"):
                    m.raise_("NiteError(res)")
                m.return_("res")
            m.return_("wrapper")
    
    def emit_func(self, m, func):
        if func.type.name == "NiteStatus":
            m.stmt("@nite_call")
        CBindings.emit_func(self, m, func)


if __name__ == "__main__":
    Nite2Builder.build()


