#!/usr/bin/env node
/**
 * PlaywrightBrowser-Automation 通用浏览器自动化引擎
 *
 * 基于 Playwright，模拟人类在浏览器中的完整操作：
 *   导航 / 点击 / 输入 / 填表 / 选择 / 悬停 / 截图 / 抓取数据 / 等待 / 人工介入
 *
 * 用法（四种模式）：
 *
 * 1) 智能意图模式（一句话驱动）：
 *    node browser.js --intent "登录并截图首页" --url http://example.com --user 账号 --pass 密码
 *
 * 2) 任务描述模式（精确控制）：
 *    node browser.js --task '{"url":"...","steps":[...]}'
 *    或读取 JSON 文件： node browser.js --task-file task.json
 *
 * 3) 命令行原语模式（单步操作）：
 *    node browser.js open <url>
 *    node browser.js screenshot <path> [--full]
 *
 * 4) 会话保持模式（keepalive）：
 *    任务加 "keepalive": true 时，任务结束后浏览器窗口不关闭，
 *    可通过 stateOutput 保存登录态供下次复用。
 *
 * 依赖自动检测：require('playwright') 失败时给出安装指引，
 * 并自动把脚本所在目录的 node_modules 加入模块搜索路径（NODE_PATH 兜底）。
 */

const fs = require('fs');
const path = require('path');

// ---------- 依赖检测（含 NODE_PATH 兜底） ----------
(function addModulePath() {
  const local = path.join(__dirname, 'node_modules');
  if (fs.existsSync(local)) {
    const cur = process.env.NODE_PATH || '';
    process.env.NODE_PATH = cur ? `${local}${path.delimiter}${cur}` : local;
    require('module').Module._initPaths();
  }
})();

let playwright;
try {
  playwright = require('playwright');
} catch (e) {
  console.error('[browser-automation] 未找到 playwright 依赖。');
  console.error('请先执行： npm install playwright');
  console.error('（若需使用系统 Edge/Chrome，无需下载浏览器内核）');
  process.exit(1);
}

const { chromium, firefox, webkit } = playwright;

