# report_renderer.py
import html
from pathlib import Path
from typing import Dict, Any

CSS = r"""
:root{
 --blue:#4285f4;--purple:#9b72cb;--pink:#d96570;--green:#34a853;--red:#ea4335;--yellow:#fbbc05;
 --ink:#202124;--ink2:#5f6368;--ink3:#80868b;--line:#e8eaed;--bg:#f6f8fc;--card:#fff;
 --grad:linear-gradient(120deg,#4285f4 0%,#9b72cb 55%,#d96570 100%);
 --shadow:0 8px 30px rgba(60,64,67,.08);--shadow-hi:0 18px 48px rgba(60,64,67,.14);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Google Sans','Product Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Microsoft YaHei',sans-serif;
 background:var(--bg);color:var(--ink);line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px 72px}
.hero{position:relative;overflow:hidden;padding:58px 0 48px;border-radius:0 0 40px 40px;
 background:linear-gradient(135deg,#fff 0%,#f2f5ff 52%,#fdf2f6 100%);box-shadow:0 10px 40px rgba(60,64,67,.05);margin-bottom:40px}
.orb{position:absolute;border-radius:50%;filter:blur(72px);opacity:.42;animation:float 16s ease-in-out infinite}
.orb.a{width:390px;height:390px;background:#bfd4ff;top:-160px;left:-100px}
.orb.b{width:330px;height:330px;background:#e2ccff;top:-50px;right:-80px;animation-delay:-5s}
.orb.c{width:290px;height:290px;background:#ffd2df;bottom:-170px;left:42%;animation-delay:-10s}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(26px,-24px)}}
.hero-in{position:relative;z-index:2;max-width:1180px;margin:0 auto;padding:0 26px}
.brand{display:flex;align-items:center;gap:12px;margin-bottom:22px}
.brand svg{width:38px;height:38px;filter:drop-shadow(0 5px 12px rgba(155,114,203,.35))}
.brand span{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2);font-weight:700}
.hero h1{font-size:clamp(30px,5vw,50px);line-height:1.16;letter-spacing:-.025em;font-weight:700;
 background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{margin-top:12px;color:var(--ink2);font-size:16px;max-width:720px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.chip{display:inline-flex;align-items:center;gap:8px;padding:8px 15px;border-radius:999px;background:rgba(255,255,255,.88);
 border:1px solid var(--line);font-size:13px;color:var(--ink2);box-shadow:0 2px 10px rgba(60,64,67,.05);backdrop-filter:blur(6px)}
.chip b{color:var(--ink);font-weight:650}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot.g{background:var(--green);box-shadow:0 0 0 4px rgba(52,168,83,.14)}
.dot.r{background:var(--red);box-shadow:0 0 0 4px rgba(234,67,53,.14)}
.sec{margin-top:46px}
.sec-h{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.sec-h .bar{width:4px;height:24px;border-radius:4px;background:var(--grad)}
.sec-h h2{font-size:21px;font-weight:680;letter-spacing:-.01em}
.sec-h .hint{margin-left:auto;font-size:12px;color:var(--ink3)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}
.stat{position:relative;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:20px 20px 18px;
 box-shadow:var(--shadow);overflow:hidden;opacity:0;animation:rise .55s ease forwards;transition:transform .25s,box-shadow .25s}
.stat:hover{transform:translateY(-5px);box-shadow:var(--shadow-hi)}
.stat:nth-child(1){animation-delay:.04s}.stat:nth-child(2){animation-delay:.11s}.stat:nth-child(3){animation-delay:.18s}
.stat:nth-child(4){animation-delay:.25s}.stat:nth-child(5){animation-delay:.32s}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.stat::after{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:var(--grad)}
.stat .k{font-size:12px;color:var(--ink3);font-weight:600;letter-spacing:.04em}
.stat .v{font-size:29px;font-weight:720;letter-spacing:-.02em;margin-top:8px;line-height:1.2}
.stat .s{font-size:12px;color:var(--ink3);margin-top:5px}
.v.good{color:var(--green)}.v.bad{color:var(--red)}
.grid2{display:grid;grid-template-columns:minmax(280px,.85fr) minmax(320px,1.15fr);gap:18px}
@media(max-width:860px){.grid2{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px;box-shadow:var(--shadow)}
.card h3{font-size:15px;font-weight:680;margin-bottom:18px}
.donut-wrap{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.donut{width:132px;height:132px;border-radius:50%;display:grid;place-items:center;position:relative;flex:none}
.donut::after{content:"";position:absolute;inset:16px;border-radius:50%;background:#fff;box-shadow:inset 0 2px 10px rgba(60,64,67,.08)}
.donut .inner{position:relative;z-index:2;text-align:center}
.donut .inner b{font-size:25px;letter-spacing:-.02em}.donut .inner small{display:block;color:var(--ink3);font-size:11px}
.legend{font-size:13px;color:var(--ink2);display:grid;gap:9px}
.legend div{display:flex;align-items:center;gap:9px}
.bars{display:grid;gap:15px}
.bar-row{display:grid;grid-template-columns:120px 1fr 58px;align-items:center;gap:12px;font-size:12px;color:var(--ink2)}
.track{height:9px;border-radius:99px;background:#eef0f4;overflow:hidden}
.fill{height:100%;border-radius:99px;background:var(--grad);width:0;transition:width 1s cubic-bezier(.2,.8,.2,1)}
.bar-row .val{text-align:right;color:var(--ink);font-weight:650;font-variant-numeric:tabular-nums}
.timeline{position:relative;padding-left:8px}
.timeline::before{content:"";position:absolute;left:19px;top:14px;bottom:14px;width:2px;background:linear-gradient(#4285f4,#9b72cb,#e8eaed)}
.tl-item{position:relative;display:flex;gap:18px;padding:0 0 22px 0}
.tl-item:last-child{padding-bottom:0}
.tl-dot{width:24px;height:24px;border-radius:50%;background:var(--green);border:4px solid #e8f5e9;flex:none;z-index:2;margin-top:16px}
.tl-dot.fail{background:var(--red);border-color:#fdecea}
.tl-dot.pending{background:#bdc1c6;border-color:#f1f3f4}
.tl-body{flex:1;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 20px;box-shadow:var(--shadow)}
.tl-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.tl-top b{font-size:15px}.tl-top .t{font-size:12px;color:var(--ink3);margin-left:auto;font-variant-numeric:tabular-nums}
.tl-toggle{margin-left:auto;background:transparent;border:0;font-size:16px;cursor:pointer;color:var(--ink3);transition:transform 0.2s}
.tl-item.open .tl-toggle{transform:rotate(180deg);}
.tl-collapse{display:none;margin-top:12px}
.tl-item.open .tl-collapse{display:block}
.tl-thumb{max-width:280px;border-radius:12px;cursor:pointer;border:1px solid var(--line)}
.tl-detail{font-size:13px;color:var(--ink2);margin-top:6px;word-break:break-all}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;letter-spacing:.03em}
.badge.ok{background:#e6f4ea;color:#137333}.badge.no{background:#fce8e6;color:#c5221f}.badge.wait{background:#f1f3f4;color:#5f6368}
.step-scroll{max-height:430px;overflow:auto;border-radius:14px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:12px 14px;color:var(--ink3);font-weight:650;font-size:11px;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid var(--line)}
td{padding:11px 14px;border-bottom:1px solid #f1f3f4;color:var(--ink2)}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:#fafbff}
td.idx{color:var(--ink3);font-variant-numeric:tabular-nums;width:42px}
.products{display:grid;gap:10px}
.product{display:flex;align-items:center;gap:12px;padding:11px 14px;border:1px solid var(--line);border-radius:14px;background:#fafbff}
.product .ic{width:34px;height:34px;border-radius:10px;background:var(--grad);display:grid;place-items:center;color:#fff;flex:none}
.product .nm{font-size:13px;font-weight:600;color:var(--ink)}
.product .pr{margin-left:auto;font-size:13px;font-weight:680;color:var(--ink)}
.totals{display:grid;gap:8px;margin-top:16px;font-size:13px}
.totals div{display:flex;justify-content:space-between;color:var(--ink2)}
.totals div.last{padding-top:10px;border-top:1px dashed var(--line);font-size:15px;font-weight:700;color:var(--ink)}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.shot{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:var(--shadow)}
.shot img{width:100%;height:150px;object-fit:cover;object-position:top;display:block;cursor:pointer}
.shot figcaption{padding:10px 14px;font-size:12px;color:var(--ink2);border-top:1px solid var(--line)}
details{margin-top:16px;font-size:12px;color:var(--ink2)}
summary{cursor:pointer;font-weight:600;color:var(--ink)}
pre{margin-top:10px;background:#202124;color:#e8eaed;padding:16px;border-radius:14px;max-height:280px;overflow:auto;font-size:11px;line-height:1.55;white-space:pre-wrap;word-break:break-all}
footer{margin-top:52px;text-align:center;font-size:12px;color:var(--ink3)}
/* lightbox 弹窗 */
#lightbox{position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:9999;display:none;align-items:center;justify-content:center;padding:20px}
#lightbox img{max-width:90%;max-height:90%;border-radius:8px;cursor:pointer}
#lightbox.show{display:flex}
@media print{.orb{display:none}.hero{border-radius:0}.stat,.tl-body,.card{box-shadow:none;opacity:1}.step-scroll{max-height:none;overflow:visible}body{background:#fff}}
"""

