# general functions for getting block opcodes
# internal use only

from urllib.request import urlopen, Request
import re
import json
import warnings
import sys

try:
    from py_mini_racer import MiniRacer
except ModuleNotFoundError:
    print("mini-racer not found", file=sys.stderr)

__all__ = ["get_opcodes_from_js"]

def _get_rguc_data(url:str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"}) # to be safe
    with urlopen(req) as response:
        return response.read().decode("utf-8")
    
def get_opcodes_from_js(file:str) -> dict | list:
    """Get block opcodes from a JS extension file's getInfo's return value. 
    Use with a custom extension, like one developed for SBX or TurboWarp.

    WARNING: This function executes arbitrary external JS. Ensure file comes
    from a trusted source.
    """

    # Future issues: need more dummies
    with MiniRacer() as ctx:
        ctx.eval("""
                const Scratch = {
                    BlockType: {
                        REPORTER: "REPORTER",
                        COMMAND: "COMMAND",
                        BOOLEAN: "BOOLEAN",
                        EVENT: "BOOLEAN",
                        HAT: "HAT"
                    },
                    extensions: {
                        register(ext){
                            // dummy
                            globalThis.__ext = ext
                        },
                        unsandboxed: true
                    },
                    vm: {
                        runtime: {
                            on(a, b){}
                        }
                    }
                }
                document = {
                  addEventListener(a, b){} // For hat blocks
                }
            """
        )

        with open(file) as f:
            ctx.eval(f.read())

        return json.loads(ctx.eval("JSON.stringify(__ext.getInfo())"))['blocks']


if __name__ == "__main__":
    print(get_opcodes_from_js(sys.argv[1]))
