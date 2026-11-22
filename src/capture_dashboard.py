"""Capture the actual Streamlit UI in headless Edge; stop the owned server on exit."""
from common import *
import subprocess, urllib.request
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    dest=ROOT/'phase3_output/ui_upgrade';dest.mkdir(exist_ok=True,parents=True)
    with (dest/'dashboard_capture.log').open('w') as log:
        server=subprocess.Popen([sys.executable,'-m','streamlit','run',str(ROOT/'src/dashboard.py'),'--server.headless=true','--server.port=8507','--browser.gatherUsageStats=false'],stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            for _ in range(120):
                if server.poll() is not None:raise RuntimeError('Streamlit stopped; inspect capture log')
                try:
                    urllib.request.urlopen('http://localhost:8507/_stcore/health',timeout=1);break
                except Exception:time.sleep(.5)
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',headless=True)
                page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=2)
                page.goto('http://localhost:8507',wait_until='domcontentloaded')
                try:
                    page.get_by_role('heading',name='Quick Artwork Inspector',exact=True).wait_for(timeout=240000)
                except Exception:
                    (dest/'dashboard_browser_error.txt').write_text(page.locator('body').inner_text(),encoding='utf-8')
                    page.screenshot(path=str(dest/'dashboard_browser_error.png'))
                    raise
                page.locator('.js-plotly-plot').first.wait_for(timeout=120000)
                page.evaluate('document.fonts.ready')
                page.evaluate("Promise.all([400,500,600,700].map(w=>document.fonts.load(`${w} 14px Quicksand`)))")
                page.wait_for_timeout(1800)
                checks=[]
                def inspect(label):
                    assert page.locator('[data-testid="stException"]').count()==0
                    footer=page.locator('footer.footer');assert footer.inner_text()=='Wasil Kayani · Umer Asghar'
                    import re
                    assert not re.search(r'24[Ii]\s*[-–]?\s*(2551|2532)|i242551|i242532',page.locator('body').inner_text())
                    checks.append(label)
                inspect('landing browser and exact footer')
                fonts=page.evaluate("({body:document.fonts.check('500 14px Quicksand'),display:document.fonts.check('36px \"Titan One\"'),heading:getComputedStyle(document.querySelector('h1')).fontFamily})")
                assert fonts['body'] and fonts['display'],fonts
                page.locator('.stMainBlockContainer').screenshot(path=str(dest/'landing_full.png'))
                page.locator('[data-testid="stMain"]').evaluate('(el)=>el.scrollTop=0');page.wait_for_timeout(300)
                bottom=page.get_by_role('button',name='Open the gallery →').bounding_box()
                page.screenshot(path=str(dest/'landing_panel.png'),clip={'x':24,'y':45,'width':1392,'height':bottom['y']+bottom['height']-45+15})
                from dashboard_views import SHORT
                headings=['H–C Causality Atlas','Manifold & Fidelity','Spectral & Wavelet Profiles','Style Drift & Ablations','Forensic Error Gallery']
                for label,heading in zip(SHORT[1:],headings):
                    page.get_by_text(label,exact=True).click();page.get_by_role('heading',name=heading,exact=True).wait_for(timeout=180000)
                    expected={SHORT[1]:"p._fullLayout?.xaxis?.title?.text==='H_pooled'",SHORT[2]:"p._fullLayout?.xaxis?.title?.text==='PC1'",SHORT[3]:"p._fullLayout?.title?.text==='Hann-windowed 16-annulus FFT'",SHORT[4]:"p.data?.[0]?.type==='histogram2d'",SHORT[5]:"p._fullLayout?.title?.text?.startsWith('Radial FFT')"}[label]
                    page.wait_for_function("Array.from(document.querySelectorAll('.js-plotly-plot')).some(p=>"+expected+")",timeout=180000)
                    page.wait_for_function("document.querySelectorAll('[data-stale=\"true\"]').length===0",timeout=180000)
                    page.wait_for_timeout(1000);inspect(label)
                    if label==SHORT[1]:
                        page.locator('.stMainBlockContainer').screenshot(path=str(dest/'atlas_full.png'))
                        page.locator('[data-testid="stMain"]').evaluate('(el)=>el.scrollTop=0');page.wait_for_timeout(300)
                        box=page.locator('[data-testid="stPlotlyChart"]').first.bounding_box()
                        # Enlarge the browser viewport so the complete chart and legend are captured.
                        page.set_viewport_size({'width':1440,'height':max(1100,round(box['y']+box['height']+30))});page.wait_for_timeout(300)
                        page.screenshot(path=str(dest/'atlas_panel.png'),clip={'x':24,'y':45,'width':1392,'height':box['y']+box['height']-45+15})
                page.set_viewport_size({'width':390,'height':844});page.get_by_text(SHORT[0],exact=True).click()
                page.get_by_role('heading',name='Quick Artwork Inspector',exact=True).wait_for(timeout=180000);page.wait_for_timeout(500)
                assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+2')
                inspect('mobile landing without horizontal page overflow');page.screenshot(path=str(dest/'mobile_landing.png'))
                (dest/'browser_verification.json').write_text(json.dumps({'passed':True,'checks':checks,'fonts':fonts,'server_left_running':False},indent=2),encoding='utf-8')
                browser.close()
            panels=[Image.open(dest/f'{name}_panel.png').convert('RGB') for name in ['landing','atlas']]
            composite=Image.new('RGB',(panels[0].width,sum(im.height for im in panels)+32),'#FFFFFF');y=0
            for im in panels:composite.paste(im,(0,y));y+=im.height+32
            composite.save(ROOT/'figures/fig11_dashboard_ui.png',dpi=(300,300),optimize=True)
            for name in ['landing','atlas']:
                im=Image.open(dest/f'{name}_full.png').convert('RGB')
                im.thumbnail((1800,7000));im.save(ROOT/f'figures/dashboard_{name}.png',dpi=(300,300),optimize=True)
            import shutil
            shutil.copy2(ROOT/'figures/fig11_dashboard_ui.png',ROOT/'phase3_output/submission_build/figures/fig11_dashboard_ui.png')
            print('Actual landing and atlas captures complete; all browser checks passed',flush=True)
        finally:
            server.terminate();server.wait(timeout=30)
if __name__=='__main__':main()
