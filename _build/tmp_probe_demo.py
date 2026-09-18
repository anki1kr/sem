"""Layout probe in headless Chrome: SVG text overlaps / text outside viewBox / text escaping its shape,
CSS diagram boxes overflowing, figures wider than the page at 390px. Usage: python probe.py [key ...]"""
import subprocess, sys, re, json, html
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
SEM5 = Path("demo_out")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FOLDERS = {"java": "java", "daav": "DAAV", "ml": "ML", "se": "SE", "speech": "Speech Audio"}

PROBE = r"""
<script>
window.addEventListener('load',function(){setTimeout(function(){
var res=[];
function cap(el){var f=el.closest('figure');var c=f&&f.querySelector('figcaption');return c?c.textContent.slice(0,40):'?';}
document.querySelectorAll('svg.sv').forEach(function(svg){
  var vb=svg.viewBox.baseVal, texts=[].slice.call(svg.querySelectorAll('text')), bb=[];
  texts.forEach(function(t){var b=t.getBBox();bb.push(b);
    if(b.x<vb.x-1||b.y<vb.y-1||b.x+b.width>vb.x+vb.width+1||b.y+b.height>vb.y+vb.height+1)
      res.push(['outside-viewBox',cap(svg),t.textContent]);});
  for(var i=0;i<bb.length;i++)for(var j=i+1;j<bb.length;j++){var a=bb[i],b=bb[j];
    var ox=Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x), oy=Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y);
    if(ox>2&&oy>2)res.push(['text-overlap',cap(svg),texts[i].textContent+' | '+texts[j].textContent]);}
  // text centre inside a rect but text wider than rect
  var rects=[].slice.call(svg.querySelectorAll('rect'));
  texts.forEach(function(t,i){var b=bb[i],cx=b.x+b.width/2,cy=b.y+b.height/2;
    rects.forEach(function(r){var x=r.x.baseVal.value,y=r.y.baseVal.value,w=r.width.baseVal.value,h=r.height.baseVal.value;
      if(cx>x&&cx<x+w&&cy>y&&cy<y+h&&w<vb.width*0.9&&(b.width>w-4||b.height>h))res.push(['text-exceeds-rect',cap(svg),t.textContent]);});});
});
document.querySelectorAll('.n,.tree span,.stack .l,.boxes .b').forEach(function(el){
  if(el.scrollWidth>el.clientWidth+2)res.push(['css-box-overflow',cap(el),el.textContent.slice(0,40)]);});
var pre=document.createElement('pre');pre.id='PROBE';pre.textContent=JSON.stringify(res);document.body.appendChild(pre);
},300);});
</script>
"""

for key in sys.argv[1:] or list(FOLDERS):
    src = SEM5 / FOLDERS[key] / f"{key}-sessional-u1-u2.html"
    if not src.exists():
        print(key, "not built"); continue
    s = src.read_text(encoding="utf-8")
    i = s.rindex("</body>")
    tmp = HERE / "tmp" / f"probe-{key}.html"
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(s[:i] + PROBE + s[i:], encoding="utf-8")
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=4000", "--window-size=900,1200",
                        "--dump-dom", tmp.resolve().as_uri()], capture_output=True, text=True, encoding="utf-8", timeout=120)
    m = re.search(r'<pre id="PROBE">(.*?)</pre>', r.stdout, flags=re.S)
    if not m:
        print(key, "probe did not run"); continue
    res = json.loads(html.unescape(m.group(1)))
    print(f"== {key}: {len(res)} issues")
    for x in res:
        print("  ", x)
