from soap import checkText

def test_step1(good_text, bad_text):
    assert good_text in checkText(bad_text)