SVG_BRAND = """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="40" y2="40"><stop stop-color="#4285f4"/><stop offset=".55" stop-color="#9b72cb"/><stop offset="1" stop-color="#d96570"/></linearGradient></defs>
<path d="M20 2l3.6 10.4L34 16l-10.4 3.6L20 30l-3.6-10.4L6 16l10.4-3.6L20 2z" fill="url(#g)"/>
<circle cx="31" cy="30" r="4" fill="#fbbc05"/><circle cx="8" cy="31" r="2.6" fill="#34a853"/></svg>"""


def render_report(result: dict, report_path: Path, out_dir: Path) -> None:
    esc = lambda v: html.escape(str(v) if v is not None else "", quote=True)
    meta, summary = result["meta"], result["summary"]
    business = result["business"]
    ok = bool(meta["all_passed"])

    def rel(path: str | None) -> str:
        if not path:
            return ""
        try:
            return Path(path).relative_to(out_dir).as_posix()
        except ValueError:
            return Path(path).as_posix()

    pass_rate = summary["pass_rate"]
    fail_rate = round(summary["failed"] / summary["total_steps"] * 100, 1) if summary["total_steps"] else 0.0
    donut = (
        f"conic-gradient(#34a853 0 {pass_rate}%, #ea4335 {pass_rate}% {pass_rate + fail_rate}%, "
        f"#e8eaed {pass_rate + fail_rate}% 100%)"
    )

    durations = [p.get("duration_ms") or 0 for p in result["phases"]]
    max_dur = max(durations) if durations else 1

    parts: list[str] = []
    parts.append("<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'>")
    parts.append("<meta name='viewport' content='width=device-width,initial-scale=1.0'>")
    parts.append("<title>SauceDemo 自动化测试报告 · " + esc(meta["run_id"]) + "</title>")
    parts.append("<style>" + CSS + "</style></head><body>")
    parts.append("<div id='lightbox'><img id='lb-img' src='' alt='大图预览'></div>")
    parts.append("<header class='hero'><div class='orb a'></div><div class='orb b'></div><div class='orb c'></div><div class='hero-in'>")
    parts.append("<div class='brand'>" + SVG_BRAND + "<span>Test Intelligence · SauceDemo E2E</span></div>")
    parts.append("<h1>端到端自动化测试报告</h1>")
    parts.append("<p>Playwright CLI 有头模式驱动真实浏览器，完整走通登录、加购、购物车、收货信息与结算流程。</p>")
    parts.append("<div class='chips'>")
    dot_cls = "g" if ok else "r"
    verdict = "通过" if ok else "失败"
    parts.append(f"<span class='chip'><span class='dot {dot_cls}'></span>结果 <b>{verdict}</b></span>")
    parts.append(f"<span class='chip'>测试轮次 <b>{esc(meta['run_id'])}</b></span>")
    parts.append(f"<span class='chip'>站点 <b>{esc(meta['site'])}</b></span>")
    parts.append(f"<span class='chip'>账号 <b>{esc(meta['account'])}</b></span>")
    parts.append(f"<span class='chip'>模式 <b>{esc(meta['mode'])}</b></span>")
    parts.append("</div></div></header><main class='wrap'>")

    # 指标卡
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>核心指标</h2><span class='hint'>本轮数据概览</span></div><div class='stats'>")
    stat_data = [
        ("总体结果", "PASS" if ok else "FAIL", "good" if ok else "bad", ""),
        ("步骤通过率", f"{pass_rate}%", "", f"{summary['passed']} / {summary['total_steps']} 步通过"),
        ("执行步骤", str(summary["total_steps"]), "", f"失败 {summary['failed']} · 跳过 {summary['skipped']}"),
        ("总耗时", f"{meta['duration_seconds']}s", "", "含浏览器启动与截图"),
        ("订单总额", esc(business.get("total") or "—"), "", "结算页金额"),
    ]
    for k, v, cls, s in stat_data:
        parts.append(f"<div class='stat'><div class='k'>{esc(k)}</div><div class='v {cls}'>{v}</div><div class='s'>{esc(s)}</div></div>")
    parts.append("</div></section>")

    # 通过率 + 阶段耗时
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>执行质量与耗时</h2><span class='hint'>按阶段统计</span></div><div class='grid2'>")
    parts.append("<div class='card'><h3>步骤通过率</h3><div class='donut-wrap'>")
    parts.append(f"<div class='donut' style='background:{donut}'><div class='inner'><b>{pass_rate}%</b><small>通过率</small></div></div>")
    parts.append("<div class='legend'>")
    parts.append(f"<div><span class='dot g'></span>通过 {summary['passed']} 步</div>")
    parts.append(f"<div><span class='dot r'></span>失败 {summary['failed']} 步</div>")
    parts.append(f"<div><span style='width:8px;height:8px;border-radius:50%;display:inline-block;background:#bdc1c6'></span>未执行 {summary['skipped']} 步</div>")
    parts.append("</div></div></div>")
    parts.append("<div class='card'><h3>各阶段耗时（毫秒）</h3><div class='bars'>")
    for p in result["phases"]:
        dur = p.get("duration_ms") or 0
        width = min(100, round(dur / max_dur * 100)) if max_dur else 0
        parts.append(
            f"<div class='bar-row'><span>{esc(p['name'])}</span><div class='track'>"
            f"<div class='fill' data-w='{width}'></div></div><span class='val'>{dur}</span></div>"
        )
    parts.append("</div></div></section>")

    # 时间线（带下拉折叠缩略图）
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>流程时间线</h2><span class='hint'>点击箭头展开缩略图；点击图片放大预览</span></div><div class='timeline'>")
    for p in result["phases"]:
        state = p["status"]
        cls = "fail" if state == "failed" else ("pending" if state != "passed" else "")
        badge = {"passed": ("ok", "通过"), "failed": ("no", "失败")}.get(state, ("wait", "未执行"))
        screenshot = rel(p.get("screenshot"))
        thumb_html = ""
        if screenshot:
            thumb_html = f'<img class="tl-thumb" src="{esc(screenshot)}" alt="{esc(p["name"])}">'
        err_msg = p.get("error_msg", "")
        err_html = f"<div style='color:var(--red);margin-top:6px'>【异常】{esc(err_msg)}</div>" if err_msg else ""

        parts.append(
            f"<div class='tl-item'><div class='tl-dot {cls}'></div><div class='tl-body'>"
            f"<div class='tl-top'><span class='badge {badge[0]}'>{badge[1]}</span><b>{esc(p['name'])}</b>"
            f"<span class='t'>{p.get('duration_ms') or '—'} ms</span>"
            f"<button class='tl-toggle'>▾</button></div>"
            f"<div class='tl-detail'>{esc(p.get('detail'))}</div>{err_html}"
            f"<div class='tl-collapse'>{thumb_html}</div></div></div>"
        )
    parts.append("</div></section>")

    # 步骤明细 + 订单信息
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>步骤明细</h2><span class='hint'>共 " + str(summary["total_steps"]) + " 步 · 可滚动</span></div><div class='card'><div class='step-scroll'><table>")
    parts.append("<thead><tr><th>#</th><th>阶段</th><th>操作</th><th>类型</th><th>状态</th></tr></thead><tbody>")
    for s in result["steps"]:
        badge = {"passed": ("ok", "通过"), "failed": ("no", "失败"), "skipped": ("wait", "跳过")}[s["status"]]
        parts.append(
            f"<tr><td class='idx'>{s['index']}</td><td>{esc(s['phase'])}</td><td>{esc(s['label'])}</td>"
            f"<td>{esc(s['type'])}</td><td><span class='badge {badge[0]}'>{badge[1]}</span></td></tr>"
        )
    parts.append("</tbody></table></div>")
    parts.append("</div></section>")

    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>业务数据核对</h2><span class='hint'>商品与金额</span></div><div class='grid2'>")
    parts.append("<div class='card'><h3>已加入购物车的商品</h3><div class='products'>")
    products = business.get("added_products") or []
    if not products:
        parts.append("<div style='font-size:13px;color:var(--ink3)'>未采集到商品数据</div>")
    for p in products:
        parts.append(
            "<div class='product'><div class='ic'>✦</div><div class='nm'>" + esc(p.get("name"))
            + "</div><div class='pr'>" + esc(p.get("price")) + "</div></div>"
        )
    parts.append("</div></div>")
    parts.append("<div class='card'><h3>订单金额</h3><div class='totals'>")
    for label, key in (("商品小计", "subtotal"), ("税费", "tax")):
        parts.append(f"<div><span>{label}</span><b>{esc(business.get(key) or '—')}</b></div>")
    parts.append(f"<div class='last'><span>合计</span><b>{esc(business.get('total') or '—')}</b></div>")
    parts.append("</div><div style='margin-top:18px;font-size:13px;color:var(--ink2)'>")
    parts.append("结算结果：<b style='color:" + ("var(--green)" if ok else "var(--red)") + "'>"
                 + esc(business.get("success_header") or "未完成") + "</b></div></div></section>")

    # 截图证据画廊
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>过程证据</h2><span class='hint'>点击图片放大预览</span></div><div class='gallery'>")
    for p in result["phases"]:
        src = rel(p.get("screenshot"))
        if not src:
            continue
        parts.append(f"<figure class='shot'><img src='{esc(src)}' alt='{esc(p['name'])}'>")
        parts.append(f"<figcaption>{esc(p['name'])}</figcaption></figure>")
    parts.append("</div>")
    parts.append("<details><summary>查看 CLI 原始日志</summary><pre>" + esc(result.get("cli_log", "")) + "</pre></details>")
    parts.append("</section>")

    parts.append("<footer>Generated by SauceDemo E2E · " + esc(meta["finished_at"])
                 + " · Run ID " + esc(meta["run_id"]) + "</footer>")
    # JS 交互：折叠切换 + lightbox
    parts.append("""
<script>
const lightbox = document.getElementById('lightbox');
const lbImg = document.getElementById('lb-img');
// 折叠切换
document.querySelectorAll('.tl-toggle').forEach(btn=>{
    btn.onclick = ()=>{
        const item = btn.closest('.tl-item');
        item.classList.toggle('open');
    }
})
// lightbox 打开
document.querySelectorAll('.tl-thumb, .gallery img').forEach(img=>{
    img.onclick = ()=>{
        lbImg.src = img.src;
        lightbox.classList.add('show');
    }
})
// 关闭
lightbox.onclick = ()=>{
    lightbox.classList.remove('show');
    lbImg.src = '';
}
// ESC关闭
document.addEventListener('keydown',e=>{
    if(e.key==='Escape') lightbox.classList.remove('show');
})
// 条形动画
window.addEventListener('load',function(){setTimeout(function(){
document.querySelectorAll('.fill').forEach(function(e){e.style.width=e.dataset.w+'%';});},120);});
</script>""")
    parts.append("</body></html>")
    report_path.write_text("\n".join(parts), encoding="utf-8")
