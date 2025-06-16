from playwright.sync_api import Page

def prepare_streamlit_app(page: Page, link_text: str):
    page.goto("http://localhost:8501/")
    page.locator("[data-testid='stSidebar']").get_by_role(
        "link", name=link_text, exact=True
    ).click()
    page.evaluate(
        """
        () => {
            document.querySelector('[data-testid="stApp"]').style.position = 'relative';
            document.querySelector('[data-testid="stAppViewContainer"]').style.position = 'relative';
        }
        """
    )
    wait(page)

def wait(page: Page):
    # Taken from https://github.com/streamlit/streamlit/blob/415c3fbfcd7322b2b5199149854cced519ef2b0c/e2e_playwright/conftest.py#L908
    page.locator("[data-testid='stApp'][data-test-script-state='notRunning']").wait_for(state="attached")
    page.locator("[data-testid='stStatusWidget']:has-text('RUNNING')").wait_for(state="hidden")
    # Wait until all blocks are recalculated
    for item in page.locator("[data-stale='true']").all():
        item.wait_for(state="hidden")

def test_foo(page: Page, assert_snapshot):
    prepare_streamlit_app(page, "foo")
    assert_snapshot(page.screenshot(full_page=True), "child_init.png")
    page.locator(".st-key-btn button").click()
    wait(page)
    #page.locator(".st-key-ack").wait_for(state="visible", timeout=2000)
    assert_snapshot(page.screenshot(full_page=True), "child_after.png")
