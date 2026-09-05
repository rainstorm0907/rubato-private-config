import { register } from "node:module";

const registered = Symbol.for("rubato.private.resume-recovery");
if (!globalThis[registered]) {
  globalThis[registered] = true;
  register(new URL("./resume-recovery-hooks.mjs", import.meta.url));
}
