
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # 1. Setup LocalStorage for Admin User and Mock Data
    admin_user = '{"id":"admin","name":"Admin","role":"ADMIN","credits":9999}'
    mock_chapters = '[{"id":"ch1","title":"Chemical Reactions","description":"Chapter 1"}]'
    
    page.goto("http://localhost:5001")
    
    page.evaluate(f"""() => {{
        localStorage.setItem('nst_current_user', '{admin_user}');
        localStorage.setItem('nst_custom_chapters_CBSE-10-Science-English', '{mock_chapters}');
        localStorage.setItem('nst_terms_accepted', 'true');
        localStorage.setItem('nst_has_seen_welcome', 'true');
        sessionStorage.setItem('nst_ad_seen', 'true');
    }}""")
    
    page.reload()

    # Dismiss popups
    try: page.get_by_role("button", name="I Agree & Continue").click(timeout=2000)
    except: pass
    try: page.get_by_role("button", name="Start Learning").click(timeout=2000)
    except: pass
    try: page.get_by_label("Close").click(timeout=2000)
    except: pass
    try: page.get_by_role("button", name="Get Started").click(timeout=2000)
    except: pass
    try: page.get_by_role("button", name="Okay").click(timeout=2000)
    except: pass
    try: page.get_by_role("button", name="CLAIM NOW").click(timeout=2000)
    except: pass
    try: page.get_by_role("button", name="Okay").click(timeout=2000)
    except: pass

    # 2. Verify Admin Dashboard
    expect(page.get_by_text("Admin Console")).to_be_visible(timeout=10000)

    # 3. Click "PDF/AI Notes" (Content Manager)
    page.get_by_text("PDF/AI Notes").first.click()

    # 4. Select Class 10 -> Science -> Chapter
    page.get_by_role("button", name="10", exact=True).click()
    page.get_by_role("button", name="Science", exact=True).click()
    
    expect(page.get_by_text("Chemical Reactions")).to_be_visible()
    page.get_by_role("button", name="Manage All Content").click()

    # 5. Click "HTML Modules" Tab
    # This is the critical step. If it crashes here, we found it.
    page.get_by_role("button", name="HTML Modules").click()
    
    # 6. Check for Inputs
    try:
        expect(page.get_by_text("Interactive HTML Modules (10 Slots)")).to_be_visible()
    except:
        page.screenshot(path="verification/admin_html_fail.png")
        raise

    # Check for inputs
    expect(page.get_by_placeholder("Module Title (e.g. Lab 1)")).to_be_visible()
    
    print("SUCCESS: Admin HTML Tab loaded without white screen.")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
