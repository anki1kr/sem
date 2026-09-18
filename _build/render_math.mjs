// Build-time math: renders $$...$$ (display) and $...$ (inline) in an HTML body with KaTeX.
// Skips <pre>, <code>, <svg>, <script>, <style>. throwOnError: an invalid formula FAILS the build.
// Usage: node render_math.mjs in.html out.html   |   node render_math.mjs --css out.css
import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(here, "katex", "package.json"));
const katex = require("katex");
const dist = path.join(here, "katex", "node_modules", "katex", "dist");

if (process.argv[2] === "--css") {
  // katex.min.css with every @font-face reduced to one inlined woff2 (offline, single file)
  let css = readFileSync(path.join(dist, "katex.min.css"), "utf8");
  css = css.replace(/src:url\(fonts\/([^)]+?)\.woff2\) format\("woff2"\)(,url\([^)]+\) format\("[^"]+"\))*/g, (_m, name) => {
    const b64 = readFileSync(path.join(dist, "fonts", name + ".woff2")).toString("base64");
    return `src:url(data:font/woff2;base64,${b64}) format("woff2")`;
  });
  if (/url\(fonts\//.test(css)) throw new Error("un-inlined font reference left in katex css");
  writeFileSync(process.argv[3], css);
  process.exit(0);
}

const decode = (s) =>
  s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&");

const src = readFileSync(process.argv[2], "utf8");
const parts = src.split(/(<pre\b[\s\S]*?<\/pre>|<code\b[\s\S]*?<\/code>|<svg\b[\s\S]*?<\/svg>|<script\b[\s\S]*?<\/script>|<style\b[\s\S]*?<\/style>)/);
let count = 0;
const render = (tex, displayMode, where) => {
  count++;
  try {
    return katex.renderToString(decode(tex).trim(), { displayMode, throwOnError: true, output: "htmlAndMathml", strict: "ignore" });
  } catch (e) {
    throw new Error(`KaTeX error in ${where}: ${e.message}\n  source: ${tex.slice(0, 160)}`);
  }
};
const out = parts.map((chunk, i) => {
  if (i % 2 === 1) return chunk; // protected block
  let c = chunk.replace(/\$\$([\s\S]+?)\$\$/g, (_m, t) => `<span class="math-display">${render(t, true, "display math")}</span>`);
  c = c.replace(/\$([^$\n]+?)\$/g, (_m, t) => render(t, false, "inline math"));
  if (c.includes("$")) {
    const at = c.indexOf("$");
    throw new Error(`unpaired $ near: ${c.slice(Math.max(0, at - 80), at + 80)}`);
  }
  return c;
});
writeFileSync(process.argv[3], out.join(""));
console.log(`math rendered: ${count}`);
