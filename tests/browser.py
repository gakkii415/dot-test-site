"""Browser QA against a local server or the actual deployed URL."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000'
screens = Path(os.environ.get('SCREENSHOT_DIR', '/tmp/dot-qa'))
screens.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'))
    for name, settings in [('desktop', {'viewport': {'width': 1440, 'height': 1000}}),
                           ('iphone', {**p.devices['iPhone 13'], 'default_browser_type': 'chromium'}),
                           ('narrow', {'viewport': {'width': 320, 'height': 740}})]:
        settings.pop('default_browser_type', None)
        context = browser.new_context(**settings)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        response = page.goto(url)
        assert response.status == 200
        expect(page.locator('h1')).to_have_text('小さな「できた」を、一緒に。')
        expect(page.locator('#app-version')).to_have_text('v2')
        expect(page.locator('#count')).to_have_text('0')
        assert page.locator('#mascot').evaluate('(e) => e.complete && e.naturalWidth > 0')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        test = page.get_by_role('button', name='dotにあいさつ')
        reset = page.get_by_role('button', name='リセット')
        expect(reset).to_be_disabled()
        for count in range(1, 10):
            test.click()
            expect(page.locator('#count')).to_have_text(str(count))
            expect(page.get_by_role('status')).to_contain_text(f'{count}回目のあいさつ')
        page.screenshot(path=str(screens / f'{name}-success.png'), full_page=True)
        reset.click()
        expect(page.locator('#count')).to_have_text('0')
        expect(page.locator('#state')).to_have_text('リセットしました')
        expect(test).to_be_focused()
        expect(reset).to_be_disabled()
        test.press('Enter')
        expect(page.locator('#count')).to_have_text('1')
        test.press('Space')
        expect(page.locator('#count')).to_have_text('2')
        page.keyboard.press('Tab')
        expect(reset).to_be_focused()
        assert reset.evaluate('(e) => getComputedStyle(e).outlineStyle') == 'solid'
        page.keyboard.press('Enter')
        expect(page.locator('#count')).to_have_text('0')
        test.click()
        page.reload()
        expect(page.locator('#count')).to_have_text('0')
        page.emulate_media(reduced_motion='reduce')
        test.click()
        assert page.locator('#mascot').evaluate('(e) => getComputedStyle(e).animationName') == 'none'
        for button in (test, reset):
            assert button.bounding_box()['height'] >= 44
        page.reload()
        page.screenshot(path=str(screens / f'{name}-initial.png'), full_page=True)
        assert not errors, errors
        print(f'PASS {name}: layout, image, 9 clicks, reset, repeat, keyboard, focus, reload, reduced motion, touch targets, no JS errors')
        context.close()
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(url)
    expect(page.locator('.no-script')).to_be_visible()
    expect(page.locator('#test-button')).to_be_disabled()
    print('PASS JavaScript disabled: explanatory fallback and disabled controls')
    browser.close()
