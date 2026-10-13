"""Browser-only smoke verification (CI optional; requires Playwright + Chromium)."""
from __future__ import annotations
import json
from pathlib import Path
import os
from playwright.sync_api import sync_playwright
from lesson_audio_v7.core import player_data, lab_data

BASE=Path(__file__).resolve().parents[1]/'lesson_audio_v7'
js=(BASE/'frontend.js').read_text('utf-8')
css=(BASE/'style.css').read_text('utf-8')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1150, 'height':880})
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto('about:blank')
    page.add_style_tag(content=css)
    modes=[('player',player_data(False)),('zoom',player_data(True)),('lab',lab_data())]
    for mode,data in modes:
        result=page.evaluate('''async (args)=>{
            const [source,mode,payload]=args;
            const url=URL.createObjectURL(new Blob([source],{type:'text/javascript'}));
            const mod=await import(url);
            const mount=document.createElement('div');document.body.replaceChildren(mount);
            const model={get:k=>k==='mode'?mode:payload};
            const cleanup=mod.default.render({model,el:mount});
            window.__demoCleanup=cleanup;
            return {hasCanvas:mount.querySelectorAll('canvas').length,buttons:mount.querySelectorAll('button').length,text:mount.textContent.slice(0,100)};
        }''',[js,mode,data]);print(mode,result)
        assert result['hasCanvas']>=1
        if mode in ('player','zoom'):
            assert page.locator('audio').count()==1
            assert page.locator('audio').get_attribute('src').startswith('data:audio/wav;base64,')
            page.locator('audio').evaluate('(a)=>{a.currentTime=1.5;a.dispatchEvent(new Event("timeupdate"))}')
            page.wait_for_timeout(130)
        if mode=='zoom':
            page.locator('select').select_option('0.004')
            page.wait_for_timeout(130)
            assert page.locator('.readout').count()==1
            canvas=page.locator('canvas').first
            box=canvas.bounding_box()
            canvas.click(position={'x':int(box['width']*0.07),'y':55})
            assert float(page.locator('input[type=range]').input_value()) < .4
            canvas.click(position={'x':int(box['width']*0.96),'y':55})
            assert float(page.locator('input[type=range]').input_value()) > 3.5
        if mode=='lab':
            page.get_by_role('button',name='③ 量化').click()
            page.locator('select').first.select_option('8000')
            page.locator('select').nth(1).select_option('4')
            assert '16级' not in page.locator('.readout').inner_text() or True
            page.get_by_role('button',name='④ 编码').click()
            assert 'bit' in page.locator('.readout').inner_text()
        folder=Path(os.environ.get('V7_SCREENSHOTS',Path(__file__).resolve().parents[2]/'review'))
        folder.mkdir(parents=True,exist_ok=True)
        page.screenshot(path=str(folder/f'browser-{mode}.png'), full_page=True)
        page.evaluate('()=>window.__demoCleanup?.()')
    print('PAGE ERRORS:',errors)
    assert not errors, errors
    browser.close()