// ---------- 默认浏览器内核探测 ----------
function findBrowser() {
  const candidates = [
    process.env.BROWSER_EXECUTABLE_PATH,
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
  ].filter(Boolean);
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

// ---------- 工具函数 ----------
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function argVal(argv, flag) {
  const i = argv.indexOf(flag);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : undefined;
}

// ---------- 操作原语执行器 ----------
async function execStep(page, ctx, step) {
  if (ctx.page) page = ctx.page;
  const t = step.type;
  const sel = step.selector;
  const wait = step.wait || ctx.defaultWait || 2000;

  switch (t) {
    case 'goto':
    case 'open': {
      await page.goto(step.url, { waitUntil: step.waitUntil || 'domcontentloaded', timeout: step.timeout || 30000 });
      await sleep(wait);
      break;
    }
    case 'click': {
      const ctxPage = ctx.page || page;
      const newPagePromise = ctx.context
        ? ctx.context.waitForEvent('page', { timeout: step.newTabTimeout || 8000 }).catch(() => null)
        : Promise.resolve(null);
      await ctxPage.click(sel, { timeout: step.timeout || 10000 });
      await sleep(wait);
      const newPage = await newPagePromise;
      if (newPage && step.switchToNewTab !== false) {
        await newPage.waitForLoadState('domcontentloaded', { timeout: 30000 }).catch(() => {});
        ctx.page = newPage;
        console.log('[click] 已切换到新标签页:', newPage.url());
      }
      break;
    }
    case 'dblclick': {
      await page.dblclick(sel);
      await sleep(wait);
      break;
    }
    case 'fill': {
      await page.fill(sel, step.value);
      await sleep(wait);
      break;
    }
    case 'type': {
      await page.type(sel, step.value, { delay: step.delay || 50 });
      await sleep(wait);
      break;
    }
    case 'press': {
      await page.press(sel || 'body', step.key);
      await sleep(wait);
      break;
    }
    case 'check': {
      await page.check(sel);
      await sleep(wait);
      break;
    }
    case 'uncheck': {
      await page.uncheck(sel);
      await sleep(wait);
      break;
    }
    case 'select': {
      await page.selectOption(sel, step.value);
      await sleep(wait);
      break;
    }
    case 'hover': {
      await page.hover(sel);
      await sleep(wait);
      break;
    }
    case 'scroll': {
      const dir = step.direction || 'bottom';
      if (dir === 'bottom') await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      else if (dir === 'top') await page.evaluate(() => window.scrollTo(0, 0));
      else await page.evaluate(y => window.scrollBy(0, y), step.px || 500);
      await sleep(wait);
      break;
    }
    case 'screenshot': {
      const p = step.path || `screenshot_${Date.now()}.png`;
      const dir = path.dirname(p);
      if (dir && dir !== '.' && !fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      await page.screenshot({ path: p, fullPage: !!step.full });
      console.log('[screenshot]', p);
      break;
    }
    case 'wait': {
      await sleep(step.ms || wait);
      break;
    }
    case 'waitSelector': {
      await page.waitForSelector(sel, { timeout: step.timeout || 30000 });
      break;
    }
    case 'waitText': {
      await page.waitForSelector(`text=${step.text}`, { timeout: step.timeout || 30000 });
      break;
    }
    case 'eval': {
      const r = await page.evaluate(step.js);
      if (step.var) ctx.vars[step.var] = r;
      else console.log('[eval]', JSON.stringify(r));
      break;
    }
    case 'text': {
      const r = await page.evaluate(s => {
        const el = s ? document.querySelector(s) : document.body;
        return el ? el.innerText : '';
      }, sel);
      if (step.var) ctx.vars[step.var] = r;
      else if (step.output) fs.writeFileSync(step.output, r, 'utf8');
      else console.log('[text]', r.slice(0, 2000));
      break;
    }
    case 'html': {
      const r = await page.evaluate(s => {
        const el = s ? document.querySelector(s) : document.documentElement;
        return el ? el.outerHTML : '';
      }, sel);
      if (step.var) ctx.vars[step.var] = r;
      else if (step.output) fs.writeFileSync(step.output, r, 'utf8');
      else console.log('[html]', r.slice(0, 2000));
      break;
    }
    case 'title': {
      const r = await page.title();
      if (step.var) ctx.vars[step.var] = r;
      else console.log('[title]', r);
      break;
    }
    case 'url': {
      const r = page.url();
      if (step.var) ctx.vars[step.var] = r;
      else console.log('[url]', r);
      break;
    }
    case 'reload': {
      await page.reload();
      await sleep(wait);
      break;
    }
    case 'back': {
      await page.goBack();
      await sleep(wait);
      break;
    }
    case 'forward': {
      await page.goForward();
      await sleep(wait);
      break;
    }
    case 'login': {
      const user = step.user || process.env.BROWSER_USER;
      const pass = step.pass || process.env.BROWSER_PASS;
      if (!user || !pass) {
        throw new Error('login 缺少凭证：请通过步骤参数 user/pass 或环境变量 BROWSER_USER/BROWSER_PASS 提供');
      }
      await page.fill(step.userSelector || 'input[placeholder="用户名"]', user);
      await page.fill(step.passSelector || 'input[placeholder="密码"]', pass);
      await page.click(step.buttonSelector || 'button:has-text("登")');
      await sleep(step.waitAfter || 5000);
      break;
    }
    case 'waitLogin': {
      // 人工登录：可选预填账号密码，保持窗口等待用户手动输入验证码并登录。
      if (step.user) {
        await page.fill(step.userSelector || 'input[placeholder*="账号"], input[placeholder*="用户名"]', step.user).catch(() => {});
      }
      if (step.pass) {
        await page.fill(step.passSelector || 'input[type="password"]', step.pass).catch(() => {});
      }
      console.log('[waitLogin] 请在浏览器窗口中手动完成登录（如输入验证码）。等待中...');

      const timeout = step.timeout || 180000;
      const interval = step.interval || 1500;
      const menuSel = step.menuSelector || '.el-menu, .el-aside, .sidebar, aside, nav, .ant-menu';
      const deadline = Date.now() + timeout;
      let ok = false;
      while (Date.now() < deadline) {
        const u = page.url();
        const hasMenu = await page.locator(menuSel).count().catch(() => 0);
        const title = await page.title().catch(() => '');
        const stillLogin = u.includes('login') || title.includes('登录');
        if ((hasMenu > 0) || (!stillLogin && title && !title.includes('登录') && u.includes('#'))) {
          ok = true;
          break;
        }
        await sleep(interval);
      }
      if (!ok) {
        throw new Error(`waitLogin 超时（${Math.round(timeout / 1000)}s）未检测到登录成功`);
      }
      console.log('[waitLogin] 登录成功:', page.url());
      if (ctx.statePath) {
        await ctx.context.storageState({ path: ctx.statePath });
        console.log('[waitLogin] 登录态已保存:', ctx.statePath);
      }
      break;
    }
    case 'saveState': {
      const p = step.path || ctx.statePath || 'auth.json';
      await ctx.context.storageState({ path: p });
      console.log('[saveState]', p);
      break;
    }
    case 'close': {
      await page.close();
      break;
    }
    case 'menuWalk': {
      const shotDir = step.shotDir || './menu_shots';
      if (!fs.existsSync(shotDir)) fs.mkdirSync(shotDir, { recursive: true });

      const menuInfo = await page.evaluate((sel) => {
        const root = sel ? document.querySelector(sel) : document.querySelector('.el-menu, .ant-menu, .sidebar, aside, nav');
        if (!root) return { items: [] };
        const items = [];
        const seen = new Set();
        const push = (el) => {
          const text = (el.innerText || '').trim().split('\n')[0].trim();
          const cls = el.className || '';
          if (cls.includes('sub-menu') && !cls.includes('menu-item')) {
            el.querySelectorAll('.el-menu-item, .ant-menu-item, [class*="menu-item"]').forEach(c => push(c));
            return;
          }
          if (!text || text.length > 40 || seen.has(text)) return;
          seen.add(text);
          const sub = el.closest('.el-sub-menu');
          items.push({ text, cls, top: sub ? (sub.innerText.split('\n')[0] || text).trim() : text });
        };
        root.querySelectorAll('.el-menu-item, .ant-menu-item, .el-sub-menu, .ant-menu-submenu, li').forEach(push);
        return { items };
      }, step.menuSelector || null);

      const items = menuInfo.items;
      console.log(`[menuWalk] 检测到 ${items.length} 个菜单项`);

      const results = [];
      for (let i = 0; i < items.length; i++) {
        const { text: name, top } = items[i];
        try {
          if (step.expandTop !== false && top && top !== name) {
            const sub = page.locator('.el-sub-menu, .ant-menu-submenu', { hasText: top }).first();
            if (await sub.count() > 0) {
              const opened = await sub.evaluate(el => el.classList.contains('is-opened') || el.classList.contains('ant-menu-submenu-open'));
              if (!opened) {
                await sub.locator('.el-sub-menu__title, .ant-menu-submenu-title').click().catch(() => {});
                await sleep(500);
              }
            }
          }
          const item = page.locator('.el-menu-item, .ant-menu-item, [class*="menu-item"]', { hasText: name }).first();
          if (await item.count() === 0) { results.push({ index: i, name, clicked: false, error: '未找到可点击元素' }); continue; }
          await item.click().catch(() => {});
          await sleep(step.waitEach || 2000);
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await sleep(400);
          await page.evaluate(() => window.scrollTo(0, 0));

          const safe = name.replace(/[\/\\:*?"<>|]/g, '_');
          const shotPath = path.join(shotDir, `${String(i).padStart(2, '0')}_${safe}.png`);
          await page.screenshot({ path: shotPath, fullPage: !!step.full }).catch(() => {});
          const text = await page.evaluate(() => document.body.innerText).catch(() => '');
          results.push({ index: i, name, top, clicked: true, url: page.url(), shotPath, textLen: text.length, text: step.captureText ? text : undefined });
          console.log(`[menuWalk ${i}] ${name} -> ${shotPath}`);
        } catch (e) {
          results.push({ index: i, name, clicked: false, error: e.message.slice(0, 120) });
          console.warn(`[menuWalk ${i}] ${name} 失败: ${e.message.slice(0, 120)}`);
        }
      }

      if (step.var) ctx.vars[step.var] = results;
      if (step.output) {
        const outDir = path.dirname(step.output);
        if (outDir && outDir !== '.' && !fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
        fs.writeFileSync(step.output, JSON.stringify(results, null, 2), 'utf8');
      }
      break;
    }
    case 'export': {
      const data = step.var ? ctx.vars[step.var] : ctx.vars;
      const file = step.path || 'export.json';
      const fmt = step.format || (file.endsWith('.csv') ? 'csv' : 'json');
      const dir = path.dirname(file);
      if (dir && dir !== '.' && !fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      if (fmt === 'csv' && Array.isArray(data)) {
        const headers = step.columns || Object.keys(data[0] || {});
        const lines = [headers.join(',')];
        data.forEach(row => {
          lines.push(headers.map(h => {
            const v = row[h] === undefined ? '' : String(row[h]);
            return /[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v;
          }).join(','));
        });
        fs.writeFileSync(file, lines.join('\n'), 'utf8');
      } else {
        fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
      }
      console.log(`[export] ${file}`);
      break;
    }
    default: {
      console.warn('[warn] 未知操作类型:', t);
    }
  }
}

// ---------- 任务模式 ----------
async function runTask(task) {
  const engine = task.engine || 'chromium';
  const browsers = { chromium, firefox, webkit };
  const launchOpts = {
    headless: task.headed ? false : (task.headless !== undefined ? task.headless : true),
    args: ['--no-sandbox'],
  };
  const exe = task.executablePath || findBrowser();
  if (exe) launchOpts.executablePath = exe;

  const statePath = task.storageState || null;

  const browser = await browsers[engine].launch(launchOpts);
  const ctxOpts = { viewport: task.viewport || { width: 1600, height: 900 } };
  if (statePath && fs.existsSync(statePath)) {
    ctxOpts.storageState = statePath;
    console.log('[state] 已加载登录态:', statePath);
  }
  const context = await browser.newContext(ctxOpts);
  const page = await context.newPage();

  if (task.listenConsole) {
    page.on('console', m => console.log('[console]', m.type(), m.text().slice(0, 200)));
    page.on('pageerror', e => console.log('[pageerror]', String(e).slice(0, 300)));
  }

  const ctx = {
    vars: {},
    defaultWait: task.defaultWait,
    context,
    page,
    statePath: task.stateOutput || statePath || null,
  };

  if (task.url && task.steps.length > 0 && task.steps[0].type !== 'goto' && task.steps[0].type !== 'open') {
    await page.goto(task.url, { waitUntil: 'domcontentloaded', timeout: task.timeout || 30000 });
    await sleep(task.initialWait || 3000);
  }

  let keepalive = !!task.keepalive;
  try {
    for (let i = 0; i < task.steps.length; i++) {
      const step = task.steps[i];
      try {
        console.log(`[step ${i + 1}/${task.steps.length}] ${step.type}`);
        await execStep(page, ctx, step);
      } catch (e) {
        console.error(`[step ${i + 1} 失败] ${step.type}: ${e.message.slice(0, 300)}`);
        if (task.continueOnError) continue;
        else throw e;
      }
    }

    if (task.outputVars) {
      fs.writeFileSync(task.outputVars, JSON.stringify(ctx.vars, null, 2), 'utf8');
      console.log('[outputVars]', task.outputVars);
    }
    console.log('=== 任务完成 ===');
  } catch (e) {
    keepalive = false;
    throw e;
  } finally {
    if (keepalive) {
      console.log('[keepalive] 任务已完成，浏览器保持打开。');
      if (task.stateOutput) {
        await context.storageState({ path: task.stateOutput }).catch(() => {});
        console.log('[state] 登录态已保存:', task.stateOutput);
      }
      if (task.keepaliveTimeout) {
        console.log(`[keepalive] ${Math.round(task.keepaliveTimeout / 1000)}s 后自动关闭。`);
        await sleep(task.keepaliveTimeout);
        await browser.close();
        console.log('[keepalive] 已关闭浏览器。');
      } else {
        await sleep(24 * 3600 * 1000);
      }
    } else {
      await browser.close();
    }
  }
}

// ---------- 原语模式 ----------
async function runPrimitive(args) {
  const cmd = args[0];
  const browser = await chromium.launch({ headless: false, executablePath: findBrowser() || undefined, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });

  try {
    switch (cmd) {
      case 'open':
        await page.goto(args[1], { waitUntil: 'domcontentloaded', timeout: 30000 });
        await sleep(3000);
        console.log('[open]', page.url(), '|', await page.title());
        break;
      case 'screenshot':
        await page.screenshot({ path: args[1] || 'shot.png', fullPage: args.includes('--full') });
        console.log('[screenshot] saved', args[1]);
        break;
      case 'text':
        console.log(await page.evaluate(() => document.body.innerText));
        break;
      case 'title':
        console.log(await page.title());
        break;
      case 'url':
        console.log(page.url());
        break;
      default:
        console.error('未知原语命令:', cmd);
        console.error('支持: open <url> | screenshot <path> [--full] | text | title | url');
    }
  } finally {
    await browser.close();
  }
}

// ---------- 智能意图编排 ----------
function parseIntent(intent, opts) {
  const steps = [];
  const url = opts.url;
  const user = opts.user || process.env.BROWSER_USER;
  const pass = opts.pass || process.env.BROWSER_PASS;
  const shotDir = opts.shotDir || './shots';

  const has = kw => intent.includes(kw);

  if (has('登录') || has('登陆') || has('login')) {
    if (has('验证码') || has('人工')) {
      steps.push({ type: 'waitLogin', user, pass, timeout: opts.loginTimeout });
    } else {
      steps.push({ type: 'login', user, pass, waitAfter: opts.loginWait || 5000 });
    }
  }
  if (has('截图') || has('全屏') || has('screenshot')) {
    const full = has('全屏');
    if (has('遍历菜单') || has('每个页面') || has('所有页面') || has('菜单遍历')) {
      steps.push({ type: 'menuWalk', shotDir, full });
    } else {
      steps.push({ type: 'screenshot', path: opts.shotPath || path.join(shotDir, 'page.png'), full });
    }
  }
  if (has('文本') || has('内容') || has('文字') || has('text')) {
    steps.push({ type: 'text', output: opts.textOutput || 'page.txt' });
  }
  if (has('标题') || has('title')) {
    steps.push({ type: 'title', var: 'title' });
  }
  if (has('网址') || has('url') || has('地址')) {
    steps.push({ type: 'url', var: 'url' });
  }
  if (opts.clickSelector) {
    steps.push({ type: 'click', selector: opts.clickSelector });
  }
  if (opts.fillSelector && opts.fillValue) {
    steps.push({ type: 'fill', selector: opts.fillSelector, value: opts.fillValue });
  }
  if (steps.length === 0) {
    steps.push({ type: 'screenshot', path: opts.shotPath || path.join(shotDir, 'page.png'), full: true });
  }

  return { url, steps, outputVars: opts.outputVars };
}

// ---------- 入口 ----------
async function main() {
  const argv = process.argv.slice(2);

  const itIdx = argv.indexOf('--intent');
  if (itIdx >= 0) {
    const intent = argv[itIdx + 1];
    const opts = {
      url: argVal(argv, '--url'),
      user: argVal(argv, '--user'),
      pass: argVal(argv, '--pass'),
      shotDir: argVal(argv, '--shot-dir'),
      shotPath: argVal(argv, '--shot-path'),
      textOutput: argVal(argv, '--text-output'),
      outputVars: argVal(argv, '--output-vars'),
      clickSelector: argVal(argv, '--click'),
      fillSelector: argVal(argv, '--fill-selector'),
      fillValue: argVal(argv, '--fill-value'),
      loginWait: argVal(argv, '--login-wait'),
      loginTimeout: argVal(argv, '--login-timeout'),
    };
    if (!opts.url) { console.error('--intent 需要配合 --url 指定目标网址'); process.exit(1); }
    const task = parseIntent(intent, opts);
    console.log('[intent] 解析为步骤:', task.steps.map(s => s.type).join(' -> '));
    return runTask(task);
  }

  const tfIdx = argv.indexOf('--task-file');
  if (tfIdx >= 0) {
    const task = JSON.parse(fs.readFileSync(argv[tfIdx + 1], 'utf8'));
    return runTask(task);
  }
  const tIdx = argv.indexOf('--task');
  if (tIdx >= 0) {
    const task = JSON.parse(argv[tIdx + 1]);
    return runTask(task);
  }
  if (argv.length > 0) {
    return runPrimitive(argv);
  }

  console.log(`PlaywrightBrowser-Automation 通用浏览器自动化引擎

智能意图模式（A，一句话驱动）：
  node browser.js --intent "登录并截图首页" --url http://example.com --user 账号 --pass 密码
  node browser.js --intent "人工登录并遍历菜单截图" --url http://example.com --user 账号 --pass 密码 --shot-dir D:/shots

任务模式（B，精确控制）：
  node browser.js --task '{"url":"...","steps":[...]}'
  node browser.js --task-file task.json

原语模式（单步）：
  node browser.js open <url>
  node browser.js screenshot <path> [--full]
  node browser.js text | title | url

任务 steps 支持的操作类型：
  goto/open, click, dblclick, fill, type, press, check, uncheck,
  select, hover, scroll, screenshot, wait, waitSelector, waitText,
  eval, text, html, title, url, reload, back, forward,
  login, waitLogin（人工登录/验证码）, saveState（保存登录态）,
  menuWalk（多级菜单遍历截图）, export（导出 JSON/CSV）, close

关键任务字段：
  headless/headed  无头/有头
  executablePath   指定浏览器内核路径
  storageState     加载已有登录态 JSON（免重复登录）
  stateOutput      登录成功后保存登录态到该 JSON
  keepalive        任务结束后保持浏览器窗口不关闭
  keepaliveTimeout 保持时长（ms），缺省无限

环境变量：
  BROWSER_EXECUTABLE_PATH  指定浏览器内核路径
  BROWSER_USER / BROWSER_PASS  登录凭证（不写死脚本）
  BROWSER_HEADED  非空则显示浏览器窗口
  `);
}

main().catch(e => { console.error('[FATAL]', e); process.exit(1); });
